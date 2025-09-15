import re
import socket
import dns.resolver
import dns.exception

# Regex from a practical subset of RFC 5322 (keeps things simple)
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r'|^"([^"]|\\")*"'
    r')@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$'
)

def is_valid_format(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))

def get_mx_records(domain: str, timeout: int = 5):
    """Return sorted list of (priority, exchange) or []"""
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=timeout)
        mx = sorted([(r.preference, str(r.exchange).rstrip(".")) for r in answers], key=lambda x: x[0])
        return mx
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []

def get_txt_records(name: str, timeout: int = 5):
    try:
        answers = dns.resolver.resolve(name, "TXT", lifetime=timeout)
        return [b"".join(r.strings).decode("utf-8") if isinstance(r.strings, (list, tuple)) else r.strings.decode("utf-8")
                for r in answers]
    except Exception:
        return []

def get_spf_record(domain: str):
    """Find first TXT record that starts with v=spf1"""
    txts = get_txt_records(domain)
    for t in txts:
        if t.lower().startswith("v=spf1"):
            return t
    return None

def get_dmarc_record(domain: str):
    txts = get_txt_records("_dmarc." + domain)
    for t in txts:
        if t.lower().startswith("v=dmarc1") or t.lower().startswith("v=dmarc"):
            return t
    return None

def check_dkim_selectors(domain: str, selectors=None):
    """
    Heuristic check for DKIM: try a small list of common selectors and see if TXT exists.
    Note: true DKIM signature verification requires the signed message (we can't do that here).
    """
    if selectors is None:
        selectors = ["default", "selector1", "s1", "mail", "smtp"]
    found = {}
    for sel in selectors:
        name = f"{sel}._domainkey.{domain}"
        txts = get_txt_records(name)
        if txts:
            found[sel] = txts
    return found  # dict selector -> list of TXT values

import smtplib

def smtp_check(email: str, mx_hosts, from_address="verify@example.com", timeout=10):
    """
    Try SMTP RCPT TO probe. Returns dict with status: 'accept' | 'reject' | 'unknown' and raw response details.
    This function connects to the highest-priority MX record and sends MAIL/RCPT commands.
    WARNING: Many servers will not allow RCPT probes or will have greylisting/catch-all.
    """
    last_exc = None
    for _, host in mx_hosts:
        try:
            # Create SMTP connection (will use socket timeout)
            server = smtplib.SMTP(host, 25, timeout=timeout)
            server.set_debuglevel(0)
            server.ehlo_or_helo_if_needed()
            # Use a harmless MAIL FROM
            code, resp = server.mail(from_address)
            if code >= 400:
                server.quit()
                continue

            code, resp = server.rcpt(email)
            server.quit()
            # rcpt response codes:
            # 250/251 -> accepted (may still be catch-all)
            # 550/5xx -> rejected
            if 200 <= code < 300:
                return {"status": "accept", "code": code, "response": resp.decode() if isinstance(resp, bytes) else str(resp), "mx_host": host}
            elif 400 <= code < 600:
                return {"status": "reject", "code": code, "response": resp.decode() if isinstance(resp, bytes) else str(resp), "mx_host": host}
            else:
                return {"status": "unknown", "code": code, "response": str(resp), "mx_host": host}
        except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError, socket.timeout, ConnectionRefusedError) as e:
            last_exc = str(e)
            continue
        except Exception as e:
            last_exc = str(e)
            continue
    return {"status": "error", "error": last_exc or "no-mx-found"}
