from rest_framework import serializers

class EmailValidationRequestSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child=serializers.EmailField(),
        help_text="List of email addresses to validate",
    )



class EmailValidationResultSerializer(serializers.Serializer):
    email = serializers.EmailField()
    format_valid = serializers.BooleanField()
    mx = serializers.ListField(child=serializers.DictField(), required=False)
    spf_record = serializers.CharField(allow_blank=True, required=False)
    dmarc_record = serializers.CharField(allow_blank=True, required=False)
    dkim_selectors_found = serializers.ListField(child=serializers.CharField(), required=False)
    smtp_check = serializers.DictField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
