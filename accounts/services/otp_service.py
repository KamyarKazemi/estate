from django.core.cache import cache
from accounts.otp import *
from accounts.utils import send_otp_code
from django.contrib.auth import get_user_model

User = get_user_model()


class OTPService:

    @staticmethod
    def send_otp(phone_number):
        code = generate_otp_code()
        session_token = generate_session_token()

        send_otp_code(phone_number , code)
        print(session_token)

        cache.set(otp_data_key(phone_number), code, timeout=OTP_TTL_SECONDS)

        cache.set(otp_limit_key(phone_number) , True , timeout=OTP_RATE_LIMIT_SECONDS)

        cache.set(otp_session_key(session_token) , phone_number , timeout=OTP_TTL_SECONDS)

        cache.delete(f"otp attempts for {phone_number}")

        return session_token