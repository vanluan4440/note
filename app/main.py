from flask import Flask, render_template, jsonify,request,redirect
import json,urllib.request
import string
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
key={
  "api from fire base"
}

#function
def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_data():
    docs = db.collection(u'data').stream()
    post = []
    for doc in docs:
        post.append(doc.to_dict())
    return(post)  
def get_doc(data,doc,value):
    a = db.collection(data).where(doc, '==', value).get()
    for i in a:
        return(i.to_dict()[doc]) 
def get_value(data,doc,value,out):
    a = db.collection(data).where(doc, '==', value).get()
    for i in a:
        return(i.to_dict()[out]) 
        
def get_len(value,dk):
    docs = db.collection(u'data').stream()
    len = 0
    for doc in docs:
       if doc.to_dict()[value] == dk:
           len +=1
    return(len)    
def kt(value):
    if len(value) == 0:
        return False
    else:
        return True


cred=credentials.Certificate(key)
firebase_admin.initialize_app(cred)
db=firestore.client()
app= Flask(__name__)


app= Flask(__name__)
@app.route('/')
def index():
    len_1 = get_len('active',False)
    len = get_len('active',True)
    data = get_data()
    return render_template('index.html', data = data,len =len,len_1=len_1, err="")

@app.route('/delete/<_id>')  
def delete(_id):  
    db.collection(u'data').document(_id).delete()
    return redirect('/') 


@app.route('/update/<_id>',methods = ['GET', 'POST'])  
def update(_id):  
    if request.method == "GET":
        doc= get_doc('data','id',_id )
        title = get_value('data','id',_id,'title')
        id = get_value('data','id',_id,'id')
        data = {"title":title,"id":id}
        return render_template('edit.html',data=data,err="") 
    if request.method == "POST":
        if kt(request.form['title']) == False:
            doc= get_doc('data','id',_id )
            title = get_value('data','id',_id,'title')
            id = get_value('data','id',_id,'id')
            data = {"title":title,"id":id}
            return render_template('edit.html',data=data,err="require from input")  
        else:
            id = id_generator()
            doc = db.collection('data').document(id)
            time = get_value('data','id', _id, 'time')
            active = get_value('data','id', _id, 'active')
            obj = {
                    'id':id,
                    'title': request.form['title'],
                    'active':active,
                    'time': time
                    }
            doc.set(obj)
            db.collection(u'data').document(_id).delete()
            return redirect('/')
@app.route('/add',methods = ['GET', 'POST'] )  
def add(): 
    if request.method == "GET":
         return render_template('index.html')
    if request.method == "POST":
        if kt(request.form['title']) == False:
            len_1 = get_len('active',False)
            len = get_len('active',True)
            data = get_data()
            return render_template('index.html', data = data,len =len,len_1=len_1,err="Require from title")
        else:
            id = id_generator()
            doc = db.collection('data').document(id)
            obj = {
                'id':id,
                'title': request.form['title'],
                'active':True,
                'time': datetime.datetime.now()
                }
            doc.set(obj)
            return redirect('/')
@app.route('/api/data' )
def api():
    return jsonify(get_data())
@app.route('/complete/<_id>',methods = ['GET', 'POST'])
def complete(_id):
    doc = db.collection('data').document(_id)
    id = get_value('data','id', _id, 'id')
    title = get_value('data','id', _id, 'title')
    time = get_value('data','id', _id, 'time')
    obj = {
            'id':id,
            'title': title,
            'active':False,
            'time': time
        }
    doc.set(obj)
    return redirect('/')
@app.route('/undo/<_id>',methods = ['GET', 'POST'])
def undo(_id):
    doc = db.collection('data').document(_id)
    id = get_value('data','id', _id, 'id')
    title = get_value('data','id', _id, 'title')
    time = get_value('data','id', _id, 'time')
    obj = {
            'id':id,
            'title': title,
            'active':True,
            'time': time
        }
    doc.set(obj)
    return redirect('/')
