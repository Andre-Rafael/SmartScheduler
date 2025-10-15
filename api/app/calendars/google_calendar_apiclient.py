from pathlib import Path
from calendars.calendar_api_repository_mixin import ApiCalendarRepositoryMixin
from smart_schedule.schemas.new_event import NewEvent

from requests import post, get
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendarApiclient(ApiCalendarRepositoryMixin):
    def __init__(self):
        pass

    def list_events(self):
        return super().list_events()

    def get_event(self):
        return super().get_event()

    def delete_event(self):
        return super().delete_event()

    def update_event(self):
        return super().update_event()

    def create_event(self, event: NewEvent):
        calendarId = "primary"
        post(
            f"https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events",
            json={
                "summary": event.title,
                "start": {"date": "", "dateTime": "", "timeZone": ""},
                "end": {"date": "", "dateTime": "", "timeZone": ""},
                "location": event.place,
            },
        )
