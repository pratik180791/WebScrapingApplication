import sqlite3

# Open database connection
try:
    conn = sqlite3.connect('scraping.db')
    cur=conn.cursor()
    print("Opened database successfully");
except sqlite3:
            print("Error in connecting db")


def checkTable():
    try:
        cursor = cur.execute("SELECT name FROM login WHERE type='table' AND name='PRATIK'")
        val=cursor.fetchall()
        return val
    except Exception as e:
        print("Exception in check")

def createTable():
    try:

        conn.execute('DROP TABLE IF EXISTS PRATIK')
        conn.execute('CREATE TABLE PRATIK(USERNAME TEXT NOT NULL, PASSWORD TEXT PRIMARY KEY NOT NULL);');
        print('Admin Table created')
        conn.execute("INSERT INTO PRATIK(USERNAME,PASSWORD) VALUES('admin','admin');")
        conn.commit();
    except Exception as e:
                    print("Exception Occured while creating a table"+str(e))

def loginCheck(username,password):
    try:



        cursor = cur.execute("SELECT count(1) FROM PRATIK where username='"+username+"' and password='"+password+"'")
        i=cursor.fetchone()
        #print(i[0])

        if(i[0]>0):
                return 'Pass'
        else:
             return 'False'
    except Exception as e:
                    print("Exception Occured while Login check a table"+str(e))

    #return 'Pass'
def insertContact(name, phone):
    try:
            conn.execute("INSERT INTO PRATIK(NAME,PHONE) VALUES('" + name.title() + "', '" + phone + "');")
          #  conn.commit();
            print("Insert executed for contact "+name.title())
    except Exception as e:
                    conn.rollback()
                    print("Exception Occured while inserting in table "+str(e))

def deleteContactDB(name):
    try:
        ct1=cur.execute("DELETE FROM PRATIK WHERE NAME = '" + name + "'")
        print("Deleted contact "+ name+" succesfully")
    except Exception as e:
                    conn.rollback()
                    print("Exception Occurred while deleting from table "+str(e))
