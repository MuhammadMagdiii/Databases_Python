import sqlite3
import json
import codecs

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations') #retrieve all rows
fhand = codecs.open('where.js','w', "utf-8") # open where.js and write utf character set
fhand.write("myData = [\n")  # write some json
count = 0
for row in cur :  #cursor keeps track; row is an iteration variable
    data = str(row[1])  # row is a 2-dim array; 0 is address and 1 is the actual data
    try: js = json.loads(str(data))
    except: continue

    if not('status' in js and js['status'] == 'OK') : continue # check status

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'","")
    try :
        print where, lat, lng

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']" #print out lat, long, and location
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print count, "records written to where.js"
print "Open where.html to view the data in a browser"

