from flask import Flask, request
import platform
import tempfile
import os
from mysql.connector import Error, MySQLConnection
from python_mysql_dbconfig import read_db_config


app = Flask(__name__)


@app.route("/")
def homepage():
    return f"""<h1>Welcome to the homepage</h1>
<code>
        {request}<br>
<hr>
        {request.headers}<br>
<hr>
        {request.data}
</code>
    <ol>
      <li> <a href="upload">upload</a></li>
      <li> <a href="hi">say hi</a></li>
    </ol>
    """
def name():
    return "pic"

NAME = 'pic'

@app.route("/upload")
def upload():
    return f"""
<div class="container">
  <hr><h3>Contact Us: </h3><hr><p></p>  <p><span class="error">* required field</span></p>
  <form action="submit", method="post", enctype="multipart/form-data">
  
  <input type="file" name={NAME} accept="image/* ">

    <label for="fname">First Name</label>
    <input id="fname" name="firstname" placeholder="Your name.." type="text">

    <label for="lname">Last Name</label>
    <input id="lname" name="lastname" placeholder="Your last name.." type="text">

    <label for="country">Country</label>
    <select id="country" name="country">
      <option value="australia" selected="selected">Australia</option>
      <option value="canada">Canada</option>
      <option value="usa">USA</option>
    </select>

    <label for="subject">Subject</label><span class="error">*
    <textarea id="subject" name="subject" placeholder="What are looking for?" style="height:40px"></textarea>

    <label for="Message">Message</label><span class="error">*
    <textarea id="msg" name="msg" placeholder="How can we help you today?" style="height:100px"></textarea>

    <input value="Submit" type="submit">

  </form>
</div> 
    """


def allowed_file(filename):
    pass


@app.route("/submit", methods=['GET','POST'])
def receivedata():
    filename = tempfile.mktemp() # [suffix = ''[, prefix = 'tmp'[, dir = None]]])

    if request.method == 'POST':
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
            return f"""
                <hr>
                save = {filepath}
                <hr>
            """
            return redirect(url_for('uploaded_file',
                                    filename=filepath))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    
    files = request.files
    return f"""<code>
        {request}<br>
<hr>
        {request.headers}<br>
<hr>
        {files}<br>
</code>
"""

@app.route("/ha")
def hello1():
    return "<h1>Not Much Going On Here, but ha</h1>"

@app.route("/hi")
def hello2():
    return "<h1>Not Much Going On Here but hi</h1>"

if platform.system() == 'Windows':
    app.run(host='0.0.0.0', port=5000)
else:
    app.run(host='172.31.87.59', port=80)

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
###############################################################
# ADD IMAGE


def addImg():
    return
    #  ./Data/emilfine2.jpg
    #  ./Data/test.jpg
    # conn = connect()
    # cursor = conn.cursor()
    #
    # imgpath = input("Enter Path: ")
    # # img_gray = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)  # Load Image in Grayscale
    # query = ("INSERT INTO `mvp`.`data` (type_id, data) VALUES (%s, %s);")
    # cursor.execute(query, ("image", cPickle.dumps(img_gray)))
    # conn.commit()
    #
    # query = ("SELECT LAST_INSERT_ID()")
    # cursor.execute(query)
    #
    # for ID in cursor:
    #     print(ID)
    #
    # cursor.close()
    # close(conn)

########################################################################################################################
#MAIN


if input("Do you have a user id? y/n: ").lower() == 'y'.strip():
    author = getAuthor()  # returns tuple (author_id, nickname)
elif input("Create new ID? y/n: ").lower() == 'y'.strip():
    author = createNewId()  # returns tuple (author_id, nickname)

if input("Add new image? y/n: ").lower() == 'y'.strip():
    # imgData = addImg()
    print("Need Function")
