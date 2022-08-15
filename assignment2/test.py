#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    userid = "postgres"
    passwd = "123456"
    myHost = "localhost"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn

def checkUserCredentials(username, password):
    
    curs = openConnection().cursor()
    
    curs.callproc("checkuser")
    row = curs.fetchone()
    print(row)
    openConnection().close()
    return 

def findEventsByOfficial(official_id):
    
    curs = openConnection().cursor()
    curs.callproc("findEventsOfficial",[official_id])
    row = curs.fetchone()
    event_db = []
    while row is not None:
        print(row)
        event_db.append(row)
        row = curs.fetchone()

    event_list = [{
        'event_id': str(row[0]),
        'event_name': row[1],
        'sport': row[2],
        'referee': row[3],
        'judge': row[4],
        'medal_giver': row[5]
    } for row in event_db]
    openConnection().close()
    return event_list
    

findEventsByOfficial(5)