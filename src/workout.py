import csv
import datetime
import os

import numpy as np

from .wattbike_importer import HubClient


TCX_BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), './templates/tcx_base')
TCX_TRACKPOINT = os.path.join(os.path.dirname(os.path.realpath(__file__)), './templates/tcx_trackpoint')


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

        start_ts = self.session['xAxis'][0]
        timestamps = [(ts - start_ts)/1000. for ts in self.session['xAxis']]
        x_axis = self.session['time']
        heartrate = np.interp(x_axis, timestamps, self.session['hr'])
        cadence = np.interp(x_axis, timestamps, self.session['cadence'])
        power = np.interp(x_axis, timestamps, self.session['power'])

        trackpoints = str()
        start = datetime.datetime.strptime(
            self.session['headers']['startDate'], '%Y-%m-%d %H:%M:%S'
        )

        for t, hr, cad, pwr in zip(x_axis, heartrate, cadence, power):
            timestamp = start + datetime.timedelta(0, t)
            trkp = tcx_trackpoint.replace('{TIMESTAMP}', timestamp.isoformat()+'Z')
            trkp = trkp.replace('{HEARTRATE}', str(int(hr)))
            trkp = trkp.replace('{CADENCE}', str(int(cad)))
            trkp = trkp.replace('{POWER}', str(int(pwr)))
            trackpoints += trkp

        tcx_base = tcx_base.replace('{TRACKPOINTS}', trackpoints)
        tcx_base = tcx_base.replace(
            '{ACTIVITY_ID}', start.isoformat()+'Z'
        )
        tcx_base = tcx_base.replace(
            '{LAP_STARTTIME}','"'+ start.isoformat()+'Z"'
        )
        tcx_base = tcx_base.replace(
            '{TOTAL_TIME_SECONDS}', str(int(float(self.session['headers']['timeTotal'])))
        )
        tcx_base = tcx_base.replace(
            '{DISTANCE_METERS}', str(0.0)
        )
        tcx_base = tcx_base.replace(
            '{MAXIMUMSPEED}', str(0.0)
        )
        tcx_base = tcx_base.replace(
            '{CALORIES}', str(0)
        )
        tcx_base = tcx_base.replace(
            '{AVERAGE_HEARTRATE}', self.session['headers']['hrAvg']
        )
        tcx_base = tcx_base.replace(
            '{MAXIMUM_HEARTRATE}', self.session['headers']['hrPeak']
        )
        tcx_base = tcx_base.replace(
            '{AVERAGE_CADENCE}', self.session['headers']['cadence']
        )
        tcx_base = tcx_base.replace(
            '{AVERAGE_WATTS}', self.session['headers']['powerAvg']
        )
        tcx_base = tcx_base.replace(
            '{AVERAGE_SPEED}', str(0)
        )
        
        fname = '{}_{}.tcx'.format(
            self.session['headers']['title'],
            self.session['headers']['title']
        )

        with open(fname, 'w') as output_file:
            output_file.write(tcx_base)

    def export_to_csv(self, fname=None):
        pass
