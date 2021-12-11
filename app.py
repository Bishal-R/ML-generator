import pickle
import types
from flask import Flask,url_for,render_template,send_from_directory,request,send_file
from datetime import datetime

from sqlalchemy.sql.sqltypes import NullType
from process import estimate
from col_maneged import col_reset
import  numpy as np
import csv

from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy, model,sqlalchemy
from sqlalchemy import PickleType
import io
import pandas as pd
from io import BytesIO
from werkzeug.routing import FloatConverter as BaseFloatConverter
from sqlalchemy.ext.mutable import MutableList

app=Flask(__name__)

# database operation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ML_generator.db'

db = SQLAlchemy(app)

class USERS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(200), nullable=True)
    uemail=db.Column(db.String(200),nullable=True)
    upassword=db.Column(db.String(200),nullable=True)
    df_name=db.Column(db.String(200),nullable=False) 
    df_data=db.Column(db.LargeBinary)
    model_name=db.Column(db.String(200),nullable=True) 
    model_data=db.Column(PickleType)
    # model_data=db.Column(db.LargeBinary)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        print("<Task%r>" % self.id)
        return "<Task %r>" % self.id

@app.route('/')
def homepage():
    return render_template('home.html')
@app.route('/train')
def train():
   return render_template('train.html')
@app.route('/test')
def test():
   return render_template('test.html')

@app.route('/training',methods=['POST'])
def training():
    if request.method=='POST':
        
        uname=request.form['uname']
        uemail=request.form['uemail']
        upassword=request.form['upassword']
        csv_file=request.files['upload_file']
        label_col=request.form['tar_col_nm']
        # learnmethod = request.form.getlist('learnmethod')
        # tar_class = request.form.getlist('tar_class')
        # print(tar_class[0])
        data=[]
        try:
            stream = io.TextIOWrapper(csv_file.stream._file, "UTF8", newline=None)
            csv_input = csv.reader(stream)
            for row in csv_input:
                data.append(row)
            df=pd.DataFrame(data=data)
            show_df=df.to_html(header=False,index=False)
            cal_data=df.to_csv(index=False)
            final_df= col_reset(df)
            train_model=estimate(final_df)
            db_task=USERS(
            uname=uname,
            uemail=uemail,
            upassword=upassword,
            df_name=csv_file.filename,
            df_data=csv_file.read(),
            model_name='Trained model',
            model_data=pickle.dumps(train_model)
            )
            try:
                db.session.add(db_task)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue additing your task"

        except:
            return "There is an error"
        
        
    else:
       train_error="There are error by training on data"
       return render_template('error.html',train_error=train_error)
    
       
@app.route('/save')
def save():
    tasks=USERS.query.order_by(USERS.date_created).all()
    return render_template('model.html',tasks=tasks)

@app.route('/testing',methods=['POST'])
def testing():
    if request.method=='POST':
        upload_model=request.files['upload_model']
        my_mdl=pickle.load(upload_model)
        label_col=request.form['input_val']
        predict_val=my_mdl.predict([[label_col]])
    return str(predict_val[0])

@app.route('/download_df/<int:id>')
def download_df(id):
    file_data=USERS.query.filter_by(id=id).first()
    return send_file(BytesIO(file_data.df_data),attachment_filename=file_data.df_name,as_attachment=True)
@app.route('/download_mdl/<int:id>')
def download_mdl(id):
    file_data=USERS.query.filter_by(id=id).first()
    return send_file(BytesIO(file_data.model_data),attachment_filename=file_data.model_name,as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)
