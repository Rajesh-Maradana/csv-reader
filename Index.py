import os
import pandas as pd
from flask import Flask, flash, jsonify, request, redirect, send_file, url_for, render_template, session
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = 'UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.secret_key = 'asdsdfsdfs13sdf_df%&'


# Home Page


@app.route('/')
def upload_file():
    return render_template('home.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Uploading and Saving File


@app.route('/upload', methods=['POST'])
def uploader():
    file = request.files['file']
    print(file.filename)
    print(allowed_file(file.filename))
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template('error.html', message='File Uploaded Successfully')
    else:
        return render_template('error.html', error='Upload Failed!')

# Login Page


@app.route('/loginpage')
def admin_login():
    return render_template('admin_login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['username'] = request.form['username']
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            files = os.listdir('UPLOAD_FOLDER')
            return render_template('data.html', file=files)
        else:
            return render_template('error.html', error='Invalid Credentials')
    elif session['username'] == 'admin':
        files = os.listdir('UPLOAD_FOLDER')
        return render_template('data.html', file=files)

    return render_template('error.html', error='Invalid Method')


# File Downloading
@app.route('/download/<name>')
def download(name):
    path = 'UPLOAD_FOLDER/{}'.format(name)
    return send_file(path, as_attachment=True)


# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('admin_login'))


# File Viewing
@app.route('/open/<name>')
def open(name):
    result = []
    path = 'UPLOAD_FOLDER/{}'.format(name)
    if name.split('.')[-1].lower() == 'csv':
        df_csv = pd.read_csv(path)
        table = df_csv.to_html()
        return render_template('table.html', table=table)
    else:
        xls = pd.ExcelFile(path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            table = df.to_html()
        return render_template('table.html', table=table)


if __name__ == '__main__':
    app.run(debug=True)
