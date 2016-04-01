import requests


HUB_LOCATION = 'http://hub.wattbike.com/ranking/getSessionRows?sessionId='

class Workout:
    def __init__(self, timestamps: list, heartrate: list, cadence: list, power: list):
        self.timestamps = timestamps
        self.heartrate = heartrate
        self.cadence = cadence[:-3]
        self.power = power
        self._validate()

    def __repr__(self):
        return '<instance of Workout class (Wattbike Session)>'

    def _validate(self):
        assert len(self.timestamps) == len(self.heartrate) == len(self.cadence)\
                == len(self.power)


class HubClient:
    def __init__(self, location=None):
        self.location = location if location else HUB_LOCATION

    def validate_session_id(self, session_id):
        # TODO: add regex validation of session_id
        return HUB_LOCATION + session_id

    def get_session(self, session_id):
        session_url = self.validate_session_id(session_id)
        
        resp = requests.get(session_url)
        if resp.status_code != 200:
            raise requests.HTTPError('Response status code != 200')

        data = resp.json()

        try:
            timestamps = data['time']
            heartrate = data['hr']
            cadence = data['cadence']
            power = data['power']
        except KeyError as e:
            raise KeyError('JSON response has missing data: {}'.format(e))

        workout = Workout(
            timestamps=timestamps,
            heartrate=heartrate,
            cadence=cadence,
            power=power
        )

        return workout

