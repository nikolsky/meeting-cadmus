from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
#@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        #return "File has been uploaded."
        print("filename", file.filename)
        return redirect(url_for('video', VideoPath=file.filename))
    return render_template('index.html', form=form)

@app.route('/video/<path:VideoPath>')
def video(VideoPath):
    print(VideoPath)

    insights = summary = arrangements = "In progress..."
    folder_path = app.config['UPLOAD_FOLDER'] + "/" + VideoPath
    try:
        with open(folder_path + "_insights.txt", "r") as f:
            insights = f.read()
    except:
        pass
    
    try:
        with open(folder_path + "_summary.txt", "r") as f:
            summary = f.read()
    except:
        pass

    try:
        with open(folder_path + "_arrangements.txt", "r") as f:
            arrangements = f.read()
    except:
        pass
    
    return render_template('videoplayer.html', video_path = VideoPath, insights = insights, summary = summary, arrangements = arrangements)


if __name__ == '__main__':
    app.run(debug=True)