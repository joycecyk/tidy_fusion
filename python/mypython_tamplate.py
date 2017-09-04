#!/usr/bin/env python3

"""Test your cx_Oracle installation on cgpbar server."""
import cx_Oracle, getpass

# Import Oracle database module.
import csv
import argparse,textwrap


sql = {}

def connectDb():

    """Test your cx_Oracle installation."""

    # Connect to Oracle and test
    #con = cx_Oracle.connect ('coste_owner/cosmic1234@cost')
    con = cx_Oracle.connect ('coste_owner/cosmic1234@cost')

    print("Success to connect db: "+ con.version)
    return con




def addQuery():
  sql['insert_xxx'] = """insert into sample_struc_mutation ( ID_AGS, ID_STRUC_MUT, ID_MUT_SOMATIC_STATUS, ID_MUT_VERIF_STATUS, ID_SSM) values (:id_ags,:id_struc_mut,:mutation_status,51,ssm_seq.nextval)"""


  sql['get_xxxx'] = "select struc_seq.currval as id_struc_mut from dual"


if __name__ == "__main__":
    try:
        global cur
        conn = connectDb()
        cur = conn.cursor()
        addQuery()

    except:

        print("Fail to connect database")

    else:
        pass



