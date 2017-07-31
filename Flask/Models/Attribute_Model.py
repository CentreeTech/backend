from flaskapp import db, app



# class Numeric_Attribute(db.Model):
#     __tablename__ = 'numeric-attributes'
#     id = db.Column(db.String(36), primary_key = True)
#     name = db.Column(db.String(36))
#     value = db.Column(db.Integer)
#     _classifications = db.relationship('Classification_To_Numeric_Attribute', backref='attributes', cascade = 'all')

#     def __init__(self, id, name, value):
#     	self.id = id
#     	self.name = name
#     	self.value = value