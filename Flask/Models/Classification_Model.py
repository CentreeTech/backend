from flaskapp import db, app


class Classification_Model(db.Model):
    __tablename__ = 'classifications'

    id = db.Column(db.Text, primary_key=True)
    service_name = db.Column(db.String(36), db.ForeignKey('services.name'))
    start_time = db.Column(db.Integer)
    stop_time = db.Column(db.Integer)
    media = db.Column(db.Text)
    #num_attributes = db.relationship('Classification_To_Numeric_Attribute', backref='classifications', cascade = 'all')
    str_attributes = db.relationship('Classification_To_String_Attribute', backref='classifications', cascade = 'all')

    def __init__(self, id, service_name, start, stop, media):
        self.id = id
        self.service_name = service_name
        self.start_time = start
        self.stop_time = stop
        self.media = media

    def __repr__(self):
        return '<id {}>'.format(self.id) + ', <service {}>'.format(self.service) 
        + ', <start {},'.format(self.start) + ', stop {}>'.format(self.stop) + ', <media {}>'.format(self.media)

class Classification_To_String_Attribute(db.Model):
	__tablename__ = 'class-string-attribute'
	classification_id = db.Column(db.String(36), db.ForeignKey('classifications.id', ondelete = 'CASCADE'), primary_key = True)
	attribute_name = db.Column(db.String(36), db.ForeignKey('string-attributes.id', ondelete = 'CASCADE'), primary_key = True)

	def __init__(self, classification_id, attribute_name):
		self.classification_id = classification_id
		self.attribute_name = attribute_name

	def __repr__(self):
		return '<classification_id {}>'.format(self.classification_id) + ', <attribute_name {}>'.format(self.attribute_name)

class String_Attribute(db.Model):
    __tablename__ = 'string-attributes'

    id = db.Column(db.String(36), primary_key = True)
    name = db.Column(db.String(36))
    value = db.Column(db.String(36))
    _classifications = db.relationship('Classification_To_String_Attribute', backref='attributes', cascade = 'all')

    def __init__(self, id, name, value):
    	self.id = id
    	self.name = name
    	self.value = value

# class Classification_To_Numeric_Attribute(db.Model):
# 	__tablename__ = 'class-numeric-attribute'
# 	classification_id = db.Column(db.String(36), db.ForeignKey('classifications.id', ondelete = 'CASCADE'), primary_key = True)
# 	attribute_name = db.Column(db.String(36), db.ForeignKey('numeric-attributes.id'), primary_key = True)
	
# 	def __init__(self, classification_id, attribute_name):
# 		self.classification_id = classification_id
# 		self.attribute_name = attribute_name

# 	def __repr__(self):
# 		return '<classification_id {}>'.format(self.classification_id) + ', <attribute_name {}>'.format(self.attribute_name)


