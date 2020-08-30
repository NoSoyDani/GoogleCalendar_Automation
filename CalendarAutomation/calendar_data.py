from __future__ import print_function
import pickle
import os.path
import time
import datetime
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
DAYS=['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
MONTH=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']


def calendarAut():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def incomingEvents(nEvents,service):
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {nEvents} events')
    eventList = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=nEvents, singleEvents=True,
                                        orderBy='startTime').execute()
    events = eventList.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def createEvent(service,title,day,hour,minutes,durationHour,durationMin):

   instant = datetime.now().date()
   taskInstant = datetime(instant.year, instant.month, instant.day, hour,minutes)+timedelta(days=day)
   startTime = taskInstant.isoformat()
   endTime = (taskInstant + timedelta(hours=durationHour,minutes=durationMin)).isoformat()

   eventInsert = service.events().insert(calendarId='primary',
   body={
           "summary": title,
           "description": '',
           "start": {"dateTime": startTime, "timeZone": 'Europe/Madrid'},
           "end": {"dateTime": endTime, "timeZone": 'Europe/Madrid'},
       }
   ).execute()

   print("Created event")
   print("id: ", eventInsert['id'])
   print("summary: ", eventInsert['summary'])
   print("starts at: ", eventInsert['start']['dateTime'])
   print("ends at: ", eventInsert['end']['dateTime'])


if __name__ == '__main__':
    autService=calendarAut()
    incomingEvents(3,autService)
    createEvent(autService,"tEST OU MAMA",1,16,30,5,0)
# [END calendar_quickstart]
