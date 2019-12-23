from mysql.connector import Error, MySQLConnection
from python_mysql_dbconfig import read_db_config

########################################################################################################################
# FUNCTIONS
######################################################################
# CONNECT TO CLOUD DB

def connect():
    db_config = read_db_config()
    conn = None
    try:
        print("Connecting to MySQL DB...")
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print("Connected established.")
        else:
            print("Connection failed.")

    except Error as error:
        print(error)

    return conn
######################################################################
# DISCONNECT FROM CLOUD DB

def close(conn):
    if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')

######################################################################
# CREATE NEW USER
def getUserId(name):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * from `mvp`.`author` WHERE nickname  = %s;"
    cursor.execute(query, (name,))
    user = None
    for user in cursor:
        break
    cursor.close()
    close(conn)
    return user
######################################################################
def createNewId(name):
    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO `mvp`.`author` (nickname) VALUES (%s);"
    cursor.execute(query, (name,))
    conn.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    close(conn)
    return lastrowid
######################################################################
def createNewDataRecord(path, type_id = 'image'):
    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO `mvp`.`data`  (type_id, data) VALUES (%s, %s);"
    cursor.execute(query, (type_id, path))
    conn.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    close(conn)
    return lastrowid

######################################################################
def getDataRecord(data_id):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * from `mvp`.`data` WHERE data_id = %s;"
    cursor.execute(query, (data_id,))
    path = None
    for path in cursor:
        break
    cursor.close()
    close(conn)
    return path
######################################################################
def getRecord(record_id):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * from `mvp`.`record` WHERE record_id = %s;"
    cursor.execute(query, (record_id,) )
    record = None
    for record in cursor:
        break
    cursor.close()
    close(conn)
    return record
######################################################################
def createNewRecord( author_id, data_id, ref_data_id=None):
    ref_data_id = ref_data_id or data_id
    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO `mvp`.`record`  (author_id, data_id, ref_data_id) VALUES (%s, %s, %s);"
    cursor.execute(query, (author_id, data_id, ref_data_id))
    conn.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    close(conn)
    return lastrowid


########################################################################################################################
# MAIN


if __name__ == "__main__":
    author = None
    if input("Do you have a user id? y/n: ").lower() == 'y'.strip():
        while not author:
            name = input("What is your user nickname? ")
            author = getUserId(name)  # returns tuple (author_id, nickname)
            if author:
                print(f"User {name} has been found {author}")
            else:
                print(f"User {name} doesn't exist")

    if author is None and input("Create new ID? y/n: ").lower() == 'y'.strip():
        name = input("Create nickname: ")
        user = getUserId(name)
        if user:
            print(f"User {user} already exists")
        else:
            author = createNewId(name)  # returns tuple (author_id, nickname)
            author = getUserId(name)
    if author:
        print(f"Congrats, new nickname created: {author}")
    if author and input("Add new image? y/n: ").lower() == 'y'.strip():
        path = input("What is a path of your image file?").lower()
        data_id = createNewDataRecord(path)
        print(f"Need Function {path} {data_id}")
        check_record = getDataRecord(data_id)
        print (f"We have added {check_record}")
        author_id = author[0]
        record_id = createNewRecord(author_id, data_id, ref_data_id=None)


        #check
        record2Check = getRecord(record_id)
        print(f"DB has benn completed {record2Check}")




