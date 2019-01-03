from flask import (Flask,request,session,url_for,jsonify,
                        flash,render_template,redirect,send_from_directory)

import config
from models import model
from CGPA import gpa


app=Flask(__name__)
app.config.from_object(config)
model.db.init_app(app)
model.db.create_all(app=app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/app")
def app_route():
    return render_template("app.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/login/")
def login():
    name=request.form["name"]
    password=request.form["password"]

    log_user_in=model.Admin.login(name,password)
    if log_user_in:
        response=redirect(url_for("home"))
        session['log'] = True
        response.set_cookie("log",value=log_user_in.id,max_age=config.COOKIE_MAX_AGE)
        return response
    else:
        return "user is not logged in"

@app.route("/register/")
def register():
    name=request.form["name"]
    password=request.form["password"]
    admin=model.Admin.reg(name,password)
    response=redirect(url_for("home"))
    session['log'] = True
    response.set_cookie("log",value=admin.id,max_age=config.COOKIE_MAX_AGE)
    return response

@app.route("/upload/result/",methods=["GET","POST"])
def upload_result():
    if config.admin or not(session.get("log") or request.cookies.get("log")):
        return redirect(url_for("login"))
    if request.methods=="POST":
        file=request.files["file"]
        title=request.form["title"]
        file.save(config.UPLOAD_FOLDER,file.filename)
        users=gpa.process(config.UPLOAD_FOLDER+"/"+file.filename+"/"+title)
        admin=model.Admin.query.filter_by(id=config.admin or request.cookies.get("log"))
        with app.test_request_context():
            model.AddUser(users,admin).start()
        return send_from_directory(app.config["UPLOAD_FOLDER"],users)
    else:
        flash("method not allowed")
        return "method not allowed"


if __name__=="__main__":
    app.run(debug=True)