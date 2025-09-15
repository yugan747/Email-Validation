from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import EmailValidationRequestSerializer, EmailValidationResultSerializer
from concurrent.futures import ThreadPoolExecutor, as_completed
from . import validation

MAX_WORKERS = 10

def validate_one(email: str):
    # same as before
    result = {"email": email}
    result["format_valid"] = validation.is_valid_format(email)
    if "@" not in email:
        result["notes"] = "missing @"
        return result

    local, domain = email.rsplit("@", 1)
    mx = validation.get_mx_records(domain)
    result["mx"] = [{"priority": p, "host": h} for p, h in mx] if mx else []
    result["spf_record"] = validation.get_spf_record(domain)
    result["dmarc_record"] = validation.get_dmarc_record(domain)
    result["dkim_selectors_found"] = validation.check_dkim_selectors(domain)
    if mx:
        result["smtp_check"] = validation.smtp_check(email, mx)
    else:
        result["smtp_check"] = {"status": "no-mx"}
    return result

class ValidateEmailsView(GenericAPIView):
    serializer_class = EmailValidationRequestSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        emails = serializer.validated_data["emails"]
        results = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            futures = {ex.submit(validate_one, e): e for e in emails}
            for fut in as_completed(futures):
                try:
                    results.append(fut.result())
                except Exception as exc:
                    results.append({"email": futures[fut], "error": str(exc)})

        response_serializer = EmailValidationResultSerializer(results, many=True)
        return Response({"results": response_serializer.data})
