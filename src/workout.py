import csv
from datetime import datetime

from .wattbike_importer import HubClient


TCX_BASE = './templates/tcx_base'
TCX_TRACKPOINT = './templates/tcx_trackpoint'


class Workout:
    def __init__(self, session_id):
        self.session = HubClient().get_session(session_id)

    def __repr__(self):
        return '<Workout instance :\'{}\'>'.format(self.title)

    def _validate(self):
        assert len(self.session['xAxis']) == len(self.session['hr'])\
                == len(self.session['cadence']) == len(self.session['power'])
    
    def export_to_tcx(self, fname=None):
        with open(TCX_BASE, 'r') as tcx_base_file:
            tcx_base = tcx_base_file.read()

        with open(TCX_TRACKPOINT, 'r') as tcx_trackpoint_file:
            tcx_trackpoint = tcx_trackpoint_file.read()

        trackpoints = str()
        data = zip([self.session[key] for key in ['xAxis', 'hr', 'cadence', 'power']])
        start = datetime.strptime(
            self.session['headers']['startDate']+'.00', '%Y-%m-%d %H:%M:%S.%f'
        )
        min_x_axis = self.session['xAxis'][0]

        for t, hr, cad, pwr in data:
            timestamp = start + datetime.timedelta(0, 0, 0, t - min_x_axis)
            trkp = trkp.replace('{TIMESTAMP}', timestamp.isoformat())
            trkp = trkp.replace('{HEARTRATE}', hr)
            trkp = trkp.replace('{CADENCE}', cad)
            trkp = trkp.replace('{POWER}', pwr)
            trackpoints += '\n' + trkp

        tcx_base = tcx_base.replace('{TRACKPOINTS}', trackpoints)
        tcx_base = tcx_base.replace(
            '{ACTIVITY_ID}', self.session['headers']['sessionId']
        )
        tcx_base = tcx_base.replace(
            '{LAP_STARTIME}', start
        )
        tcx_base = tcx_base.replace(
            '{TOTAL_TIME_SECONDS}', self.session['headers']['timeTotal']
        )
        tcx_base = tcx_base.replace(
            '{DISTANCE_METERS}', 0
        )
        tcx_base = tcx_base.replace(
            '{MAXIMUMSPEED}', 0
        )
        tcx_base = tcx_base.replace(
            '{CALORIES}', 0
        )
        tcx_base = tcx_base.replace(
            '{WATTBIKE_ID}', self.session['headers']['serialNumber']
        )
        
        fname = '{}_{}.tcx'.format(
            self.session['headers']['title'],
            self.session['headers']['title']
        )

        with open(fname, 'w') as output_file:
            output_file.write(tcx_base)

    def export_to_csv(self, fname=None):
        pass
