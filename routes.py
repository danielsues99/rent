# routes.py
from flask import Blueprint, jsonify, make_response, request
from models import Tenant  # Asegúrate de importar el modelo Tenant
from app import db  # Asegúrate de importar la instancia de la base de datos

tenants_bp = Blueprint('tenants', __name__)

# Get a specific tenant by id
@tenants_bp.route('/tenants/<int:id>', methods=['GET'])
def get_tenant(id):
    try:
        tenant = Tenant.query.filter_by(id=id).first()
        if tenant:
            return make_response(jsonify({'tenant': tenant.json()}), 200)
        return make_response(jsonify({'message': 'tenant not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting tenant', 'error': str(e)}), 500)

# Update a tenant
@tenants_bp.route('/tenants/<int:id>', methods=['PUT'])
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
@tenants_bp.route('/tenants/<int:id>', methods=['DELETE'])
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