import urllib
import sqlite3
import json
import time
import ssl

#geocoding API
serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"

# Deal with SSL certificate anomalies Python > 2.7
# scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
scontext = None

#create a file handle, a connection,
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()  # use cursor to create a subconnection

# use SQL to create 2 columns in table Locations; execute SQL
cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

#Retrieve from API; open input data
fh = open("where.data") #where.data is the input; data that came from survey
count = 0
for line in fh:
    if count > 200 : break
    address = line.strip() # address is the entire line
    print ''  #buffer forces it to what we want it to be if unicode use logical key in WHERE clause
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", (buffer(address), ))

    try:
        data = cur.fetchone()[0] # gives 1 row, which is a list, and gets 1st column position 0
        print "Found in database ",address
        continue
    except:
        pass

    print 'Resolving', address
    url = serviceurl + urllib.urlencode({"sensor":"false", "address": address})
    print 'Retrieving', url
    uh = urllib.urlopen(url, context=scontext)
    data = uh.read()
    print 'Retrieved',len(data),'characters',data[:20].replace('\n',' ')
    count = count + 1
    try: #check to see if you got good data or not
        js = json.loads(str(data))
        # print js  # We print in case unicode causes an error
    except: 
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') : 
        print '==== Failure To Retrieve ===='
        print data
        break
# geodata is the json data
    cur.execute('''INSERT INTO Locations (address, geodata) 
            VALUES ( ?, ? )''', ( buffer(address),buffer(data) ) ) # 0 is address and 1 is data
    conn.commit() # now, actually write to the database; puts file in disk
    time.sleep(1)

print "Run geodump.py to read the data from the database so you can visualize it on a map."
