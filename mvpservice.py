from pprint import pprint
from flask import Flask, request, jsonify
import platform
import tempfile
import os
from mysql.connector import Error, MySQLConnection
from python_mysql_dbconfig import read_db_config
import db_connect_test
import socket

###############################################################
app = Flask(__name__)
host = socket.gethostname()

if platform.system() == 'Windows':
    port_num = 5000 # Free Port for local testing purposes
else:
    port_num = 80 # Standard HTTP Port on Cloud
###############################################################
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

###############################################################

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

###############################################################
@app.route("/")
def homepage():
    return f"""<h1>Welcome to the homepage</h1>
<code>
        {request}<br>
<hr>
        {request.headers}<br>
</code>
    <ol>
      <li> <a href="upload">upload</a></li>
    </ol>
    """
###############################

def name():
    return "pic"

NAME = 'pic'

###############################################################

@app.route("/upload")
def upload():
    return homepage_content()

###############################


def allowed_file(filename):
    pass

###############################################################

# class Edge(object):
#
#      def __init(self, start, finishm confidion, action):
#         self.start = start
#         self.finish = finition
#         self condtion = condifion
#         self.action = action
#         super(Edge, self).__init()
#
#     def canSwitch(self, input):
#         if self.condtion(input):
#             self.action()
#             return self.finish
# def FSM(dict):
#     def __init__(self):
#         super(FS)
#
# def Edge(0, 1000)
###############################################################
def homepage_content():
  return f"""
        <div class="container">
          
          <hr>
          <p><span class="error">* required field</span></p>
          
          <form action="submit", method="post", enctype="multipart/form-data">
          
              <input type="file" name={NAME} accept="image/* ">* <br><br><br>
    
              Nickname*:<br>
              <input type="text" name="Nickname" title="Select New if New nickname">
    
              <p>New Nickname? First Time here?</p>
              <input type="checkbox" name="new" value="yes" title="Select if new"> Yes <br><br>
                    
              <label for="Comment">Comment</label><span class="error"> <br>
              <textarea id="msg" name="msg" placeholder="Image Comments..." style="height:100px"></textarea>
            
              <input value="Post" type="submit">
            
          </form>
        </div> 
    """
###############################################################


def redirect(page=host, port=port_num):

    return f"""
    <meta http-equiv="Refresh" content="0; url=http:{page}:{port}" />
    """

###############################################################

def completeDb(data):
    author = data.get('Nickname')
    if data.get('new'):
        if db_connect_test.getUserId(author):
            raise InvalidUsage(f"{author} Nickname is not New and already Exists")
        db_connect_test.createNewId(author)
    author_id = db_connect_test.getUserId(author)
    if not author_id:
        raise InvalidUsage(f"Provided nickname: {author}, not found in database")
    author_id = author_id[0]
    filepath = data.get('filepath')
    if filepath:
        ref_data_id = db_connect_test.createNewDataRecord(filepath)

    comment = data.get('msg')
    if comment:
        data_id = db_connect_test.createNewDataRecord(comment, "comment")
    else:
        data_id = ref_data_id

    if data_id and ref_data_id and author_id:
        db_connect_test.createNewRecord(author_id, data_id, ref_data_id)
    else:
        raise InvalidUsage(f"Missing paramater {data}")

    pprint(data)

@app.route("/submit", methods=['GET','POST'])
def receivedata():
    filename = tempfile.mktemp() # [suffix = ''[, prefix = 'tmp'[, dir = None]]])

    if request.method == 'POST':

        data = request.form.to_dict()

        # check if the post request has the file part
        if NAME not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files[NAME]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file: # and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename, file_extension = os.path.splitext(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("Name of file uploaded: ", filename)

            # if platform.system() == 'Windows':
            #     filenamepath = ["C:/Users/Emil/Downloads/", filename,'USER_ID', file_extension]
            # else:
            #     filenamepath = ["/home/ec2-user/mountstorage/", filename,'USER_ID', file_extension]
            # filepath = "".join(filenamepath)


            filepath = tempfile.mktemp(suffix=file_extension) # [, prefix = 'tmp'[, dir = None]]])
            print("File Path to save: ", filepath)
            file.save(filepath)
            data['filepath'] = filepath
            completeDb(data)
            return redirect()
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


###############################################################
@app.route("/ha")
def hello1():
    return "<h1>Not Much Going On Here, but ha</h1>"
###############################################################
@app.route("/hi")
def hello2():
    return "<h1>Not Much Going On Here but hi</h1>"
###############################################################





###############################################################
'''
CONNECTIONS 

Original EC2
Use in Browser: Public IP: http://3.88.217.30/
Use in Code: Private IP: 172.31.90.152

New EC2: webservice2
Use in Browser: Public IP: http://18.205.29.255/
Use in Code: Private IP: 172.31.87.215

New EC2: webservice2
Use in Browser: Public IP: http://3.92.175.47/
Use in Code: Private IP: 172.31.87.59

'''
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
###############################################################
# DISCONNECT FROM CLOUD DB

def close(conn):
    if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.')
###############################################################
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

###############################################################
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

# host = socket.gethostname()

app.run(host=host, port=port_num)




########################################################################################################################
#MAIN

#
# if input("Do you have a user id? y/n: ").lower() == 'y'.strip():
#     author = getAuthor()  # returns tuple (author_id, nickname)
# elif input("Create new ID? y/n: ").lower() == 'y'.strip():
#     author = createNewId()  # returns tuple (author_id, nickname)
#
# if input("Add new image? y/n: ").lower() == 'y'.strip():
#
#
#     print("Need Function")
