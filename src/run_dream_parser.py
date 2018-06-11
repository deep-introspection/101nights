#! /bin/env python3

# GNU GPLv3+
# https://www.gnu.org/licenses/gpl-3.0.en.html
# Contributors: Ale Abdo <abdo@member.fsf.org>

""" Produces parsed CSV files ready for pandas.DataFrame
    consumption from both dreams.txt and diary.txt.

    Currently expects to be run from the 'src' dir of the repo.

    More generally, parses a document containing chunks of
    text separated by text headers, loading them into a
    dataframe and saving as csv files."""

import re, pandas
from os import path
from datetime import date, datetime
from numpy import datetime64, timedelta64
import pdb # pdb.set_trace()

YEAR = 2017
GET_MONTH = {'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}.get

def FIX_TIMEZONE(dtimed_texts):
    """
    Convert datetimes for the period from Eugene-OR-USA to UTC
    Ref: https://www.timeanddate.com/time/zone/usa/eugene
    This simple routine works since there are no records between
    01:00 and 02:00 at 'tzchange'
    """
    tzchange = datetime64('2017-05-02T09:00')
    tzdelta0, tzdelta1 = timedelta64(7, 'h'), timedelta64(8, 'h')
    for item in dtimed_texts:
        if item[1] < tzchange:
            item[1] += tzdelta0
        else:
            item[1] += tzdelta1

def parse_headers(source_file, header_re):

    with open(source_file) as f:
        raw_text = f.read()

    re_header = re.compile( header_re, re.I )
    headers = re_header.findall(raw_text)

    split_re = header_re.replace('(', '(?:')
    re_split = re.compile( split_re, re.I )
    texts = re_split.split(raw_text)[1:]
    
    assert len(texts)==len(headers)==101, 'len mismatch, check your regex'
    
    nights, _, places, months, days = zip(*headers)
    dates = [date(YEAR, GET_MONTH(m), int(d)) for m, d in zip(months, days)]

    index = pandas.Index(list(map(int, nights)), name='night')
    dict_ = dict( place=places, date=dates, text=texts )

    return pandas.DataFrame(dict_, index=index)

def parse_times(df):
    time_re = '\n*(\d{1,2}):(\d{1,2}) ?(.*)'
    re_time = re.compile( time_re )

    dtimed_texts = []
    for item in df.itertuples():
        slices = (x.groups() for x in re_time.finditer(item.text) if x)
        for hour, minute, text in slices:
            dt = datetime64(datetime(item.date.year, item.date.month,
                            item.date.day, int(hour), int(minute)))
            dtimed_texts.append( [item.Index, dt, text] )

    FIX_TIMEZONE(dtimed_texts)

    new_index = pandas.Index( [dt for _, dt, _ in dtimed_texts] )

    return pandas.DataFrame(
       ( [df.loc[i, 'place'], txt] for i, _, txt in dtimed_texts ),
        columns=['place', 'text'],
        index=new_index )

def __main__():

    # setup
    raw_path = '../data/raw/TXT'
    derived_path = '../data/derived'

    dream_file = path.join(raw_path, 'dreams.txt')
    dream_out = path.join(derived_path, 'dreams.csv')
    dream_re = (
        '[\n ]*ref.*nights.*dreams *\n' +
        ' *night *(\d+)( *, *(\w+)|.*) *\n' +
        ' *(\w+) *, *(\d+) *[\n ]+' )
    
    diary_file = path.join(raw_path, 'diary.txt')
    diary_out = path.join(derived_path, 'diary.csv')
    diary_re = (
        '[\n ]*ref.*nights *\n' +
        ' *day *(\d+)( *, *(\w+)|.*) *\n' +
        ' *(\w+) *, *(\d+) *[\n ]+' )

    # run parsing functions
    dreams = parse_headers(dream_file, dream_re)
    diary = parse_headers(diary_file, diary_re)
    tdiary = parse_times(diary)

    #import pdb; pdb.set_trace()

    # save to files
    dreams.to_csv(dream_out)
    tdiary.to_csv(diary_out)

__main__()
