from flask import Flask, render_template, request, redirect, url_for, session
# Importaciones necesarias para SQLAlchemy y datetime
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os 
# from dotenv import load_dotenv # Opcional: si deseas cargar variables desde un archivo .env

# load_dotenv() # Descomentar si usas un archivo .env

app = Flask(__name__)
# Usar una variable de entorno para la clave secreta
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_fallback_si_no_hay_env')

# --- CONFIGURACIÓN DE BASE DE DATOS (CAMBIADO A SQLITE PARA ELIMINAR ERRORES DE CONEXIÓN) ---
# SQLITE es la base de datos recomendada para desarrollo en Flask.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'sqlite:///site.db' # Usamos una base de datos SQLite en un archivo local
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELO DE DATOS (Tabla de Órdenes) ---
class Order(db.Model):
    __tablename__ = 'orders' # Nombre explícito de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    piso = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.id} by {self.nombre}>"

# Creador de tablas (solo se ejecuta una vez al inicio)
with app.app_context():
    db.create_all()
    print("--- Tablas de la base de datos creadas o verificadas. ---")
# --------------------------------------------------------------------------------

# 1. Página de Intro (Video)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Página de Inicio (Botón Empezar)
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

# 3. Paso 1: Ingresar Nombre
@app.route('/orden/nombre', methods=['GET', 'POST'])
def paso1_nombre():
    if request.method == 'POST':
        nombre = request.form.get('recipient_name')
        session['nombre_usuario'] = nombre
        return redirect(url_for('paso2_telefono'))
    
    return render_template('crear-orden.html')

# 4. Paso 2: Ingresar Teléfono
@app.route('/orden/telefono', methods=['GET', 'POST'])
def paso2_telefono():
    if request.method == 'POST':
        telefono = request.form.get('recipient_phone')
        session['telefono_usuario'] = telefono
        return redirect(url_for('paso3_final'))
        
    return render_template('crear-orden2.html')

# 5. Paso 3: Confirmación / Piso (Guarda la orden y redirige a ENVIO)
@app.route('/orden/final', methods=['GET', 'POST'])
def paso3_final():
    if request.method == 'POST':
        piso = request.form.get('floor_number')
        nombre = session.get('nombre_usuario')
        telefono = session.get('telefono_usuario')
        
        # --- LÓGICA DE PERSISTENCIA (GUARDAR EN LA DB) ---
        if nombre and telefono and piso:
            try:
                nueva_orden = Order(
                    nombre=nombre,
                    telefono=telefono,
                    piso=piso
                )
                db.session.add(nueva_orden)
                db.session.commit()
                print(f"--- ORDEN ID {nueva_orden.id} GUARDADA EN DB ---")
            except Exception as e:
                db.session.rollback()
                print(f"ERROR al guardar en DB: {e}")
            finally:
                # Limpiamos la sesión después de guardar
                session.pop('nombre_usuario', None)
                session.pop('telefono_usuario', None)
            
        # REDIRECCIÓN CLAVE: Ir a la pantalla de "Enviando"
        return redirect(url_for('orden_enviando'))
    
    # Si es GET (al cargar la página), renderizamos la plantilla
    return render_template('crear-orden3.html', 
                           nombre=session.get('nombre_usuario'), 
                           telefono=session.get('telefono_usuario'))

# 6. Nueva Ruta: Pantalla de Envío (Dura 10s)
@app.route('/orden/enviando')
def orden_enviando():
    return render_template('envio.html')

# 7. Nueva Ruta: Pantalla de Fin
@app.route('/orden/completada')
def orden_completada():
    return render_template('fin.html')

if __name__ == '__main__':
    app.run(debug=True)