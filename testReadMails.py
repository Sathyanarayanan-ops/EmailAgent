import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import re
from bs4 import BeautifulSoup

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

def clean_body(encoded_data, mime_type=""):
    try:
        # Decode the base64 data
        body = base64.urlsafe_b64decode(encoded_data.encode("ASCII")).decode("utf-8")
        # Remove links
        body = re.sub(r'http[s]?://\S+', '', body)
        # If the content is HTML, remove HTML tags using BeautifulSoup
        if mime_type.lower() == "text/html":
            body = BeautifulSoup(body, "html.parser").get_text()
        # Normalize whitespace: reduce any sequence of whitespace to a single space
        body = re.sub(r'\s+', ' ', body).strip()
        # Remove zero-width non-joiners and similar invisible characters
        body = body.replace('\u200c', '')
        return body
    except Exception as e:
        return f"Error decoding body: {str(e)}"

def getmessages(n = 1) -> str:
    test_accounts = ["sathyanarayanan0705@gmail.com","sathyanarayanan847@gmail.com"]
    sol = []
    emails_by_user = {}
    
    for user in test_accounts :
        email_list = []
        creds = get_credentials(user)
        service = build("gmail", "v1", credentials=creds)

        
        # Use query targeting primary inbox emails newer than 1 day.
        query = f"newer_than:{n}d category:primary -in:trash -in:spam"
        msgs_response = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            q=query
        ).execute()
        
        # print("msgs_response",msgs_response)
        
        msgs = msgs_response.get("messages", [])
        
        # print("msgs",msgs)
        #msgs has only id and thread id , see how to extract text info from these two information 
        
        
        if not msgs :
            emails_txt = f"No messages found for {user} in the last 24 hours.\n{'-'*40}\n"
            emails_by_user[user] = email_list
            continue
            
            
        else :
            for msg in msgs:
                message = service.users().messages().get(userId="me",id=msg["id"]).execute()
                # print("Given Message********************",message)
                #body': {'size': 0}, 'parts': [{'partId': '0', 'mimeType': 'text/plain', 'filename': '
                
                
                # print("************JSON keys",message.keys())
                
                #Snippet contains subject  snippet': 'Your delivery is scheduled to arrive by 4:03 pm 🚗
                # from headers figure out who it was sent to 
                # headers also has date time 
                
                # So first msgs shows list of emails with id 
                # access a single msg using id ?
                # One message has JSON keys dict_keys(['id', 'threadId', 'labelIds', 'snippet', 'payload', 'sizeEstimate', 'historyId', 'internalDate']) fields
                # Payload********* dict_keys(['partId', 'mimeType', 'filename', 'headers', 'body', 'parts'])

                # Body not really useful 
                
                
                # payload = message.get("payload",{})
                # print("*********Payload*********",payload.keys())
                
                
                
                ########################################################################################
                # snippet = message.get("snippet",{})
                # print("SNIPPET",snippet)
                ############ SNIPPET IS A VERY VALUEABLE TOOL , BUT QUESTION IS HOW TO USE IT PROPERLY 
                
                
                

                headers = message.get("payload", {}).get("headers", [])
                subject = next((header["value"] for header in headers if header["name"].lower() == "subject"), "No Subject")
                receiver = next((header["value"] for header in headers if header["name"].lower() == "to"), "No rx name")
                date = next((header["value"] for header in headers if header["name"].lower() == "date"), "No Date")
                
                
                
                # for p in message["payload"]["parts"]:
                #     if p["mimeType"] in ["text/plain"]:
                #         data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
                #         print(data)
                payload = message.get("payload", {})
                if "body" in payload and "data" in payload["body"]:
                    # body_data = payload["body"]["data"]
                    mime_type = payload.get("mimeType", "text/plain")
                    body = clean_body(payload["body"]["data"], mime_type)
                    # try:
                    #     body = base64.urlsafe_b64decode(body_data.encode("ASCII")).decode("utf-8")
                    #     # body = re.sub(r'http[s]?://\S+', '', body)
                    #     # body = re.sub(r'\s+', ' ', body)
                    #     # body = body.replace('\u200c', '')
                    # except Exception as e:
                    #     body = f"Error decoding body: {str(e)}"
                elif "parts" in payload:
                    body = ""
                    for part in payload["parts"]:
                        # if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                        #     body_data = part["body"]["data"]
                        #     try:
                        #         body = base64.urlsafe_b64decode(body_data.encode("ASCII")).decode("utf-8")
                        #         body = re.sub(r'http[s]?://\S+', '', body)
                        #         body = re.sub(r'\s+', ' ', body)
                        #         body = body.replace('\u200c', '')
                        #     except Exception as e:
                        #         body = f"Error decoding body: {str(e)}"
                        #     break
                        
                        # Check for text/plain first; if you want to support text/html as well,
                        # you could add an elif or use another condition.
                        if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                            body = clean_body(part["body"]["data"], part.get("mimeType", "text/plain"))
                            break
                        # Alternatively, if you want to handle HTML parts as a fallback:
                        elif part.get("mimeType") == "text/html" and "data" in part.get("body", {}):
                            body = clean_body(part["body"]["data"], part.get("mimeType", "text/html"))
                            break
                        
                else:
                    body = "No Body Found"
                        
                        
                # email_str = (f"User: {user}\nSubject: {subject}\nDate: {date}\n"
                #             f"Body: {body}\n{'-'*40}\n")
                # print(email_str)
                
                email_data = {"Subject": subject, "Date": date, "Body": body}
                email_list.append(email_data)
                
        emails_by_user[user] = email_list
            
            

            
            # print("SUBJECT___________",subject)
            
            
            #{'name': 'To', 'value': 'Sathyanarayanan RS <sathyanarayanan847@gmail.com>'} gives who it was sent to 
            
            # print("####################Headers",headers)
            # for header in headers:
            #     print("#####Header",header)
            
    # print(emails_by_user)       
    return emails_by_user

        
if __name__ == "__main__":
    mails_json = getmessages()
    


