# app.py
from flask import Flask
from models import db  # Asegúrate de importar la instancia de la base de datos
from routes import tenants_bp  # Importa el Blueprint de rutas

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db.init_app(app)

# Registrar el Blueprint de rutas
app.register_blueprint(tenants_bp)

if __name__ == '__main__':
    app.run(debug=True)