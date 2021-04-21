#!/usr/bin/env python3

import gzip
import shutil

with gzip.open('JMdict_e.gz', 'rb') as f_in:
    with open('JMdict_e', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
