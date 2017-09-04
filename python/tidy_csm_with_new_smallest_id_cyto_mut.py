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

  sql['get_ags_csm'] = """select s.id_sample, csm.ID_CYTO_MUT, csm.ID_CSM , ags1.id_ags from CYTO_SAMPLE_MUTATION csm, ags1 , sample s 
  where ags1.ID_AGS = csm.ID_AGS and ags1.id_sample = s.id_sample
  and csm.ID_CYTO_MUT = :id order by csm.id_cyto_mut"""


  sql['get_duplicate_cyto'] = """select * from 
  (select t2.CDS_MUT_SYNTAX, LISTAGG(t.id_cyto_mut, ',') WITHIN GROUP (ORDER BY t2.CDS_MUT_SYNTAX) ids from
  (select distinct c.ID_CYTO_MUT from CYTO_MUTATION c, CYTO_SAMPLE_MUTATION csm
  where c.ID_CYTO_MUT = csm.ID_CYTO_MUT
  and c.CYTO_MUT_INHERITANCE_TYPE = 41) t,CYTO_MUTATION t2
  where t.ID_CYTO_MUT = t2.ID_CYTO_MUT and t2.CYTO_MUT_INHERITANCE_TYPE = 41
  group by t2.CDS_MUT_SYNTAX order by ids) t3 where t3.IDS like '%,%'"""


if __name__ == "__main__":
    try:
        conn = connectDb()
        cur = conn.cursor()
        addQuery()
        cur.execute(sql['get_duplicate_cyto'])
        query = cur.fetchall()
        for i in query: # EML4{ENST00000318522}:r.1_1903_ALK{ENST00000389048}:r.4080_6220    1065,1128
            ids = i[1]
            l = ids.split(',')
            l.sort(key=int)
            good_id = l.pop(0)
            cur.execute(sql['get_ags_csm'],{'id':good_id})
            res = cur.fetchone()
            (id_sample, id_cyto_mut, id_csm, id_ags) = (res[0],res[1],res[2],res[3]) 
            #print("-----",id_sample,id_cyto_mut,id_csm);
            for bad_id in  l:

                    cur.execute(sql['get_ags_csm'],{'id':bad_id})
                    res1 = cur.fetchone()
                    (id_sample_bad, id_cyto_mut_bad, id_csm_bad, id_ags_bad) = (res1[0],res1[1],res1[2],res1[3]) 
                    #print  (id_sample_bad, id_cyto_mut_bad, id_csm_bad, id_ags_bad);
                    if id_sample != id_sample_bad:
                        #print("Update cyto_sample_mutation set id_cyto_mut = ",id_cyto_mut," where id_csm = ", id_csm_bad, " and id_ags = ", id_ags_bad,";")
                        print("Update cyto_sample_mutation set id_cyto_mut = ",id_cyto_mut," where id_cyto_mut = ", id_cyto_mut_bad,";")
                        print("delete from cyto_mutation_temp1 where id_cyto_mut = ",id_cyto_mut_bad,";")
                    else:
                        print("Keep")
    except :

        print("Fail to connect database")

    else:
        pass



