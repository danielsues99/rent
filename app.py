from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Landlord(db.Model):
    __tablename__ = 'landlords'
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'dni': self.dni, 'name': self.name, 'phone': self.phone, 'email': self.email}
    
class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'dni': self.dni, 'name': self.name, 'phone': self.phone, 'email': self.email}

@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

### Routes for Landlords ###
# Create Landlord
@app.route('/landlords', methods=['POST'])
def create_landlord():
    try:
        data = request.get_json()
        new_landlord = Landlord(name=data['name'], phone=data['phone'], email=data['email'], dni=data['dni'])
        db.session.add(new_landlord)
        db.session.commit()
        return make_response(jsonify({'message': 'landlord created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating landlord', 'error': str(e)}), 500)

# Get Landlords
@app.route('/landlords', methods=['GET'])
def get_landlords():
    try:
        landlords = Landlord.query.all()
        return make_response(jsonify([landlord.json() for landlord in landlords]), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting landlords', 'error': str(e)}), 500)
  
# Get a specific landlord by id
@app.route('/landlords/<int:id>', methods=['GET'])
def get_landlord(id):
    try:
        landlord = Landlord.query.filter_by(id=id).first()
        if landlord:
            return make_response(jsonify({'landlord': landlord.json()}), 200)
        return make_response(jsonify({'message': 'landlord not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting landlord', 'error': str(e)}), 500)
  
# Update a landlord
@app.route('/landlords/<int:id>', methods=['PUT'])
def update_landlord(id):
    try:
        landlord = Landlord.query.filter_by(id=id).first()
        if landlord:
            data = request.get_json()
            landlord.name = data['name']
            landlord.phone = data['phone']
            landlord.email = data['email']
            landlord.dni = data['dni']
            db.session.commit()
            return make_response(jsonify({'message': 'landlord updated'}), 200)
        return make_response(jsonify({'message': 'landlord not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating landlord', 'error': str(e)}), 500)

# Delete a landlord
@app.route('/landlords/<int:id>', methods=['DELETE'])
def delete_landlord(id):
    try:
        landlord = Landlord.query.filter_by(id=id).first()
        if landlord:
            db.session.delete(landlord)
            db.session.commit()
            return make_response(jsonify({'message': 'landlord deleted'}), 200)
        return make_response(jsonify({'message': 'landlord not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting landlord', 'error': str(e)}), 500)

### Routes for Tenants ###
# Create Tenant
@app.route('/tenants', methods=['POST'])
def create_tenant():
    try:
        data = request.get_json()
        new_tenant = Tenant(name=data['name'], phone=data['phone'], email=data['email'], dni=data['dni'])
        db.session.add(new_tenant)
        db.session.commit()
        return make_response(jsonify({'message': 'tenant created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating tenant', 'error': str(e)}), 500)

# Get Tenants
@app.route('/tenants', methods=['GET'])
def get_tenants():
    try:
        tenants = Tenant.query.all()
        return make_response(jsonify([tenant.json() for tenant in tenants]), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting tenants', 'error': str(e)}), 500)
  
# Get a specific tenant by id
@app.route('/tenants/<int:id>', methods=['GET'])
def get_tenant(id):
    try:
        tenant = Tenant.query.filter_by(id=id).first()
        if tenant:
            return make_response(jsonify({'tenant': tenant.json()}), 200)
        return make_response(jsonify({'message': 'tenant not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting tenant', 'error': str(e)}), 500)
  
# Update a tenant
@app.route('/tenants/<int:id>', methods=['PUT'])
def update_tenant(id):
    try:
        tenant = Tenant.query.filter_by(id=id).first()
        if tenant:
            data = request.get_json()
            tenant.name = data['name']
            tenant.phone = data['phone']
            tenant.email = data['email']
            tenant.dni = data['dni']
            db.session.commit()
            return make_response(jsonify({'message': 'tenant updated'}), 200)
        return make_response(jsonify({'message': 'tenant not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating tenant', 'error': str(e)}), 500)

# Delete a tenant
@app.route('/tenants/<int:id>', methods=['DELETE'])
def delete_tenant(id):
    try:
        tenant = Tenant.query.filter_by(id=id).first()
        if tenant:
            db.session.delete(tenant)
            db.session.commit()
            return make_response(jsonify({'message': 'tenant deleted'}), 200)
        return make_response(jsonify({'message': 'tenant not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting tenant', 'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)
