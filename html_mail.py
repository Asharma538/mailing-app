import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def create_text_message(sender, to, subject, text_content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = to

    text_part = MIMEText(text_content, "html")
    message.attach(text_part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw_message}

def send_email(to_email, name):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    # Read text content from a text file
    text_content = open("index.html", "r").read()
    text_content = text_content.replace("[Last Name]", name.split()[-1])

    message = create_text_message(
        sender="me",
        to=to_email,
        subject="Digital Attendance & AI-Powered Quiz Platform",
        text_content=text_content,
    )

    send_result = service.users().messages().send(userId="me", body=message).execute()
    print("Message sent, ID:", send_result["id"])

if __name__ == "__main__":
    i = 0
    mailing_list = open("mailing_list.txt", "r").readlines()
    mailing_list = [email.strip() for email in mailing_list if email.strip()]
    while i < 1:
        print(mailing_list[i])
        name, email = map(str, mailing_list[i].split(","))
        send_email(email.strip(), name.strip())
        print("sent to: ", email, i)
        i += 1
    print("All emails sent successfully.")
