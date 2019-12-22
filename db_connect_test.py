from mysql.connector import Error, MySQLConnection
from python_mysql_dbconfig import read_db_config
# import cv2
import numpy as np
import _pickle as cPickle
########################################################################################################################
# FUNCTIONS

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

# DISCONNECT FROM CLOUD DB


def close(conn):
    if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')

# CHECK EXISTING USER


def getAuthor():
    conn = connect()
    cursor = conn.cursor()

    while True:
        name = (input("What is your user nickname? "),)
        query = ("SELECT * from `mvp`.`author`"
                 "WHERE nickname  = (%s)")
        cursor.execute(query, name)
        for match in cursor:
            print("Welcome", match[1])
            cursor.close()
            close(conn)
            return match
        if input("No Id Found. Try Again? y/n: ").lower() == 'y'.strip():
            continue
        elif input("Create new ID? y/n:  ").lower() == 'y'.strip():
            createNewId()
            break
        else:
            break
    cursor.close()
    close(conn)

# CREATE NEW USER


def createNewId():
    conn = connect()
    cursor = conn.cursor()
    while True:
        name = (input("Create nickname: "),)
        query = ("SELECT * from `mvp`.`author` WHERE nickname  = (%s)")
        cursor.execute(query, name)
        match = None
        for match in cursor:
            print("ID Exists, try again")
        if not match:
            query = ("INSERT INTO `mvp`.`author` (nickname) VALUES (%s)")
            cursor.execute(query, name)
            conn.commit()
            query = ("SELECT * from `mvp`.`author` WHERE nickname  = (%s)")
            cursor.execute(query, name)
            for match in cursor:
                print("Congrats, new nickname created: ", match[1])
                return match
            break
    cursor.close()
    close(conn)

# ADD IMAGE


# def addImg():
#
#     #  ./Data/emilfine2.jpg
#     #  ./Data/test.jpg
#     conn = connect()
#     cursor = conn.cursor()
#
#     imgpath = input("Enter Path: ")
#     # img_gray = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)  # Load Image in Grayscale
#     query = ("INSERT INTO `mvp`.`data` (type_id, data) VALUES (%s, %s);")
#     cursor.execute(query, ("image", cPickle.dumps(img_gray)))
#     conn.commit()
#
#     query = ("SELECT LAST_INSERT_ID()")
#     cursor.execute(query)
#
#     for ID in cursor:
#         print(ID)
#
#     cursor.close()
#     close(conn)



########################################################################################################################
# MAIN

# img_gray = cv2.imread('./Data/test.jpg', cv2.IMREAD_GRAYSCALE)  # Load Image in Grayscale

# SAVE METHOD
# np.savetxt(io, img_gray)
# s = io.getvalue()

# STRING METHOD
# a = str(img_gray)

#PICKLE METHOD
# s = cPickle.dumps(img_gray)
# a = cPickle.loads(s)
#
# test = np.array_repr(img_gray)
# # print(len(test))
# print("img.shape: \n",img_gray.shape)
# print("repr(img): \n", test)


# a = np.array(test)
# print(len(test))


if input("Do you have a user id? y/n: ").lower() == 'y'.strip():
    author = getAuthor()  # returns tuple (author_id, nickname)
elif input("Create new ID? y/n: ").lower() == 'y'.strip():
    author = createNewId()  # returns tuple (author_id, nickname)

if input("Add new image? y/n: ").lower() == 'y'.strip():
    # imgData = addImg()
    print("Need Function")



