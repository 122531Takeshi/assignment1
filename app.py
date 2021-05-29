from flask import Flask, render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///root.db'

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True) 
    f_name=db.Column(db.String(25),nullable=False)
    l_name=db.Column(db.String(25),nullable=False)
    email=db.Column(db.VARCHAR(25),nullable=False,unique=True)
    message=db.Column(db.String(400),nullable=False)
    complete=db.Column(db.Integer,default=0)

def __usr___(self):
    return '<Entry %r>' &self.id
@app.route('/home')
def index():
     return render_template('index.html')

@app.route('/')
def homepage():
    return redirect('/home')


@app.route('/contacts', methods=['POST','GET'])
def contact_ls():
    if request.method =='POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        message = request.form.get('message')
        new_entry = User(f_name=f_name,l_name=l_name,email=email,message=message)

        
        try:
             db.session.add(new_entry)
             db.session.commit()
             return redirect('/contacts')
        except:
                 return "Error occured when Creating Contact"
    else:
        entries=User.query.order_by(User.id).all()
        return render_template('contact.html',entries=entries)
       

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    info_to_update=User.query.get_or_404(id)
    if request.method =="POST":
        info_to_update.f_name=request.form['f_name']
        info_to_update.l_name=request.form['l_name']
        info_to_update.email=request.form['email']
        info_to_update.message=request.form['message']
        try:
            db.session.commit()
            return redirect('/contacts')
        except:
            return "There was an error in updating the info"
    
    else:
         entries=User.query.order_by(User.id).all()
         return render_template('contact.html')



@app.route("/delete/<int:id>")
def delete(id):
    info_to_remove=User.query.get_or_404(id)

    try:
        db.session.delete(info_to_remove)
        db.session.commit()
        return redirect('/contacts')
    except:
        return "Error Deleting the Task"


