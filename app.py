import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'js'}

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
def main():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        file1_name = secure_filename(file1.filename)
        file2_name = secure_filename(file2.filename)

        if not allowed_file(file1_name) or not allowed_file(file2_name):
            return "File extension is not supported"

        file1.save(os.path.join('/tmp', file1_name))
        file2.save(os.path.join('/tmp', file2_name))

        with open(os.path.join('/tmp', file1_name), 'r') as f:
            text1 = f.read()

        with open(os.path.join('/tmp', file2_name), 'r') as f:
            text2 = f.read()

        try:
            score = get_jaccard_sim(text1, text2)
            return f"Jaccard Similarity Score: {score}"
        except:
            return "File extension is not supported"
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