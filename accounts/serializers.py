from rest_framework import serializers
import re

class SendOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11 ,required=True)

    def validate_phone_number(self, value):
        value = value.strip()

        if re.fullmatch(r"9\d{9}", value):  # اگر کاربر 912 فرستاد
            value = "0" + value

        if not re.fullmatch(r"09\d{9}", value):
            raise serializers.ValidationError("شماره موبایل معتبر نیست. باید با 09 شروع شود.")

        return value
