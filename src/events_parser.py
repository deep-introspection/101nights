import datetime  # , pytz
import re
import mne
import os
import numpy as np
# from xml.etree import ElementTree
# import dateutil.parser
from parse_xml import get_events_from_xml
import pandas as pd

# def get_time_start_stamp(pathxml):
#     tree = ElementTree.parse(pathxml)
#     root = tree.getroot()
#     children = root.getchildren()
#     timestart = children[1].text
#     time_n = dateutil.parser.parse(timestart)
#     year=int(time_n.strftime('%Y'))
#     month=int(time_n.strftime('%m'))
#     day=int(time_n.strftime('%d'))
#     hour=int(time_n.strftime('%H'))
#     minute=int(time_n.strftime('%M'))
#     second=int(time_n.strftime('%S'))
#     microseconds=int(time_n.strftime('%f'))
#     timezone=int(time_n.strftime('%z'))
#     return datetime.datetime(year, month, day, hour,
#                              minute, second, microseconds)  #, timezone)
#
# def table_times_events(events, times, timestart):
#     event_times = times[events]
#     times_offset = [timestart + datetime.timedelta(seconds=t)
#                     for t in event_times]
#     return np.asarray(times_offset)

def from_raw_2_times(night=None, r_events=None, dir_path=None):
    if r_events is None:
        if dir_path is None:
           dir_path = "../data/raw/EEG"
        pattern = r'Nathalie.+\.mff'
        files = [f for f in os.listdir(dir_path) if re.match(pattern, f)]
        mne.set_log_level(verbose='CRITICAL')
        for nf, f in enumerate(files):
            fields = re.findall(pattern='\d+', string=f)
            nonight = int(fields[0])
            if nonight == night:
                break
        path_to_file = os.path.join(dir_path, files[nf])
        raw = mne.io.read_raw_egi(path_to_file,
                                  montage='GSN-HydroCel-256',
                                  preload=False)
        events = mne.find_events(raw)
    else:
        raw = r_events['raw']
        events = r_events['events']
    print(datetime.datetime.fromtimestamp(raw.info['meas_date'][0]))
    s = [t for t,n,e in events if e==raw.event_id['DIN1']]
    word_events = []
    fs = raw.info['sfreq']
    for i,inception in enumerate(s):
        if inception/fs+55 <= raw.times.max():
            timing = datetime.datetime.fromtimestamp(
            raw.info['meas_date'][0]+inception/fs)
            word_events.append({"time": timing, "index": i})
    return word_events

    # pathxml = os.path.join(pathmff, "info.xml")
    # raw = mne.io.read_raw_egi(pathmff, preload=False)
    # events = mne.find_events(raw)
    # initial_time = get_time_start_stamp(pathxml)
    # print(initial_time)
    # events_table = table_times_events(events[:, 0], raw.times,
    #                                   initial_time)
    # return events_table

def table_night(night, obj=None):
    # night = 67
    events = get_events_from_xml()
    if obj is not None:
        events_eeg = from_raw_2_times(night=night, r_events=obj)
    else:
        events_eeg = from_raw_2_times(night=night)

    dfeeg = pd.DataFrame(columns=["time", "index"])
    for eveeg in events_eeg:
        dfeeg = dfeeg.append(eveeg, ignore_index=True)

    dfwords = events.loc[events.night==night]
    dfwords = dfwords.loc[dfwords.type == "auto"]

    detime = []
    for it, evt in enumerate(dfeeg.time.values):
        detime.append(evt - dfwords.time.values[it])
    dfeeg['detime'] = detime

    alineado = pd.merge_asof(dfwords, dfeeg, on='time',
                             direction="forward")
    alineado.drop(['delta_time', 'type'], axis=1, inplace=True)
    alineado.dropna(inplace=True)
    alineado.drop_duplicates("index", inplace=True)
    alineado.set_index("index", drop=True, inplace=True)
    return alineado

if __name__ == "__main__":
    events_table = from_raw_2_times()
