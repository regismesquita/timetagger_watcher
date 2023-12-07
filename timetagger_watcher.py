import os
import logging
import time
from datetime import datetime, timezone

import requests
import urllib3
from aw_client import ActivityWatchClient
from aw_core.models import Event

# Constants
TIME_TAGGER_URL = os.environ.get("TIMETAGGER_URL", "https://timetagger.timetagger.orb.local/timetagger/api/v2/records")
VERIFY_CERTIFICATE = False # Set it to true if you don't have a self-signed cert.
SLEEP_TIME = 1  # seconds
BUCKET_ID_FORMAT = "{}_timetagger-bucket"

# Disable warnings
if not VERIFY_CERTIFICATE:
	urllib3.disable_warnings() 

# Set up logging
log_level = os.environ.get("LOG_LEVEL", logging.WARNING)
logging.basicConfig(level=log_level)

def get_timetagger_token():
    token = os.environ.get("TIMETAGGER_TOKEN")
    if not token:
        raise ValueError("TIMETAGGER_TOKEN environment variable not set.")
    return token

def get_current_task_from_timetagger():
    token = get_timetagger_token()
    headers = {"authtoken": token}
    current_unix_time = int(time.time())
    timerange = f"{current_unix_time}-{current_unix_time}"
    params = {"timerange": timerange}
    try:
        response = requests.get(TIME_TAGGER_URL, params=params, headers=headers, verify=VERIFY_CERTIFICATE)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code.
        records = response.json().get('records', [])
        if not records:
            logging.info("No records found for the current time.")
            return None
        return records[0].get('ds')
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve current task from TimeTagger: {e}")
        return None

def main():
    client = ActivityWatchClient("timetagger")
    hostname = client.client_hostname
    bucket_id = BUCKET_ID_FORMAT.format(hostname)
    client.create_bucket(bucket_id, event_type="tag")

    with client:
        while True:
            task = get_current_task_from_timetagger()
            if task:
                heartbeat_data = {"tag": task}
                now = datetime.now(timezone.utc)
                heartbeat_event = Event(timestamp=now, data=heartbeat_data)

                client.heartbeat(bucket_id, heartbeat_event,
                                 pulsetime=SLEEP_TIME + 1,
                                 queued=True,
                                 commit_interval=4.0)

            time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
