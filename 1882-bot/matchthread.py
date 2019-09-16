import datetime
import dateutil.parser as parser
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datahandler
from config import config
from log_it import log_it

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

def check_for_match_thread(r, logfile):
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='rtfuljfk5q052287gqkgrda7vad3060e@import.calendar.google.com', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return False
    for event in events:
        text = event['description'].split("\n")
        teams = text[0].split(" v ")
        now = datetime.datetime.now(datetime.timezone.utc)
        diff = parser.parse(event['start']['dateTime']) - now

        if teams[0] is "Tottenham Hotspur" :
            home = True
            opponent = teams[1]
        else :
            home = False
            opponent = teams[0]

        # if diff.days < 1:
        #     # TODO: Create pre-match thread
        #     # Check if one exists, if not post
        #     break

        if diff.days < 1 and int(diff.seconds / 60) < 5:
            # Fire if fewer than 1 day and less than 5 minutes
            history = datahandler.get("matchthreads")
            if str(event['start']) not in history:
                log_it(logfile, "\tFound match within 5 minutes! Sending message to MatchThreader...")
                subject = "Match Thread"
                message = teams[0] + " vs " + teams[1] +" for /r/" + config["sub_name"]
                r.redditor('MatchThreadder').message(subject, message)
                datahandler.addTo("matchthreads", str(event['start']))
                break
