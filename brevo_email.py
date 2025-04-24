import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
import base64
import os
import datetime

load_dotenv()
# Configure API key authorization: api-key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
sender = os.getenv('BREVO_DOMAIN_EMAIL')
name = os.getenv('BREVO_SENDER_NAME')
body = 'test'

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def brevo_send(to_email='bayusuto@gmail.com', to_name="ABM", sender=sender, sender_name=name, subject="test",
               html_content=body, attachment=None, attachment_name=None):
    if attachment:
        attachment_name = attachment_name
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{'email': to_email, 'name': to_name}],
        sender={'email': sender, 'name': sender_name},
        subject=subject,
        html_content=f'<html><body><h1>{html_content}</h1></body></html>',
        attachment=[{'content': attachment, 'name': attachment_name}]
        )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}")
