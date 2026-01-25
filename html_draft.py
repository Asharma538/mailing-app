import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

def create_text_message(sender, to, subject, text_content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = to
    # message["cc"] = ""

    text_part = MIMEText(text_content, "html")
    message.attach(text_part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw_message}

def create_draft(to_email):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    # Read text content from a text file
    text_content = open("index.html", "r").read()
    
    message = create_text_message(
        sender="Anadi Sharma <sharma.130@alumni.iitj.ac.in>",
        to=to_email,
        subject="Subject Here",
        text_content=text_content,
    )

    # Create draft instead of sending
    draft_body = {"message": message}
    draft_result = service.users().drafts().create(userId="me", body=draft_body).execute()
    print("Draft created, ID:", draft_result["id"])

if __name__ == "__main__":
    i = 0
    mailing_list = open("mailing_list.txt", "r").readlines()
    mailing_list = [email.strip() for email in mailing_list if email.strip()]
    while i < len(mailing_list):
        print(mailing_list[i])
        email = mailing_list[i]
        create_draft(email.strip())
        print("Draft created for: ", email, i)
        i += 1
    print("All drafts created successfully.")
