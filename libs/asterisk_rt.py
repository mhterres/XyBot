# -*- coding: utf-8 -*-

# asterisk_rt.py
# Asterisk Realtime Module
#
# Marcelo H. Terres <mhterres@mundoopensource.com.br>
# 2016-04-15
#

import datetime
import logging
import psycopg2
import psycopg2.extras

def getAsteriskRealtimeInformation(cfg,jid):

    dsn = 'dbname=%s host=%s user=%s password=%s' % (cfg.ast_db_name, cfg.ast_db_host, cfg.ast_db_user, cfg.ast_db_pwd)

    conn = psycopg2.connect(dsn)
    curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    sql = "SELECT name,callerid,%sjid,%sallow_call,%sallow_sms from %s where %sjid='%s';" % (cfg.ast_jid_field_prefix,cfg.ast_jid_field_prefix,cfg.ast_jid_field_prefix,cfg.ast_sip_table,cfg.ast_jid_field_prefix,jid)
    logging.debug(sql)

    try:

        curs.execute(sql,)

        if not curs.rowcount:
            logging.error("Can't find extension for jid %s - SQL: %s." % (jid,sql))
            data=[1,"Can't find the extension for your jid." ,"","","","",""]
            return data

    except:

        logging.error("Can't connect in Asterisk DB - SQL: %s." % sql)
        data=[1,"Can't connect in Asterisk DB.","","","","",""]
    else:

        row=curs.fetchone()
        name = row['name']
        callerid = row['callerid']
        callerid = row['callerid']
        allow_sms = row['xmpp_allow_sms']
        allow_call = row['xmpp_allow_call']
        data=[0,"",name,jid,callerid,allow_sms,allow_call]

    return data

