import pytz, datetime
import mne
import os
import numpy as np
from xml.etree import ElementTree
import dateutil.parser

def get_time_start_stamp(pathxml):
    tree = ElementTree.parse(pathxml)
    root = tree.getroot()
    children = root.getchildren()
    timestart = children[1].text
    time_n = dateutil.parser.parse(timestart)
    year=int(time_n.strftime('%Y'))
    month=int(time_n.strftime('%m'))
    day=int(time_n.strftime('%d'))
    hour=int(time_n.strftime('%H'))
    minute=int(time_n.strftime('%M'))
    second=int(time_n.strftime('%S'))
    microseconds=int(time_n.strftime('%f'))
    timezone=int(time_n.strftime('%z'))
    return datetime.datetime(year, month, day, hour,
                             minute, second, microseconds)  #, timezone)

def table_times_events(events, times, timestart):
    event_times = times[events]
    times_offset = [timestart + datetime.timedelta(seconds=t)
                    for t in event_times]
    return np.asarray(times_offset)

def from_raw_2_times(pathmff=None):
    if pathmff is None:
       pathmff = "../data/raw/EEG/Nathalie-78_20171118_123017.mff"
    pathxml = os.path.join(pathmff, "info.xml")
    raw = mne.io.read_raw_egi(pathmff, preload=False)
    events = mne.find_events(raw)
    initial_time = get_time_start_stamp(pathxml)
    print(initial_time)
    events_table = table_times_events(events[:, 0], raw.times,
                                      initial_time)
    return events_table

if __name__ == "__main__":
    events_table = from_raw_2_times()
