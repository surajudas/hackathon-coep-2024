import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import zipfile
import batch_reader

## Routes: '/':for 2 files and '/batch_upload'

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'js', 'py'}

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

@app.route('/batch_upload')
def upload_form():
    return '''
    <html>
    <body>
    <form method="POST" action="/upload_zip" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit">
    </form>
    </body>
    </html>
    '''    
@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)

    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('unzipped_files')

    file_paths = [os.path.join('unzipped_files', name) for name in os.listdir('unzipped_files')]

    plot_paths = batch_reader.docs_content_reader(file_paths)
    
    html = f'''<html>
    <body>
    <img src="{plot_paths[0]}" alt="Heatmap">
    <img src="{plot_paths[1]}" alt="Heatmap">
    </body>
    </html>'''

    # Return the HTML string
    return html

if __name__ == '__main__':
    app.run()