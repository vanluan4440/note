from flask import Flask, render_template, jsonify,request,redirect
import json,urllib.request
import string
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
key={
  "type": "service_account",
  "project_id": "notepad01-8ffb5",
  "private_key_id": "f9b2d70a820d49d601e47116b2eb92ba8cc0e177",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7gwTxdAMFqKzI\nFQjK9TZqy3+TGXxpfTND4Ai20Rhtpvo7DYJ2NrOWn96+N3K6C07jGlyqzbfDoXvF\nYNsmoB6wcoROFq39MoRWYRvZstcgIYYNheH8ecm35adjo5ywQInpGhr0dIgNLcqy\n4xGxH4Fhux29O4eMDY5p/4i3WubqeqaQsAYa3i0FMOOcdfdb7QsUN7VNL+kcmGO4\nykWEX/VuheAk/OdZy4pc0G6C1bsFOfLSXFq2F+Qj2bzXBZ308pf8qTUIGo9YIQIX\nk+b+034bj+yyub+A9jArIM1dlJsEPL9y4/gpvVxO0p/CsCci1gDG8ZJyRK4ilMcU\nGbcIzETzAgMBAAECggEADQSS27WaTBvZTUNOStMjmCdQ4jHteoTLXVWvrlTtnDvM\nJqo+cJSOxBofP/LgGJPfiy2WWalSQETQeM9d4wEHErHC4omLsCtbhPH50JO+pRVq\nKBcK9qtB2pKrd1GM96737T33cD4XbaY6D1BrgCihEZJR4PIK7ATvxb4e1UrFlY3z\nh45bI80nXNt+yPX74JUx9WSnKNzosCSgj8sTHmEMLJAh7f7/PuptG+aZgVoByAct\nC67HBUfT8hkNNB9rJcucNcduz1Ar1dvi5CvwOVlChyGu6AELQ1A0v1KLKbEKMO1u\nNSDYYYtaDFo/p1OFKYUULtGNBd6L1tqr8xhM866MaQKBgQDpwLZOTAIfWOxI0tsm\n0oTHV/9B8ipEQYdcfUq0tTzGBGIP/0t+1vtxmKNNKEr9y/L64DtK0unOMLRFf/0b\nBqrTSe7ZrK26KNRb9Nopza43kNTSl4/woj/iFEWEWDSSUPD3dwqdD0J/NDxT0k4H\nkIZOeyx3W5FF19lVZjKkoLjB5QKBgQDNW6o/ftl/A9+SaRL9oTpF8+evwXQcQZi/\nzL+BGgJqZQz7U+pLjiQE9WKC7ci4Xeqf6hGrh9ZlMR5yu4M2F5vijaD/CBzxhlmK\nLzvuZF5DbN/I8tscGjby3HgBbhT1UqEKOZ4YgNulrtJrhRNAdeI4dGy4vK8lyaV+\n162AaiVd9wKBgCiHXFSZAykyPs2lmY/Somj5ze0+Mqvg/LpBkwlf/yiKLAKADjPw\nzGn2wCGpoc79ZKSw6jbf+N/iO+9s8JKWBlpaEEq3kOudFqzW+FiVK+bAetYEp1Ve\nnFrzjtYSgRL5a75Mao+uzKXHhco2xYa0PUUwQBZ1zutgMHOJI7C9mSstAoGANTWc\nHkmq50tEobYSEp+07q0tChAxGqUwg/n0YOoxWAoI3BI5MgyJbrN6K/yatpK3GWpX\n278doSiiAA5wCBMD9CbIYWxju30ZNEHa4IEnH4dVUMcEWPq95B2WBqDUU2Buk6ys\nNyMkRoDOysc3Xstsqz4XcaKKK1tdQ0l1DkHynq8CgYEAk4MbhHXurxHoJiZmSHPt\nTbdkVx+6/ojwqR1ZB6IuszTKIrvq1Mjp6XYkzzkLVAhRkgO7lIgu+dhMuUr0iKMy\nTE5d0M7b2ZQe0IH8SqL+FbS6oW6VuSgFeEmP8qaN1EwIwS6/pcAGczH6/31PEiVA\nBqhJSsbfGMXnETCe7UU/+bw=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ni0ei@notepad01-8ffb5.iam.gserviceaccount.com",
  "client_id": "113774512200315815438",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ni0ei%40notepad01-8ffb5.iam.gserviceaccount.com"
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