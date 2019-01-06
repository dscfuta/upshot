from flask import (Flask,request,session,url_for,jsonify,
                        flash,render_template,redirect,send_from_directory)

from werkzeug.utils import secure_filename
import config
import os
from CGPA import gpa


app=Flask(__name__)
app.config.from_object(config)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/app")
def app_route():
    return render_template("app.html")
@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/files/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],filename)
@app.route("/upload/result/",methods=["GET","POST"])
def upload_result():

    if request.method=="POST":
        filenames=[]
        title=request.form["title"]

        files=[file for file in request.files.listvalues()][0]
        for file in files:
            file.save(os.path.join(config.UPLOAD_FOLDER,file.filename))
            filenames.append(os.path.join(config.UPLOAD_FOLDER,file.filename))
        response=gpa.process(filenames,title)
        [os.remove(name) for name in filenames]#clean up
        return jsonify(response)


    else:
        flash("method not allowed")
        return "method not allowed"


if __name__=="__main__":
    app.run(debug=True)