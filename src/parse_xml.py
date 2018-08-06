import os
from lxml import etree
import pandas as pd
from datetime import datetime

def text_to_datetime(time_txt):
    return datetime(*[int(fields) for fields in time_txt.split("-")])

def build_tuple(message):
    time, word = message.getchildren()
    return {"time": text_to_datetime(time.text), "word": word.text,
            "type": message.get(key="type")}

# def parse_file(fname):

def get_events_from_xml():
    pathxmls = '../data/raw/XML'
    files = [fil for fil in os.listdir(pathxmls) if fil[-4:] == ".xml"]
    df = pd.DataFrame(columns=["time", "word", "type"])
    for file in files:
        xmlpath = os.path.join(pathxmls, file)
        xml = open(xmlpath, "r").read()
        parser = etree.XMLParser(ns_clean=True, recover=True)
        tree = etree.fromstring("<data>{0}</data>".format(xml), parser)
        root = tree.getroottree().getroot()
        messages = [build_tuple(e) for e in root.getchildren()
                    if e.tag == "message"]
        for message in messages:
            df = df.append(message, ignore_index=True)

    assert len(df.time.unique()) == len(df.time)
    df.set_index('time', drop=False, inplace=True)
    df.sort_index(inplace=True)
    df['delta_time'] = df.time.diff().dt.seconds.div(60*60, fill_value=0)
    df['night'] = (df.delta_time > 7).cumsum() #  7h seems to be a good threshold to split days
    #df.drop(['time', 'delta_time'], axis=1, inplace=True)

    return df
