#! /bin/env python3

"""Parses a document containing chunks of text separated by
   text headers, loading them into a dataframe and saving
   as csv files."""

import re, pandas
from os import path
from datetime import time, date, datetime
import pdb # pdb.set_trace()

YEAR = 2017
GET_MONTH = {'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}.get

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
    
    dict_ = dict( night=nights,
                  place=places,
                  date=dates,
                  text=texts )
    
    return pandas.DataFrame(dict_)

def parse_times(df, major='night'):
    time_re = '\n*(\d{1,2}):(\d{1,2}) ?(.*)'
    re_time = re.compile( time_re )

    timesliced = df['text'].transform(lambda x: tuple(re_time.finditer(x)))
    dtimed_texts = [ (idx, # old_index
                     datetime(df.loc[idx, 'date'].year, df.loc[idx, 'date'].month, # datetime
                              df.loc[idx, 'date'].day, int(ts[1]), int(ts[2])),
                     ts[3]) # timed_text
                    for idx, slices in timesliced.iteritems()
                    for ts in slices if ts ]

    major_index = df[major] if major else df.index.to_series()
    new_index = pandas.MultiIndex.from_tuples(
        [ (major_index.loc[i], dt) for i, dt, _ in dtimed_texts ],
        names=[major if major else df.index.name, 'time'] )

    return pandas.DataFrame( (
        df.loc[i, ['night', 'place']].tolist() + [dt, txt]
            for i, dt, txt in dtimed_texts ),
        columns=['night', 'place', 'datetime', 'text'],
        index=new_index
    )

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

    # save to files
    dreams.to_csv(dream_out)
    tdiary.to_csv(diary_out)

__main__()
