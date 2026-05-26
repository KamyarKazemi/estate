from kavenegar import *



def send_otp_code(phone_number , code):
    api = KavenegarAPI('42684E323047744F3651507868586547384537443437533337653332377A4D7A3942733748496C784D64773D')
    params = { 'sender' : '2000660110', 'receptor': '09029219795', 'message' :f"code is {code} - phone is {phone_number}" }
    response = api.sms_send(params)
