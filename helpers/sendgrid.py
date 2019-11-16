import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(content):
    # Send email to single receipient
    message = Mail(
        from_email='admin@nextagram.com',
        to_emails='l783l74@hotmail.com',
        subject='New follow request',
        html_content=f'<strong>{content}</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(str(e))