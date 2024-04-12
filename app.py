import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_jaccard_sim(str1, str2): 
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/view')
def view():
    score = get_jaccard_sim('hello world', 'hello world')
    print(score)
    return f"Jaccard Similarity Score: {score}"

@app.route('/view2', methods=['GET', 'POST'])
def view2():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        file1_name = secure_filename(file1.filename)
        file2_name = secure_filename(file2.filename)

        file1.save(os.path.join('/tmp', file1_name))
        file2.save(os.path.join('/tmp', file2_name))

        with open(os.path.join('/tmp', file1_name), 'r') as f:
            text1 = f.read()

        with open(os.path.join('/tmp', file2_name), 'r') as f:
            text2 = f.read()

        score = get_jaccard_sim(text1, text2)
        return f"Jaccard Similarity Score: {score}"
    else:
        return '''
        <h1>Upload two files to compare</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file1>
          <input type=file name=file2>
          <input type=submit value=Upload>
        </form>
        '''

if __name__ == '__main__':
    app.run()