import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import config

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'credentials.json'

def get_calendar_service():
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service

def check_for_match_thread():
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='rtfuljfk5q052287gqkgrda7vad3060e@import.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return False
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        text = event['description'].split("\n")
        teams = text[0].split(" v ")

        if teams[0] is "Tottenham Hotspur" :
            home = True
            opponent = teams[1]
        else :
            home = False
            opponent = teams[0]

        print(datetime.datetime.utcnow() + datetime.timedelta(hours=24) < event['start'].get('dateTime'))
        # print(event['start'])
        # print(event['start']['dateTime'])
        subject = "Match Thread"
        message = teams[0] + " vs " + teams[1] +" for /r/" + config["sub_name"]
        break

if __name__ == '__main__':
    check_for_match_thread()
