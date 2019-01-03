from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from CGPA import gpa
from flask import jsonify
import threading

db=SQLAlchemy()

class Admin(db.Model):
    __tablename__="Admin"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    password=db.Column(db.String)

    @classmethod
    def login(cls,name,password):
        the_user=cls.query.filter_by(name=name).all()
        for a_user in the_user:
            if check_password_hash(a_user.password,password):
                return True
        return False

    @classmethod
    def reg(cls,name,password):
        user=cls(name=name,password=password)
        db.session.add(user)
        db.session.commit()
        return True

    def get_users(self):
        return [user.to_json() for user in self.users]

class User(db.Model):
    __tablename__="User"
    id=db.Column(db.Integer,primary_key=True)
    department=db.Column(db.String)
    fullname=db.Column(db.String)
    matno=db.Column(db.String)
    level=db.Column(db.Integer)

    admin_id=db.Column(db.Integer,db.ForeignKey(Admin.id))
    admin_relationship=db.relationship("Admin",backref="users")

    @classmethod
    def addUser(cls,matno,fullname=None,dept=None,level=None):
        user=cls(fullname=fullname,department=department,matno=matno,level=level)
        db.session.add(user)
        db.session.commit()
        return user

    def to_json(self):
        result={}
        result["id"]=self.id
        result["dept"]=self.department
        result["fullname"]=self.fullname
        result["matno"]=self.matno

        return jsonify(result)

    def __repr__(self):
        return security.matno

class gpa(db.Model):
    __tablename__="gpa"
    id=db.Column(db.Integer,primary_key=True)
    units=db.Column(db.PickleType)
    scores=db.Column(db.PickleType)

    user_id=db.Column(db.Integer,db.ForeignKey(User.id))
    user_relationship=db.relationship("User",backref="gpas")
    last_added=db.Column(db.DateTime, default=db.func.current_timestamp())

    def get(self):
        return CGPA.gpa(self.scores,self.units)

    @classmethod
    def addGpa(cls,user,units,scores):
        gpa=cls(units=units,scores=scores)
        user.gpas.append(gpa)
        db.session.commit()
        return user,gpa

class AddUser(threading.Thread):
    def __init__(self,users,admin):
        super().__init__()
        self.users=users
        self.admin=admin
        self.deamon=True
    def run(self):
        for user in self.users:
            cur_user=User.addUser(user["matno"])
            gpa.addGpa(cur_user,user["units"],user["scores"])
            self.admin.users.append(cur_user)
            db.session.commit()


if __name__=="__main__":
    ab=User(matno=11111)
    g=gpa(units=[1],scores=[79])
    ab.gpas.append(g)
    #print(g.data)
    print(type(g.units))
    gh=g.get()
    print(gh.get_tlu())
    print((g.scores))
