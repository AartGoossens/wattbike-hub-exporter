import requests


HUB_LOCATION = 'http://hub.wattbike.com/ranking/getSessionRows?sessionId='


class HubClient:
    def __init__(self, location=None):
        self.location = location if location else HUB_LOCATION

    def _validate_session_id(self, session_id):
        # TODO: add regex validation of session_id
        return HUB_LOCATION + session_id

    def get_session(self, session_id):
        session_url = self._validate_session_id(session_id)

        resp = requests.get(session_url)
        if resp.status_code != 200:
            raise requests.HTTPError('Response status code != 200')

        return resp.json()
