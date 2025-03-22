import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_credentials(user_email: str) -> Credentials:
    """
    Loads credentials for a given user from a token file specific to that user.
    If the token file does not exist or the credentials are invalid, performs
    the OAuth flow and saves the new token.
    """
    # Use a sanitized token filename in case the email has characters not suited for filenames.
    token_file = f"token_{user_email.replace('@','_at_').replace('.','_')}.json"
    creds = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds

def getmessages() -> str:
    """
    Fetch emails from multiple Gmail accounts (test users) and aggregate the results.
    Returns a concatenated string of email details.
    """
    test_accounts = ["sathyanarayanan0705@gmail.com","sathyanarayanan847@gmail.com"]
    all_emails_text = ""
    
    for user in test_accounts:
        # print(f"Processing account: {user}")
        creds = get_credentials(user)
        service = build("gmail", "v1", credentials=creds)
        
        # Use query targeting primary inbox emails newer than 1 day.
        query = "newer_than:1d category:primary -in:trash -in:spam"
        msgs_response = service.users().messages().list(
            userId="me",
            q=query
        ).execute()
        
        msgs = msgs_response.get("messages", [])
        # print(f"Found {len(msgs)} messages for {user} using query: {query}")
        
        if not msgs:
            all_emails_text += f"No messages found for {user} in the last 24 hours.\n{'-'*40}\n"
            continue

        for msg in msgs:
            message = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = message.get("payload", {}).get("headers", [])
            subject = next((header["value"] for header in headers if header["name"].lower() == "subject"), "No Subject")
            date = next((header["value"] for header in headers if header["name"].lower() == "date"), "No Date")
            
            # Retrieve body of message
            body = ""
            payload = message.get("payload", {})
            if "body" in payload and "data" in payload["body"]:
                body_data = payload["body"]["data"]
                try:
                    body = base64.urlsafe_b64decode(body_data.encode("ASCII")).decode("utf-8")
                except Exception as e:
                    body = f"Error decoding body: {str(e)}"
            elif "parts" in payload:
                for part in payload["parts"]:
                    if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                        body_data = part["body"]["data"]
                        try:
                            body = base64.urlsafe_b64decode(body_data.encode("ASCII")).decode("utf-8")
                        except Exception as e:
                            body = f"Error decoding body: {str(e)}"
                        break

            email_str = (f"User: {user}\nSubject: {subject}\nDate: {date}\n"
                         f"Body: {body}\n{'-'*40}\n")
            all_emails_text += email_str

    return all_emails_text


# mails_txt = getmessages()
# print(mails_txt)


if __name__ == "__main__":
    getmessages()