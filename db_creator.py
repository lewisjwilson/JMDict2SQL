#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_data(ent_seq, k_ele_list, keb, ke_inf, ke_pri, r_ele_list, reb, re_nokanji, re_restr_list, re_inf, re_pri):
    conn = create_connection(r"sqlite.db")

    sql = ''' INSERT INTO JMdict_e(ent_seq, k_ele_list, keb, ke_inf, ke_pri,
                r_ele_list, reb, re_nokanji, re_restr_list, re_inf, re_pri)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (ent_seq, "k_ele_fix", keb, ke_inf, ke_pri, "r_ele_fix", reb,
                        re_nokanji, "re_restr_fix", re_inf, re_pri))
    conn.commit()
    return cur.lastrowid

def create_database():
    database = r"sqlite.db"

    sql_create_main_table = """ CREATE TABLE IF NOT EXISTS JMdict_e (
                                        ent_seq TEXT PRIMARY KEY,
                                        k_ele_list TEXT,
                                        keb TEXT,
                                        ke_inf TEXT,
                                        ke_pri TEXT,
                                        r_ele_list TEXT,
                                        reb TEXT,
                                        re_nokanji TEXT,
                                        re_restr_list TEXT,
                                        re_inf TEXT,
                                        re_pri TEXT
                                                                            ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_main_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
