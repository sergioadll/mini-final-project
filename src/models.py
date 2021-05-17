from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

business_ownership = db.Table('business_ownership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    houses = db.relationship('House', backref="user", lazy=True)
    businesses = db.relationship('Business', secondary=business_ownership, back_populates="owners", lazy=True)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        user_houses = [product.serialize() for product in self.houses]
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "houses": user_houses,
        }

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), unique=True, nullable=False)
    house_number = db.Column(db.Integer, unique=False, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<House %r>' % self.house_number

    def serialize(self):
        return {
            "id": self.id,
            "city": self.city,
            "house_number": self.house_number,
            "owner_id": self.owner_id,
        }

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    owners = db.relationship('User', secondary=business_ownership, back_populates="businesses", lazy=True)

    def __repr__(self):
        return '<Business %r>' % self.name

    def serialize(self):
        business_owners = [owner.serialize() for owner in self.owners]
        return {
            "id": self.id,
            "name": self.name,
            "owners": business_owners,
        }
