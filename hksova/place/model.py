from ..database import db

class Place(db.Model):
    __tablename__ = 'place'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, db.ForeignKey('year.idYear'), nullable=True) # Assuming 'year' table has 'idYear'
    name = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    
    puzzles = db.relationship('Puzzle', back_populates='place', lazy=True)
