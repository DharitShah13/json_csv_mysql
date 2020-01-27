import pymysql

f = open(r"students.csv","r")
fString = f.read()

flist = []
for line in fString.split('\n'):
    flist.append(line.split(','))

db = pymysql.connect("localhost","root","root","redhat")

cursor = db.cursor()

cursor.execute("Drop TABLE IF EXISTS STUDENTS")

FIRST_NAME = flist[0][0];LAST_NAME = flist[0][1];AGE = flist[0][2];GENDER = flist[0][3];DEGREE = flist[0][4]

queryCreateStudentTabke = """CREATE TABLE STUDENTS( 
                              {} varchar(255) not null,
                              {} varchar(255) not null,
                              {} int,
                              {} char(1),
                              {} char(2)
                              )""".format(FIRST_NAME,LAST_NAME,AGE,GENDER,DEGREE)

cursor.execute(queryCreateStudentTabke)

del flist[0]

rows = ''
for i in range(len(flist) - 1):
    rows += "('{}','{}','{}','{}','{}')".format(flist[i][0],flist[i][1],flist[i][2],flist[i][3],flist[i][4])
    if i != len(flist) - 2:
        rows += ','

queryInsert = "INSERT INTO STUDENTS VALUES" + rows

try:
    cursor.execute(queryInsert)
    db.commit()
except:
    db.rollback()

db.close()
