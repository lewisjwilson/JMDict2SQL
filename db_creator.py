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

def insert_data(conn, data_list):

    sql = ''' INSERT INTO JMdict_e(ent_seq, k_ele_list, ke_inf, ke_pri, r_ele_list, reb,
                    re_nokanji, re_restr_list, re_inf, re_pri, sense_list)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.executemany(sql, data_list)
    conn.commit()
    return cur.lastrowid

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

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS stag_k (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS stag_r (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        sense_id INTEGER,
                                        value TEXT,

                                        FOREIGN KEY(sense_id) REFERENCES sense(id)

                                        ); """)

    create_table_sql_list.append(""" CREATE TABLE IF NOT EXISTS stag_k (
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
                                        value TEXT,
                                        lang TEXT,
                                        g_gend TEXT,
                                        g_type TEXT,
                                        pri TEXT,


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
