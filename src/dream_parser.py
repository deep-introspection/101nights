#! /bin/env python3

"""Parses a document containing chunks of text separated by
   text headers, loading them into a dataframe and saving
   as csv files."""

import re, pandas
from os import path
#import pdb # pdb.set_trace()


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
    
    dict_ = dict( night=nights,
                   place=places,
                   month=months,
                   day=days,
                   text=texts )
    
    return pandas.DataFrame(dict_)

def __main__():

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

    dreams = parse_headers(dream_file, dream_re)
    diary = parse_headers(diary_file, diary_re)

    dreams.to_csv(dream_out)
    diary.to_csv(diary_out)

__main__()
