import random
import uuid

# validate time for accepting otp_code
OTP_TTL_SECONDS = 120

# Time for resending otp_code
OTP_RATE_LIMIT_SECONDS = 120

def generate_otp_code():
    """
    create random code
    """
    return f"{random.randint(10000, 99999)}"

def otp_data_key(phone_number):
    """
    Key for otp_code in redis
    """
    return f"otp:data:{phone_number}"

def otp_limit_key(phone_number):
    """
    Key for checking time for resending otp_code
    """
    return f"otp:limit:{phone_number}"


def generate_session_token():
    """
    generate session token
    """
    return str(uuid.uuid4())

def otp_session_key(session_token):
    """
    make connection between token and phone_number
    """
    return f"otp:session:{session_token}"












