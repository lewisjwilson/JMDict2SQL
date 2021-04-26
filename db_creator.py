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
        'entry': ''' INSERT INTO entry(ent_seq) VALUES(?) ''',
        # ------------------------------k_ele tables---------------------------------
        'k_ele': ''' INSERT INTO k_ele(ent_seq, keb) VALUES(?, ?) ''',
        'ke_inf': ''' INSERT INTO ke_inf(k_ele_id, value) VALUES(?, ?) ''',
        'ke_pri': ''' INSERT INTO ke_pri(k_ele_id, value) VALUES(?, ?) ''',
        # ------------------------------r_ele tables---------------------------------
        'r_ele': ''' INSERT INTO r_ele(ent_seq, reb, no_kanji) VALUES(?, ?, ?) ''',
        're_restr': ''' INSERT INTO re_restr(r_ele_id, value) VALUES(?, ?) ''',
        're_inf': ''' INSERT INTO re_inf(r_ele_id, value) VALUES(?, ?) ''',
        're_pri': ''' INSERT INTO re_pri(r_ele_id, value) VALUES(?, ?) ''',
        # ------------------------------senses tables---------------------------------
        'sense': ''' INSERT INTO sense(ent_seq) VALUES(?) ''',
        'stagk': ''' INSERT INTO stagk(sense_id, value) VALUES(?, ?) ''',
        'stagr': ''' INSERT INTO stagr(sense_id, value) VALUES(?, ?) ''',
        'pos': ''' INSERT INTO pos(sense_id, value) VALUES(?, ?) ''',
        'xref': ''' INSERT INTO xref(sense_id, value) VALUES(?, ?) ''',
        'ant': ''' INSERT INTO ant(sense_id, value) VALUES(?, ?) ''',
        'field': ''' INSERT INTO field(sense_id, value) VALUES(?, ?) ''',
        'misc': ''' INSERT INTO misc(sense_id, value) VALUES(?, ?) ''',
        'lsource': ''' INSERT INTO lsource(sense_id, origin, lang, ls_type, ls_wasei) VALUES(?, ?, ?, ?, ?) ''',
        'dial': ''' INSERT INTO dial(sense_id, value) VALUES(?, ?) ''',
        'gloss': ''' INSERT INTO gloss(sense_id, definition, lang, g_gend, g_type) VALUES(?, ?, ?, ?, ?) ''',
        's_inf': ''' INSERT INTO s_inf(sense_id, value) VALUES(?, ?) ''',

        'pri': ''' INSERT INTO pri(gloss_id, value) VALUES(?, ?) '''

    }.get(table_name, "TABLE_NOT_FOUND")

def create_database():
    database = r"sqlite.db"

    create_table_sql_list = []

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS entry (
                                        ent_seq INTEGER PRIMARY KEY); """)


    # ------------------------------k_ele tables---------------------------------


    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS k_ele (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ent_seq INTEGER,
                                        keb TEXT,

                                        FOREIGN KEY(ent_seq) REFERENCES entry(ent_seq)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS ke_inf (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        k_ele_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(k_ele_id) REFERENCES k_ele(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS ke_pri (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        k_ele_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(k_ele_id) REFERENCES k_ele(id)

                                        ); """)


    # ------------------------------r_ele tables---------------------------------


    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS r_ele (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ent_seq INTEGER,
                                        reb TEXT,
                                        no_kanji INTEGER,

                                        FOREIGN KEY(ent_seq) REFERENCES entry(ent_seq)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS re_restr (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        r_ele_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(r_ele_id) REFERENCES r_ele(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS re_inf (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        r_ele_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(r_ele_id) REFERENCES r_ele(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS re_pri (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        r_ele_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(r_ele_id) REFERENCES r_ele(id)

                                        ); """)


    # ------------------------------senses tables---------------------------------

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS sense (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ent_seq INTEGER,

                                        FOREIGN KEY(ent_seq) REFERENCES entry(ent_seq)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS stagk (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS stagr (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS pos (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS xref (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS ant (
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

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS s_inf (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS lsource (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        origin text,
                                        lang TEXT,
                                        ls_type TEXT,
                                        ls_wasei TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS dial (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS gloss (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        definition TEXT,
                                        lang TEXT,
                                        g_gend TEXT,
                                        g_type TEXT,
                                        pri TEXT,


                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)




    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS pri (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        gloss_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(gloss_id) REFERENCES gloss(id)

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
