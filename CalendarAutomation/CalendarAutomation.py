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
timeZone='Europe/Madrid'

def calendarAut():
    global service
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

def incomingEvents(day):
    global service
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventList = service.events().list(calendarId='primary',
                                        timeMin=now,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = eventList.get('items', [])

    if not events:
        print('No hay ningún evento')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        eventTag=event['summary']
        startDivision=str(start).split("T")
        endDivision=str(end).split("T")
        startTimeHour=startDivision[1].split(":")[0]
        startTimeMin=startDivision[1].split(":")[1]
        endTimeHour=endDivision[1].split(":")[0]
        endTimeMin=endDivision[1].split(":")[1]
        eventDate=str(start).split("T")[0]
        dayEvent=str(start).split("T")[0].split("-")[1]
        if(eventDate==day or day==None):
            result="El dia {} tienes un evento títulado {} a las {} y {}, el cuál, acaba a las {} y {}.".format(dayEvent,eventTag,startTimeHour,startTimeMin,endTimeHour,endTimeMin)
        else:
            result="No hay eventos programados para este día."
            print(result)
            break;

        print(result)


def createEvent(title,day,hour,minutes,durationHour,durationMin): #if day=0 is today, if day=1 is tomorrow ...
   global service
   instant = datetime.now().date()
   taskInstant = datetime(instant.year, instant.month, instant.day,hour,minutes)+timedelta(days=day)
   startTime = taskInstant.isoformat()
   endTime = (taskInstant + timedelta(hours=durationHour,minutes=durationMin)).isoformat()

   eventInsert = service.events().insert(calendarId='primary',
   body={
           "summary": title,
           "description": '',
           "start": {"dateTime": startTime, "timeZone": timeZone},
           "end": {"dateTime": endTime, "timeZone": timeZone},
       }
   ).execute()

   print("Created event")
   print("id: ", eventInsert['id'])
   print("summary: ", eventInsert['summary'])
   print("starts at: ", eventInsert['start']['dateTime'])
   print("ends at: ", eventInsert['end']['dateTime'])


if __name__ == '__main__':

    autService=calendarAut()
    todayDate=str(datetime.now()).split(' ')[0]
    incomingEvents(todayDate)

    #createEvent("tEST OU MAMA",0,16,30,5,0)
