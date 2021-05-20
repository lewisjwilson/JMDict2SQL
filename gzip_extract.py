#!/usr/bin/env python3

import gzip
import shutil
from xml_parser import parse_xml

try:
    with gzip.open('JMdict_e.gz', 'rb') as f_in:
        with open('JMdict_e', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
except FileNotFoundError:
    print("JMdict_e_gz does not exist in the directory.")
    exit()

parse_xml()
