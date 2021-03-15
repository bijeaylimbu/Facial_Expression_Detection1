import os

from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, flash


from Graphical_Visualisation import Emotion_Analysis

# Let us Instantiate the app
app = Flask(__name__)

###################################################################################
# We define some global parameters so that its easier for us to tweak when required.

# When serving files, we set the cache control max age to zero number of seconds
# for refreshing the Cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###################################################################################
# Some Utility Functions

# Flask provides native support for streaming responses through the use of generator
# functions. A generator is a special function that can be interrupted and resumed.





def allowed_file(filename):
    """ Checks the file format when file is uploaded"""
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


###################################################################################








@app.route('/')
def Start():
    """ Renders the Home Page """

    return render_template('Start.html')









@app.route('/ManualUpload', methods=['POST'])
def ManualUpload():
    """ Manual Uploading of Images via URL or Upload """

    return render_template('ManualUpload.html')


@app.route('/uploadimage', methods=['POST'])
def uploadimage():
    """ Loads Image from System, does Emotion Analysis & renders."""

    if request.method == 'POST':

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # If user uploads the correct Image File
        if file and allowed_file(file.filename):

            # Pass it a filename and it will return a secure version of it.
            # The filename returned is an ASCII only string for maximum portability.
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            result = Emotion_Analysis(filename)
            print(result)


            # When Classifier could not detect any Face.
            if len(result) == 1:

                return render_template('NoDetection.html', orig=result[0])


            return render_template('Visual.html', orig=result[0], pred=result[1], bar=result[2],
                                   image=result[3], )



if __name__ == '__main__':
    app.run(debug=True)