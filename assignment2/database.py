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


'''
Validate user login request based on username and password
'''
def checkUserCredentials(username, password):
    
    curs = openConnection().cursor()
    if username == "-":
        return None
    curs.callproc("checkuser")
    row = curs.fetchone()
    while row is not None:
        if row[1] == username and row[4] == password:
            userInfo = []
            for i in range(len(row)):
                userInfo.append(str(row[i]))
            openConnection().close()
            return userInfo
        row = curs.fetchone()
    openConnection().close()
    return None




'''
List all the associated events in the database for a given official
'''
def findEventsByOfficial(official_id):
    
    curs = openConnection().cursor()
    curs.callproc("findEventsOfficial",[official_id])
    row = curs.fetchone()
    event_db = []
    while row is not None:
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



'''
Find a list of events based on the searchString provided as parameter
See assignment description for search specification
'''
def findEventsByCriteria(searchString):

    searchString = searchString.replace("'","''")
    
    
    curs = openConnection().cursor()
    q1 = "select distinct(eventid), eventname, sportname, (select username from official where officialid = referee) as referee,\
        (select username from official where officialid = judge) as judge,(select username from official where officialid = medalgiver) as medalgiver "
    q2 = "from event e natural join sport left outer join official o on(o.officialid = e.referee or o.officialid = e.judge or o.officialid = e.medalgiver) \
        where lower(SPORTNAME) like lower('%{}%') or lower(EVENTNAME) like lower('%{}%') or lower(username) like lower('%{}%') order by sportname;".format(searchString,searchString,searchString)
    curs.execute(q1 + q2)
    row = curs.fetchone()
    event_db = []
    while row is not None:
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



'''
Add a new event
'''
def addEvent(event_name, sport, referee, judge, medal_giver):

    curs = openConnection().cursor()
    
    event_name = event_name.replace("'","''")
    
    # check invalid input
    curs.callproc("check_invalid_input",[sport,referee,judge,medal_giver])
    row = curs.fetchone()
    for i in range(len(row)):
        if row[i] is None:
            return False
    
    
    q2 = "begin; INSERT INTO EVENT (EVENTNAME,SPORTID,REFEREE,JUDGE,MEDALGIVER) VALUES "
    q3 = "('{}',(select SPORTID from SPORT where SPORTNAME = '{}'),(select OFFICIALID from OFFICIAL where USERNAME = '{}'),\
        (select OFFICIALID from OFFICIAL where USERNAME = '{}'),(select OFFICIALID from OFFICIAL where USERNAME = '{}')); commit;".format(event_name,sport,referee,judge,medal_giver)
    curs.execute(q2 + q3)
    
    openConnection().close()
    return True


'''
Update an existing event
'''
def updateEvent(event_id, event_name, sport, referee, judge, medal_giver):
    
    curs = openConnection().cursor()
    
    # check invalid input
    curs.callproc("check_invalid_input",[sport,referee,judge,medal_giver])
    row = curs.fetchone()
    for i in range(len(row)):
        if row[i] is None:
            return False
    
    # Convert input form
    event_name = event_name.replace("'","''")
    
    q2 = "begin; UPDATE EVENT SET "
    q3 = "EVENTNAME='{}',SPORTID=(select SPORTID from SPORT where SPORTNAME = '{}'),REFEREE=(select OFFICIALID from OFFICIAL where USERNAME = '{}'),\
        JUDGE=(select OFFICIALID from OFFICIAL where USERNAME = '{}'),MEDALGIVER=(select OFFICIALID from OFFICIAL where USERNAME = '{}') \
            WHERE EVENTID={};	commit;".format(event_name,sport,referee,judge,medal_giver,event_id)
    curs.execute(q2 + q3)
    openConnection().close()

    return True
    
