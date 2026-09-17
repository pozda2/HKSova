from ..database import db

class Puzzle(db.Model):
    __tablename__ = 'puzzle'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, db.ForeignKey('year.idYear'), nullable=True)
    position = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    final = db.Column(db.Boolean, nullable=False, default=False)
    code = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    id_place = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=True)
    specification = db.Column(db.Text, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=True)
    hint = db.Column(db.Text, nullable=True)
    hint_interval = db.Column(db.Integer, nullable=True, default=30)
    mandatory_additional_info = db.Column(db.Boolean, nullable=True)
    solution = db.Column(db.Text, nullable=True)
    solution_interval = db.Column(db.Integer, nullable=True)
    solution_instructions = db.Column(db.Text, nullable=True)
    solution_url = db.Column(db.String(255), nullable=True)
    id_forum_section = db.Column(db.Integer, nullable=True)

    place = db.relationship('Place', back_populates='puzzles', lazy=True)


def _to_public_dict(p):
    return {
        'id': p.id, 'position': p.position, 'name': p.name, 'final': bool(p.final),
        'place': p.place, 'specification': p.specification, 'description': p.description,
        'url': p.url, 'hint': p.hint, 'solution': p.solution,
        'solution_instructions': p.solution_instructions, 'solution_url': p.solution_url,
        'id_forum_section': p.id_forum_section,
    }


def get_puzzles(year):
    '''Puzzles of a year, in route order, for the public "Po hře" pages.'''
    puzzles = Puzzle.query.filter_by(year=year['year']).order_by(Puzzle.position).all()
    return [_to_public_dict(p) for p in puzzles]


def get_puzzle_by_position(year, position):
    p = Puzzle.query.filter_by(year=year['year'], position=position).first()
    return _to_public_dict(p) if p else None
