from db import db



class imgModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    img=db.Column(db.Text,unique=True,nullable=False)
    name=db.Column(db.Text,nullable=False)
    mimetype=db.Column(db.Text,nullable=False)

    def __repr__(self):
        return f"Image(img={img},name={name},mimetype={mimetype})"


