from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacation_spots.db'
db = SQLAlchemy(app)

# VacationSpot model
class VacationSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description
        }

@app.route('/vacation_spots', methods=['GET'])
def get_vacation_spots():
    vacation_spots = VacationSpot.query.all()
    spots = [spot.to_dict() for spot in vacation_spots]
    return jsonify(spots)

@app.route('/vacation_spots/<int:id>', methods=['GET'])
def get_vacation_spot(id):
    spot = VacationSpot.query.get(id)
    if spot:
        return jsonify(spot.to_dict())
    else:
        return jsonify({'error': 'Vacation spot not found.'}), 404

@app.route('/vacation_spots', methods=['POST'])
def add_vacation_spot():
    name = request.json['name']
    location = request.json['location']
    description = request.json['description']
    new_spot = VacationSpot(name=name, location=location, description=description)
    db.session.add(new_spot)
    db.session.commit()
    return jsonify({'message': 'Vacation spot added successfully.', 'spot': new_spot.to_dict()}), 201

@app.route('/vacation_spots/<int:id>', methods=['PUT'])
def update_vacation_spot(id):
    spot = VacationSpot.query.get(id)
    if spot:
        spot.name = request.json['name']
        spot.location = request.json['location']
        spot.description = request.json['description']
        db.session.commit()
        return jsonify({'message': 'Vacation spot updated successfully.', 'spot': spot.to_dict()})
    else:
        return jsonify({'error': 'Vacation spot not found.'}), 404

@app.route('/vacation_spots/<int:id>', methods=['DELETE'])
def delete_vacation_spot(id):
    spot = VacationSpot.query.get(id)
    if spot:
        db.session.delete(spot)
        db.session.commit()
        return jsonify({'message': 'Vacation spot deleted successfully.'})
    else:
        return jsonify({'error': 'Vacation spot not found.'}), 404

if __name__ == '__main__':
    with app.app_context():  # Add this line to set up Flask application context
        db.create_all()  # Move this line inside the app context
    app.run(debug=True)
