from flaskapp import db, app

class User_Subscription():

    association_table = db.Table('user-subscription',
    db.Column('user_name', db.String(36), db.ForeignKey('users.name')),
    db.Column('service_name', db.String(36), db.ForeignKey('services.name'))
    )


