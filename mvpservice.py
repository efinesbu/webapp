from flask import Flask, request
import platform
import tempfile
import os

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
            filename = tempfile.mktemp(suffix=file_extension) # [, prefix = 'tmp'[, dir = None]]])
            print(filename)
            file.save(filename)
            return f"""
                <hr>
                save = {filename}
                <hr>
            """
            return redirect(url_for('uploaded_file',
                                    filename=filename))
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
    app.run(host='172.31.90.152', port=80)

'''
CONNECTIONS 

Original EC2
Use in Browser: Public IP: http://3.88.217.30/
Use in Code: Private IP: 172.31.90.152

Permissioned EC2: webservice2
Use in Browser: Public IP: http://18.205.29.255/
Use in Code: Private IP: 172.31.87.215

'''