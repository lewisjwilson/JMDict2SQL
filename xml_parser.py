#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from db_creator import create_database, insert_data

tree = ET.parse('JMdict_e')
root = tree.getroot() #root = <JMDict>

create_database()

for entry in root.findall('entry'):

    #initialize lists for elements with possible duplicates
    k_ele_list, r_ele_list, re_restr_list, stagr_list, stagk_list = ([] for i in range(5))
    xref_list, ant_list, pos_list, field_list, misc_list = ([] for i in range(5))
    lsource_list, dial_list, gloss_list, s_inf_list = ([] for i in range(4))

    keb = ""
    ke_inf = ""
    ke_pri = ""
    reb = ""
    re_nokanji = ""
    re_inf = ""
    re_pri = ""

    # unique id for each entry
    ent_seq = entry.find('ent_seq').text

    # ---------kanji elements-----------
    count = 0
    for k_ele in entry.findall('k_ele'):
        count += 1
        k_ele_list.append(count)

    #if the element list isnt empty
    if len(k_ele_list) > 0:

        #for all kanji elements
        for k_ele in entry.findall('k_ele'):

            # [no_duplicates] japanese with at least one non-kana char
            keb = k_ele.find('keb').text

            # try indicates that the element may not exist
            try:
                # orthography details
                ke_inf = k_ele.find('ke_inf').text
            except:
                pass

            try:
                # priority of the kanji entry
                ke_pri = k_ele.find('ke_pri').text
            except:
                pass

    # ---------reading elements-----------
    for r_ele in entry.findall('r_ele'):

        # [no_duplicates] kana readings
        reb = r_ele.find('reb').text

        try:
            # shows that reb is not the true reading
            re_nokanji = r_ele.find('re_nokanji').text
        except:
            pass

        # reading applies to subset of keb elements
        for re_restr in r_ele.findall('re_restr'):
            re_restr_list.append(re_restr)

        if len(re_restr_list) > 0:

            for re_restr in r_ele.findall('re_restr'):
                # reading applies to subset of keb elements
                re_restr = re_restr.text

        try:
            # unusual aspects
            re_inf = r_ele.find('re_inf').text
        except:
            pass

        try:
            # priority of the reading entry
            re_pri = r_ele.find('re_pri').text
        except:
            pass

    # ---------sense elements-----------
    for sense in entry.findall('sense'):

        # indicates the sense is restricted to the lexeme
        # represented by keb/reb
        for stagk in sense.findall('stagk'):
            stagk_list.append(stagk.text)
        for stagr in sense.findall('stagr'):
            stagr_list.append(stagr.text)

        # cross reference to other entry
        for xref in sense.findall('xref'):
            xref_list.append(xref.text)

        # another entry is an antonym of this word
        for ant in sense.findall('ant'):
            ant_list.append(ant.text)

        # part of speech information
        for pos in sense.findall('pos'):
            pos_list.append(pos.text)

        # field of application information
        for field in sense.findall('field'):
            field_list.append(field.text)

        # other relevant information
        for misc in sense.findall('misc'):
            misc_list.append(misc.text)

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

            if origin is None:
                origin = "n/a"
            if lang is None:
                lang = "n/a"
            if ls_type is None:
                ls_type = "n/a"
            if ls_wasei is None:
                ls_wasei = "n/a"

            lsource_list.append('origin: ' + origin +
                                ', lang: ' + lang +
                                ', ls_type: ' + ls_type +
                                ', ls_wasei: ' + ls_wasei)

        # dialect information
        for dial in sense.findall('dial'):
            dial_list.append(dial.text)

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

            if definition is None:
                definition = "n/a"
            if lang is None:
                lang = "n/a"
            if g_gend is None:
                g_gend = "n/a"
            if g_type is None:
                g_type = "n/a"

            gloss_list.append('definition: ' + definition +
                                ', lang: ' + lang +
                                ', gender: ' + g_gend +
                                ', type: ' + g_type)


        # sense information (frequency of senses, regional variations etc.)
        for s_inf in sense.findall('s_inf'):
            s_inf_list.append(s_inf.text)

    insert_data(ent_seq, k_ele_list, keb, ke_inf, ke_pri, r_ele_list, reb, re_nokanji,
                re_restr_list, re_inf, re_pri)

    # purge lists
    k_ele_list, r_ele_list, re_restr_list, stagr_list, stagk_list = ([] for i in range(5))
    xref_list, ant_list, pos_list, field_list, misc_list = ([] for i in range(5))
    lsource_list, dial_list, gloss_list, s_inf_list = ([] for i in range(4))
