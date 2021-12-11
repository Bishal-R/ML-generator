from flask import Flask,url_for,render_template,send_from_directory,request,send_file
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import BytesIO
from process import estimate
import libarary
# flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(200), nullable=False)
    uemail=db.Column(db.String(200),nullable=False)
    file_name=db.Column(db.String(200),nullable=False) 
    file_data=db.Column(db.LargeBinary)
    # file_model=db.Column(db.LargeBinary)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        print("<Task%r>" % self.id)
        return "<Task %r>" % self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        uname=request.form['uname']
        uemail=request.form['uemail']
        file=request.files['upload_file']
        # msg=estimate(file)
        db_task=Todo(
                    uname=uname,
                    uemail=uemail,
                    file_name=file.filename,
                    file_data=file.read()
                    )
        try:
            db.session.add(db_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue additing your task"
        return render_template('train_test.html',msg=msg)
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)
        # return render_template('train_test.html')

@app.route('/download/<int:id>')
def download(id):
    file_data=Todo.query.filter_by(id=id).first()
    return send_file(BytesIO(file_data.file_data),attachment_filename=file_data.file_name,as_attachment=True)


if __name__=="__main__":
    app.run(debug=True)
