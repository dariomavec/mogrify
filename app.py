from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import logging
import os

### CONSTANTS
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## https://docstrings.wordpress.com/2014/04/19/flask-access-log-write-requests-to-file/
logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)

# Also add the handler to Flask's logger for cases
#  where Werkzeug isn't used as the underlying WSGI server.
app.logger.addHandler(handler)


### Cache control
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    return response


### App routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/primitive/")
# def combine():
#   return redirect(url_for('index'))
#   src = request.args.get('img', 'chicago.jpg')
#   sty = request.args.get('sty', 'mosaic.t7')
#   shellargs = ["th", "fast_neural_style.lua",
#     "-model", os.path.join(STYPATH,sty),
#     "-input_image", os.path.join(app.config['UPLOAD_FOLDER'], src),
#     "-output_image", "out.png",
#     "-gpu", "0"]
#   ret = subprocess.call(shellargs, cwd = FNSPATH)
#   shutil.copy(IMGPATH, STATICPATH)
#   return redirect(url_for('index'))

### Uploads
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()