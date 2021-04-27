#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from db_creator import *

tree = ET.parse('JMdict_e')
root = tree.getroot() #root = <JMDict>

create_database()
conn = create_connection(r"sqlite.db")

k_ele_id = 0
r_ele_id = 0
sense_id = 0
gloss_id = 0

entry_data, k_ele_data, r_ele_data, sense_data = ([] for i in range(4))
ke_inf_data, ke_pri_data, re_inf_data, re_restr_data = ([] for i in range(4))
re_pri_data, stagk_data, stagr_data, pos_data = ([] for i in range(4))
xref_data, ant_data, field_data, misc_data = ([] for i in range(4))
lsource_data, dial_data, gloss_data, s_inf_data = ([] for i in range(4))
pri_data = []

for entry in root.findall('entry'):

    # unique id for each entry
    ent_seq = entry.find('ent_seq').text

    # ---------kanji elements-----------
    count = 0
    for k_ele in entry.findall('k_ele'):
        count += 1
        break

    #if there are more than one elements
    if count > 0:

        #for all kanji elements
        for k_ele in entry.findall('k_ele'):

            # [no_duplicates] japanese with at least one non-kana char
            keb = k_ele.find('keb').text
            k_ele_data.append((ent_seq, keb))
            k_ele_id += 1

            # try indicates that the element may not exist
            try:
                # orthography details
                ke_inf = k_ele.find('ke_inf').text
                ke_inf_data.append((k_ele_id, ke_inf))
            except:
                pass

            try:
                # priority of the kanji entry
                ke_pri = k_ele.find('ke_pri').text
                ke_pri_data.append((k_ele_id, ke_pri))
            except:
                pass

    # ---------reading elements-----------
    for r_ele in entry.findall('r_ele'):

        # [no_duplicates] kana readings
        reb = r_ele.find('reb').text
        no_kanji = r_ele.find('re_nokanji')
        if no_kanji is not None:
            r_ele_data.append((ent_seq, reb, 1))
        else:
            r_ele_data.append((ent_seq, reb, 0))

        r_ele_id += 1
        
        count = 0
        # reading applies to subset of keb elements
        for re_restr in r_ele.findall('re_restr'):
            count += 1
            break

        if count > 0:
            for re_restr in r_ele.findall('re_restr'):
                # reading applies to subset of keb elements
                re_restr = re_restr.text
                re_restr_data.append((r_ele_id, re_restr))

        try:
            # unusual aspects
            re_inf = r_ele.find('re_inf').text
            re_inf_data.append((r_ele_id, re_inf))
        except:
            pass

        try:
            # priority of the reading entry
            re_pri = r_ele.find('re_pri').text
            re_pri_data.append((r_ele_id, re_pri))
        except:
            pass

    # ---------sense elements-----------
    for sense in entry.findall('sense'):
        sense_data.append((ent_seq,))
        sense_id += 1

        # indicates the sense is restricted to the lexeme
        # represented by keb/reb
        for stagk in sense.findall('stagk'):
            stagk_data.append((sense_id, stagk.text))
        for stagr in sense.findall('stagr'):
            stagr_data.append((sense_id, stagr.text))

        # cross reference to other entry
        for xref in sense.findall('xref'):
            xref_data.append((sense_id, xref.text))

        # another entry is an antonym of this word
        for ant in sense.findall('ant'):
            ant_data.append((sense_id, ant.text))

        # part of speech information
        for pos in sense.findall('pos'):
            pos_data.append((sense_id, pos.text))

        # field of application information
        for field in sense.findall('field'):
            field_data.append((sense_id, field.text))

        # other relevant information
        for misc in sense.findall('misc'):
            misc_data.append((sense_id, misc.text))

        # source language of loan words
        for lsource in sense.findall('lsource'):

            # origin word
            origin = lsource.text

            # source language
            lang = lsource.get('{http://www.w3.org/XML/1998/namespace}lang')

            # does lsource element fully describe the word (default: fully)
            ls_type = lsource.get('ls_type')

            # Japanese word constructed from words in source language
            ls_wasei = lsource.get('ls_wasei')

            lsource_data.append((sense_id, origin, lang, ls_type, ls_wasei))

        # dialect information
        for dial in sense.findall('dial'):
            dial_data.append((sense_id, dial.text))

        # definitions
        for gloss in sense.findall('gloss'):

            # definition
            definition = gloss.text

            # definition language
            lang = gloss.get('{http://www.w3.org/XML/1998/namespace}lang')

            # definition gender
            g_gend = gloss.get('g_gend')

            # definition type (e.g. 'lit' (literal), 'fig' (figurative), etc)
            g_type = gloss.get('g_type')

            gloss_data.append((sense_id, definition, lang, g_gend, g_type))

            gloss_id += 1

            for pri in gloss.findall('pri'):
                pri_data.append((gloss_id, pri.text))

        # sense information (frequency of senses, regional variations etc.)
        for s_inf in sense.findall('s_inf'):
            s_inf_data.append((sense_id, s_inf.text))

    entry_data.append((ent_seq,))

insert_data(conn, 'entry', entry_data)
# -----------k_ele tables-------------
insert_data(conn, 'k_ele', k_ele_data)
insert_data(conn, 'ke_inf', ke_inf_data)
insert_data(conn, 'ke_pri', ke_pri_data)
# -----------r_ele tables-------------
insert_data(conn, 'r_ele', r_ele_data)
insert_data(conn, 're_restr', re_restr_data)
insert_data(conn, 're_inf', re_inf_data)
insert_data(conn, 're_pri', re_pri_data)
# -----------sense tables-------------
insert_data(conn, 'sense', sense_data)
insert_data(conn, 'stagk', stagk_data)
insert_data(conn, 'stagr', stagr_data)
insert_data(conn, 'pos', pos_data)
insert_data(conn, 'xref', xref_data)
insert_data(conn, 'ant', ant_data)
insert_data(conn, 'field', field_data)
insert_data(conn, 'misc', misc_data)
insert_data(conn, 'lsource', lsource_data)
insert_data(conn, 'dial', dial_data)
insert_data(conn, 'gloss', gloss_data)
insert_data(conn, 's_inf', s_inf_data)

insert_data(conn, 'pri', pri_data)
