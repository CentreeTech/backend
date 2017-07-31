from flaskapp import db, app


class Config_Model(db.Model):
    __tablename__ = 'configs'

    name = db.Column(db.String(36), primary_key=True)
    value = db.Column(db.String(50), primary_key=True)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<name {}>'.format(self.name) + ', <value {}>'.format(self.value)