import csv
import datetime
import os

import numpy as np

from .wattbike_importer import HubClient


BASE_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), './templates/tcx_base')
TRACKPOINT_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), './templates/tcx_trackpoint')


class Workout:
    def __init__(self, session_ids):
        self.sessions = list()
        for session_id in session_ids:
            self.sessions.append(HubClient().get_session(session_id))

    def __repr__(self):
        return '<Workout instance containing {} sessions>'.format(len(self.session))

    def export_to_tcx(self, fname=None, session=None):
        if session:
            sessions = [session]
        else:
            sessions = self.sessions
        
        trackpoints = str()
        min_starttime = datetime.datetime.now()
        total_time = 0.0
        total_hr = 0.0
        hr_max = 0
        total_cad = 0
        total_pwr = 0

        for session in sessions:
            trackpoints += self._tcx_render_trackpoints(session)

            session_start = datetime.datetime.strptime(
                session['headers']['startDate'], '%Y-%m-%d %H:%M:%S'
            )
            if session_start < min_starttime:
                min_starttime = session_start
            duration = float(session['headers']['timeTotal'])
            total_time += duration
            total_hr += float(session['headers']['hrAvg'])*duration
            if float(session['headers']['hrPeak']) > hr_max:
                hr_max = float(session['headers']['hrPeak'])
            total_cad += float(session['headers']['cadence'])*duration
            total_pwr += float(session['headers']['powerAvg'])*duration

        tcx_string = self._tcx_render_base(
            trackpoints=trackpoints,
            start_time=min_starttime.isoformat(),
            total_time=int(total_time),
            avg_hr=int(total_hr/total_time),
            max_hr=int(hr_max),
            avg_cad=int(total_cad/total_time),
            avg_pwr=int(total_pwr/total_time)
        )

        fname = '{}_{}.tcx'.format(
            self.sessions[0]['headers']['title'],
            min_starttime
        )

        with open(fname, 'w') as output_file:
            output_file.write(tcx_string)

    def export_to_csv(self, fname=None):
        pass

    def _tcx_render_trackpoints(self, session=None, trackpoint_template=None):
        trackpoint_template = trackpoint_template if trackpoint_template\
            else TRACKPOINT_TEMPLATE
        with open(trackpoint_template, 'r') as tcx_trackpoint_file:
            tcx_trackpoint = tcx_trackpoint_file.read()

        session = session if session else self.session[0]

        start_ts = session['xAxis'][0]
        timestamps = [(ts - start_ts)/1000. for ts in session['xAxis']]
        x_axis = range(max(session['time']))
        heartrate = np.interp(x_axis, timestamps, session['hr'])
        cadence = np.interp(x_axis, timestamps, session['cadence'])
        power = np.interp(x_axis, timestamps, session['power'])

        trackpoints = str()
        start = datetime.datetime.strptime(
            session['headers']['startDate'], '%Y-%m-%d %H:%M:%S'
        )

        for t, hr, cad, pwr in zip(x_axis, heartrate, cadence, power):
            timestamp = start + datetime.timedelta(0, t)
            trkp = tcx_trackpoint.replace('{TIMESTAMP}', timestamp.isoformat()+'Z')
            trkp = trkp.replace('{HEARTRATE}', str(int(hr)))
            trkp = trkp.replace('{CADENCE}', str(int(cad)))
            trkp = trkp.replace('{POWER}', str(int(pwr)))
            trackpoints += trkp

        return trackpoints
        
    def _tcx_render_base(self, trackpoints, start_time, total_time, avg_hr,
                         max_hr, avg_cad, avg_pwr, dist=0.0,
                         cal=0, avg_spd=0.0, max_spd=0.0,
                         base_template=None):

        base_template = base_template if base_template\
            else BASE_TEMPLATE

        with open(base_template, 'r') as tcx_base_file:
            tcx_base = tcx_base_file.read()
        repl_dict = {
            '{TRACKPOINTS}': trackpoints,
            '{ACTIVITY_ID}': start_time+'Z',
            '{LAP_STARTTIME}': '"'+start_time+'Z"',
            '{TOTAL_TIME_SECONDS}': str(total_time),
            '{DISTANCE_METERS}': str(dist),
            '{MAXIMUMSPEED}': str(max_spd),
            '{CALORIES}': str(cal),
            '{AVERAGE_HEARTRATE}': str(avg_hr),
            '{MAXIMUM_HEARTRATE}': str(max_hr),
            '{AVERAGE_CADENCE}': str(avg_cad),
            '{AVERAGE_WATTS}': str(avg_pwr),
            '{AVERAGE_SPEED}': str(avg_spd)
        }

        for key, val in repl_dict.items():
            tcx_base = tcx_base.replace(key, val)

        return tcx_base
