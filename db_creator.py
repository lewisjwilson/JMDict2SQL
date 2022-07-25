#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_data(conn, table_name, data_list):

    sql = insert_data_sql(table_name)

    if(sql == "TABLE_NOT_FOUND"):
        print("Table: '" + table_name + "' does not exist. Exiting program.")
        exit()

    cur = conn.cursor()
    cur.executemany(sql, data_list)
    conn.commit()
    return cur.lastrowid


# function for changing sql based on table inserting into
def insert_data_sql(table_name):
    return{
        'entry': ''' INSERT INTO entry(id) VALUES(?) ''',
        # ------------------------------kanji tables---------------------------
        'k_ele': ''' INSERT INTO kanji(entry_id, value) VALUES(?, ?) ''',
        'ke_inf': ''' INSERT INTO kanji_tags(kanji_id, value) VALUES(?, ?) ''',
        'ke_pri': ''' INSERT INTO kanji_common(kanji_id, value) VALUES(?, ?) ''',
        # ------------------------------kana tables---------------------------------
        'r_ele': ''' INSERT INTO kana(entry_id, value, no_kanji) VALUES(?, ?, ?) ''',
        're_restr': ''' INSERT INTO kana_applies_to_kanji(kana_id, value) VALUES(?, ?) ''',
        're_inf': ''' INSERT INTO kana_tags(kana_id, value) VALUES(?, ?) ''',
        're_pri': ''' INSERT INTO kana_common(kana_id, value) VALUES(?, ?) ''',
        # ------------------------------senses tables---------------------------------
        'sense': ''' INSERT INTO sense(entry_id) VALUES(?) ''',
        'stagk': ''' INSERT INTO sense_applies_to_kanji(sense_id, value) VALUES(?, ?) ''',
        'stagr': ''' INSERT INTO sense_applies_to_kana(sense_id, value) VALUES(?, ?) ''',
        'pos': ''' INSERT INTO part_of_speech(sense_id, value) VALUES(?, ?) ''',
        'xref': ''' INSERT INTO cross_reference(sense_id, value) VALUES(?, ?) ''',
        'ant': ''' INSERT INTO antonym(sense_id, value) VALUES(?, ?) ''',
        'field': ''' INSERT INTO field(sense_id, value) VALUES(?, ?) ''',
        'misc': ''' INSERT INTO misc(sense_id, value) VALUES(?, ?) ''',
        'lsource': ''' INSERT INTO lang_source(sense_id, origin, lang, type, wasei) VALUES(?, ?, ?, ?, ?) ''',
        'dial': ''' INSERT INTO dialect(sense_id, value) VALUES(?, ?) ''',
        'gloss': ''' INSERT INTO definition(sense_id, value, lang, type) VALUES(?, ?, ?, ?) ''',
        's_inf': ''' INSERT INTO sense_info(sense_id, value) VALUES(?, ?) '''

    }.get(table_name, "TABLE_NOT_FOUND")


def create_database():

    database = r"JMdict_e.db"

    create_table_sql_list = []

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS entry (
                                        id INTEGER PRIMARY KEY); """)

    # ------------------------------kanji tables---------------------------------

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS kanji (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        entry_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(entry_id) REFERENCES entry(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS kanji_tags (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        kanji_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(kanji_id) REFERENCES kanji(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS kanji_common (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        kanji_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(kanji_id) REFERENCES kanji(id)

                                        ); """)

    # ------------------------------kana tables---------------------------------

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS kana (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        entry_id INTEGER,
                                        value TEXT,
                                        no_kanji INTEGER,

                                        FOREIGN KEY(entry_id) REFERENCES entry(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS kana_applies_to_kanji (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        kana_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(kana_id) REFERENCES kana(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS kana_tags (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        kana_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(kana_id) REFERENCES kana(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS kana_common (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        kana_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(kana_id) REFERENCES kana(id)

                                        ); """)

    # ------------------------------senses tables---------------------------------

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS sense (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        entry_id INTEGER,

                                        FOREIGN KEY(entry_id) REFERENCES entry(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS sense_applies_to_kanji (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS sense_applies_to_kana (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS part_of_speech (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS cross_reference (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS antonym (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS field (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS misc (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS sense_info (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS lang_source (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        origin text,
                                        lang TEXT,
                                        type TEXT,
                                        wasei INTEGER,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS dialect (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS definition (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,
                                        lang TEXT,
                                        type TEXT,


                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:

        for table in create_table_sql_list:
            # create projects table
            create_table(conn, table)

        # clear list from memory
        create_table_sql_list = []

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
