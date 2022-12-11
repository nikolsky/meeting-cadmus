from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from ml import transcribe_streaming_v2, save_transcript, parse_transcript, merge_transcripts, translate_text, save_txt, get_summary, get_arrangements, get_insights, get_risks
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

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        video_filename = ""
        actual_video_name = ""
        speaker_to_transcript_path = {}
        for file in files:
            if file and allowed_file(file.filename):
                print("add file:", file.filename)

                abs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
                file.save(abs_path)

                if file.filename.startswith('video'):
                    video_filename = file.filename
                    actual_video_name, _ = os.path.splitext(abs_path)
                    speaker_name = file.filename.split('video',1)[1]
                    speaker_name = re.search(r"[a-zA-Z]*", speaker_name).group()

                if file.filename.startswith('audio'):
                    speaker_name = file.filename.split('audio',1)[1]
                    speaker_name = re.search(r"[a-zA-Z]*", speaker_name).group()
                    actual_filename, _ = os.path.splitext(abs_path)
                    
                    print("file", file.filename, speaker_name)
                    #print('ffmpeg -i {} -acodec pcm_s16le -ar 16000 {}.wav'.format(abs_path, actual_filename))
                    os.system('ffmpeg -y -i {} -acodec pcm_s16le -ar 16000 {}.wav'.format(abs_path, actual_filename))
                    print("file", file.filename, speaker_name)

                    trans_resp = transcribe_streaming_v2(PROJECT_ID, 'projects/472813974978/locations/global/recognizers/recognizer-4', actual_filename + '.wav')
                    save_transcript(trans_resp = trans_resp, path = actual_filename + '.txt')
                    
                    speaker_to_transcript_path[speaker_name] = actual_filename + '.txt'
       
        all_trans = parse_transcript(speaker_to_transcript_path)
        #print("All transcript", all_trans)
        new_transcript = merge_transcripts(all_trans)
        #print("New transcript", new_transcript)
        translated_txt = translate_text("%".join(new_transcript.split("\n")))
        #print("Translated text", translated_txt)
        translated_text_path = actual_video_name + "_translated_transcript.txt"
        save_txt(translated_txt, translated_text_path)

        with open(translated_text_path) as f:
            translated_txt = f.read()
    
        translated_txt = translated_txt.replace("&#39;", "")
        #translated_txt = translated_txt.replace("%", "\n")

        #print(f"Transcript have: {len(translated_txt.split())} words")

        translated_txt = "\n".join(translated_txt.split("%"))
        save_txt(translated_txt, actual_video_name + "_transcript.txt")

        ok_words = translated_txt.split()[-2450:]
        ok_words_len = sum([len(word) for word in ok_words]) + len(ok_words)

        cutted_translated_txt = translated_txt[:ok_words_len]
        #print("Cutted translated text", cutted_translated_txt)


        summary = get_summary(cutted_translated_txt)
        save_txt(summary, actual_video_name + "_summary.txt")
        
        arrangement = get_arrangements(cutted_translated_txt)
        save_txt(arrangement, actual_video_name + "_arrangements.txt")
        
        insights = get_insights(cutted_translated_txt)
        save_txt(insights, actual_video_name + "_insights.txt")

        risks = get_risks(cutted_translated_txt)
        save_txt(risks, actual_video_name + "_risks.txt")

        flash('File(s) successfully uploaded')
        return redirect(url_for('video', VideoPath=video_filename))
    return render_template('index.html')

@app.route('/video/<path:VideoPath>')
def video(VideoPath):
    print(VideoPath)
    actual_video_name, _ = os.path.splitext(VideoPath)
    insights = summary = arrangements =risks = "In progress..."
    folder_path = app.config['UPLOAD_FOLDER'] + "/" + actual_video_name
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

    try:
        with open(folder_path + "_risks.txt", "r") as f:
            risks = f.read()
    except:
        pass

    try:
        with open(folder_path + "_transcript.txt", "r") as f:
            transcript = f.read()
    except:
        pass
    
    return render_template('videoplayer.html', video_path = VideoPath, insights = insights, summary = summary, arrangements = arrangements, risks=risks, transcript=transcript)


if __name__ == '__main__':
    app.run(debug=True, port=5002)