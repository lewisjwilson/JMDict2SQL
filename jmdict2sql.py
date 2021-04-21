#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
import xml.etree.ElementTree as ET

tree = ET.parse('JMdict_e')
root = tree.getroot() #root = <JMDict>


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

def insert_data(conn, data):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO main(data)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def main():
    database = r"sqlite.db"

    sql_create_main_table = """ CREATE TABLE IF NOT EXISTS main (
                                        id integer PRIMARY KEY,
                                        data text NOT NULL
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
