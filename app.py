from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from ml import transcribe_streaming_v2, save_transcript, parse_transcript
import re

PROJECT_ID = "my-project-98575-371210"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

ALLOWED_EXTENSIONS = set(['wav', 'mp4', 'm4a'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET',"POST"])
# def home():
#     form = UploadFileForm()


#     if form.validate_on_submit():
#         uploaded_files = request.files.getlist("file")
#         print(uploaded_files)


#         file = form.file.data # First grab the file
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
#         #return "File has been uploaded."
#         print("filename", file.filename)
        
#         trans_resp = transcribe_streaming_v2(PROJECT_ID, 'projects/472813974978/locations/global/recognizers/recognizer-4', "stas.wav")
#         save_transcript(trans_resp=trans_resp, path="stas_transcript.txt")

#         trans_resp = transcribe_streaming_v2(PROJECT_ID, 'projects/472813974978/locations/global/recognizers/recognizer-4', "artem.wav")
#         save_transcript(trans_resp=trans_resp, path="artem_transcript.txt")

#         return redirect(url_for('video', VideoPath=file.filename))
#     return render_template('index.html', form=form)

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        video_filename = ""
        speaker_to_transcript_path = {}
        for file in files:
            if file and allowed_file(file.filename):
                print("add file:", file.filename)

                abs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))

                if file.filename.startswith('video'):
                    video_filename = file.filename
                    speaker_name = file.filename.split('video',1)[1]
                    speaker_name = re.search(r"[a-zA-Z]*", speaker_name).group()

                if file.filename.startswith('audio'):
                    speaker_name = file.filename.split('audio',1)[1]
                    speaker_name = re.search(r"[a-zA-Z]*", speaker_name).group()
                    actual_filename, _ = os.path.splitext(abs_path)
                    
                    print("file", file.filename, speaker_name)
                    #print('ffmpeg -i {} -acodec pcm_s16le -ar 16000 {}.wav'.format(abs_path, actual_filename))
                    os.system('ffmpeg -i {} -acodec pcm_s16le -ar 16000 {}.wav'.format(abs_path, actual_filename))
                    print("file", file.filename, speaker_name)

                    trans_resp = transcribe_streaming_v2(PROJECT_ID, 'projects/472813974978/locations/global/recognizers/recognizer-4', actual_filename + '.wav')
                    save_transcript(trans_resp = trans_resp, path = actual_filename + '.txt')
                    speaker_to_transcript_path[speaker_name] = actual_filename + '.txt'


                #filename = secure_filename(file.filename)
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
       
        all_trans = parse_transcript(speaker_to_transcript_path)
        # new_transcript = merge_transcripts(all_trans)
        # translated_txt = translate_text("%".join(new_transcript.split("\n")))
        # save_translated_txt(translated_txt, "translated_transcript.txt")

        flash('File(s) successfully uploaded')
        return redirect(url_for('video', VideoPath=video_filename))
    return render_template('index.html')

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
    app.run(debug=True, port=5000)