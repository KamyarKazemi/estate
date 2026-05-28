import random

# validate time for accepting otp_code
OTP_TTL_SECONDS = 120

# Time for resending otp_code
OTP_RATE_LIMIT_SECONDS = 120

def generate_otp_code():
    """
    create random code
    :return:
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
