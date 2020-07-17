import cx_Oracle as cx
import pymssql as mss
import pyhdb as hdb
import logging

logging.basicConfig(level=logging.ERROR, filename='erp.txt',
                    format='%(asctime)s :: %(funcName)s :: %(levelname)s :: %(message)s')


# Oracle connection
class OracleConn():
    def query(sql):
        db = cx.connect('INSITEQT2/KsMesDB_ht89@10.160.2.19:1521/mesora')
        cur = db.cursor()
        try:
            cur.execute(sql)
            results = cur.fetchall()

        except:
            logging.error("Error: unable to fetch data")
        cur.close()
        db.close()
        return results

    def exec(sql):
        db = cx.connect('INSITEQT2/KsMesDB_ht89@10.160.2.19:1521/mesora')
        cur = db.cursor()
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

        cur.close()
        db.close()


# Sqlserver connection
class MssConn():
    def query(sql):
        db = mss.connect('10.160.1.13', 'sa', 'ksxtDB', 'ERPBASE')
        cur = db.cursor()
        try:
            cur.execute(sql)
            results = cur.fetchall()

        except:
            logging.error("Error: unable to fetch data")
        cur.close()
        db.close()
        return results

    def exec(sql):
        db = mss.connect('10.160.1.13', 'sa', 'ksxtDB', 'ERPBASE')
        cur = db.cursor()
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

        cur.close()
        db.close()


# SapHana connection
class HanaConn():
    def query(sql):
        db = hdb.connect('10.160.2.20', '30015', 'WIP', 'Sap12345')
        cur = db.cursor()
        try:
            cur.execute(sql)
            results = cur.fetchall()
        except:
            logging.error("Error: unable to fetch data")

        cur.close()
        # db.close()
        return results

    def exec(sql):
        db = hdb.connect('10.160.2.20', '30015', 'WIP', 'Sap12345')
        cur = db.cursor()
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

        cur.close()
        db.close()
