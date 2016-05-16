import sqlite3   #library that we use to talk to sql database

conn = sqlite3.connect('emaildb.sqlite') # create connection object that connects to a file
cur = conn.cursor()  # sets up a cursor to send through commands

cur.execute('''
DROP TABLE IF EXISTS Counts''') # call execute method

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''') # create table Counts

fname = raw_input('Enter file name: ')  # prompt for file name
if ( len(fname) < 1 ) : fname = 'mbox-short.txt'
fh = open(fname)  # file handler
for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split()
    email = pieces[1]
    print email
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email, )) # ? is a placeholder
    row = cur.fetchone() # brings us back 1 row in memory and gives it as a list
#Below code checks to see if the email already exists in the database, if not, 
#it inserts a new row. if it does exist, it updates the count.    
    if row is None:
        cur.execute('''INSERT INTO Counts (email, count) 
                VALUES ( ?, 1 )''', ( email, ) )
    else : 
        cur.execute('UPDATE Counts SET count=count+1 WHERE email = ?', 
            (email, ))
    # This statement commits outstanding changes to disk each 
    # time through the loop - the program can be made faster 
    # by moving the commit so it runs only after the loop completes
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

print
print "Counts:"
for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

cur.close()

