from flask import Flask ,request,Response,jsonify
from db import create_db,db
from models import imgModel
from flask_restful import marshal_with,fields,abort
import os
from werkzeug.utils import secure_filename
from keras.models import load_model
from keras.preprocessing import image
import keras
import pandas as pd 
import numpy as np
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r'/*': {"origins": '*'}})

UPLOAD_FOLDER="files"

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///imgDb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADER'] = 'Content-Type'



create_db(app)

resource_fields ={
    "id":fields.Integer,
    "name":fields.String,
    "mimetype":fields.String,
    "img":fields.String

}


model =load_model("files/chicken_model.h5")


@app.route("/",methods=['GET','POST'])
@marshal_with(resource_fields)
def Hello():
    results = imgModel.query.filter_by(id=1).first()
    return results

@app.route('/create',methods=['POST'])
def create():
    if request.method == "POST":
        data = request.get_json()
        new_image=imgModel(img=data['img'],name=data['name'],mimetype=data['mimetype'])
        db.session.add(new_image)
        db.session.commit()
        return data

@app.route("/upload",methods=['POST'])
#@cross_origin(origin='*', headers=['Content-Type', 'Authorization','Access-Control-Allow-Origin'])
def upload():
    if request.method=="POST":
        picture = request.form['photo']
        if not  picture:
            return {"results":"No is file"}
        #filename = secure_filename(picture.filename)
        #mimetype = picture.mimetype
        #img=imgModel(img=picture.read(),name=filename,mimetype=mimetype)
        #db.session.add(img)
        #db.session.commit()
        filename=secure_filename(picture.filename)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        test_image = keras.preprocessing.image.load_img("files/"+filename,target_size=(256,256,3))
        test_image = keras.preprocessing.image.img_to_array(test_image)
        test_image = np.expand_dims(test_image,axis=0)
        prediction = model.predict_classes(test_image)
        classes=["cocci","healthy"]
        pred= classes[prediction[0]]
        return {'results':pred},200


@app.route('/image/<int:id>',methods=['GET'])
def image(id):
    img = imgModel.query.get(id)
    if not img:
        return "image not found",404
    test_image = image.load_img(img.img+img.mimetype,target_size=(256,256,3))
    test_image = image_to_array(test_image)
    test_image = np.expand_dims(test_image)
    prediction = model.predict_classes(test_image)
    return prediction,200


if __name__ == "__main__":
    app.run(debug=True)
