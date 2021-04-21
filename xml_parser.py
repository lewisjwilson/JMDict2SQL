#!/usr/bin/env python3

"""
In comments, * refers to an item which is always present (try/catch needn't be used)

"""

import xml.etree.ElementTree as ET

tree = ET.parse('JMdict_e')
root = tree.getroot() #root = <JMDict>


for entry in root.findall('entry'):

    # unique id for each entry
    ent_seq = entry.find('ent_seq').text


    # kanji elements
    k_ele_list = []

    for k_ele in entry.findall('k_ele'): #kanji elements
        k_ele_list.append(k_ele)


    if len(k_ele_list) > 0: #if the element list isnt empty

        for k_ele in entry.findall('k_ele'): #for all kanji elements

            keb = k_ele.find('keb').text # *japanese with at least one non-kana char

            try:
                ke_inf = k_ele.find('ke_inf').text # orthography details
            except:
                print('', end='') # print nothing

            try:
                ke_pri = k_ele.find('ke_pri').text # priority of the kanji entry
            except:
                print('', end='') #print nothing


    # reading elements
    r_ele_list = []

    for r_ele in entry.findall('r_ele'): # *reading elements

        reb = r_ele.find('reb').text # *kana readings

        try:
            re_nokanji = r_ele.find('re_nokanji').text # shows the reb is not the true reading
        except:
            print('', end='') #print nothing

        re_restr_list = []

        for re_restr_entry in r_ele.findall('re_restr'): # reading applies to subset of keb elements
            re_restr_list.append(re_restr_entry)

        if len(re_restr_list) > 0: #if list isn't empty

            for re_restr_entry in r_ele.findall('re_restr'):
                re_restr = re_restr_entry.text # reading applies to subset of keb elements

        try:
            re_inf = r_ele.find('re_inf').text # unusual aspects
        except:
            print('', end='') #print nothing

        try:
            re_pri = r_ele.find('re_pri').text # priority of the reading entry
            print(re_pri)
        except:
            print('', end='') #print nothing

    k_ele_list = []
    r_ele_list = []
    re_restr_list = []
