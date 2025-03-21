import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os 
import base64


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def getmessages():
    creds = None 
    
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json",SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        #create gmail api client
        service = build("gmail","v1", credentials=creds)
        msgs = service.users().messages().list(userId="me", q = "newer_than:1d").execute().get("messages",[])
        
        if not msgs:
            print("No messages found in the last 24 hours")
            return
        
        
        for msg in msgs :
            message = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = message.get("payload", {}).get("headers",[])
            subject = next((header["value"] for header in headers if header["name"].lower() == "subject"),"No Subject")
            date = next((header["value"] for header in headers if header["name"].lower() == "date"),"No Date")
            
            #Retrieve Body of message
            body = ""
            payload = message.get("payload",{})
            if "body" in payload and "data" in payload["body"]:
                body_data = payload["body"]["data"]
                body = base64.urlsafe_b64decode(body_data.encode("ASCII")).decode("utf-8")
            elif "parts" in payload:
                # Sometimes the body is split into parts.
                for part in payload["parts"]:
                    if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                        body_data = part["body"]["data"]
                        body = base64.urlsafe_b64decode(body_data.encode("ASCII")).decode("utf-8")
                        break

            print("Subject:", subject)
            print("Date:", date)
            print("Body:", body)
            print("-" * 40)
        
    except HttpError as error:
        print(f"An error occured: {error}")
        
    
if __name__ == "__main__":
    getmessages()