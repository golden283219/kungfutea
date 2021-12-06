import base64
import datetime
import os
import pickle
import pytz
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from celery.utils.log import get_task_logger
import html.parser
from django.conf import settings

from config.celery import app
from celery import shared_task
from .models import Announcement

User = get_user_model()
logger = get_task_logger(__name__)


@app.task
def refresh_mails():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", ["https://www.googleapis.com/auth/gmail.readonly"],
            )
            creds = flow.run_local_server(port=8000)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    gmail_service = build("gmail", "v1", credentials=creds)

    results = (
        gmail_service.users()
        .messages()
        .list(userId="me", q=settings.GMAIL_QUERY)
        .execute()
    )
    for message in results["messages"]:
        message = (
            gmail_service.users()
            .messages()
            .get(userId="me", id=message["id"])
            .execute()
        )
        try:
            raw_parts = message["payload"]["parts"]
            parts = None

            has_html_part = False
            for part in raw_parts:
                has_html_part = part["mimeType"] == "text/html"

            for part in raw_parts:
                try:
                    if (has_html_part and part["mimeType"] == "text/html") or (
                        not has_html_part and part["mimeType"] == "text/plain"
                    ):
                        parts = base64.b64decode(
                            part["body"]["data"], altchars="-_"
                        ).decode("utf-8")
                    elif part["mimeType"] == "multipart/alternative":
                        raw_parts = part["parts"]

                        has_html_part = False
                        for part in raw_parts:
                            has_html_part = part["mimeType"] == "text/html"

                        for part in raw_parts:
                            if (has_html_part and part["mimeType"] == "text/html") or (
                                not has_html_part and part["mimeType"] == "text/plain"
                            ):
                                parts = base64.b64decode(
                                    part["body"]["data"], altchars="-_"
                                ).decode("utf-8")
                except Exception as e:
                    logger.info(e)

            title_list = [
                h for h in message["payload"]["headers"] if h["name"] == "Subject"
            ]
            title = None
            if len(title_list) == 1:
                title = title_list[0]["value"]

            try:
                Announcement.objects.create(
                    id=message["id"],
                    label_ids=message["labelIds"],
                    snippet=html.unescape(message["snippet"]),
                    internal_date=datetime.datetime.utcfromtimestamp(
                        int(message["internalDate"]) / 1000.0
                    ).replace(tzinfo=pytz.timezone("UTC")),
                    title=title,
                    body=parts,
                )
            except IntegrityError as e:
                logger.info(e)
        except Exception as e:
            logger.info(e)

@shared_task(name="sum_two_numbers")
def add1(x, y):
    return x + y