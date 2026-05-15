import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ON24Client:
    BASE_URL = "https://api.on24.com/v2/client"

    def __init__(
        self,
        api_token: str,
        api_key: str,
        timeout: int = 60,
    ):
        self.session = requests.Session()

        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )

        adapter = HTTPAdapter(max_retries=retries)

        self.session.mount("https://", adapter)

        self.session.headers.update(
            {
                "api-token": api_token,
                "api-key": api_key,
                "Content-Type": "application/json",
            }
        )

        self.timeout = timeout

    def get_events(
        self,
        start_date: str,
        end_date: str,
    ) -> list[dict]:

        url = f"{self.BASE_URL}/event"

        response = self.session.get(
            url,
            params={
                "startDate": start_date,
                "endDate": end_date,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json().get("events", [])

    def get_registrants(self, event_id: str):
        url = f"{self.BASE_URL}/event/{event_id}/registrant"

        response = self.session.get(url, timeout=self.timeout)

        response.raise_for_status()

        return response.json()

    def get_attendees(self, event_id: str):
        url = f"{self.BASE_URL}/event/{event_id}/attendee"

        response = self.session.get(url, timeout=self.timeout)

        response.raise_for_status()

        return response.json()