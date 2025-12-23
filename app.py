from flask import Flask, render_template, request, redirect, url_for, session
from flask_babel import Babel, _
import os

app = Flask(__name__)

# =========================
# CONFIGURACIÓN
# =========================
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_secreta_fallback')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# =========================
# BABEL (FORMA CORRECTA 4.x)
# =========================
def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(
        app.config['BABEL_SUPPORTED_LOCALES']
    ) or 'en'

babel = Babel(app, locale_selector=get_locale)

# =========================
# CONTEXT PROCESSOR
# =========================
@app.context_processor
def inject_language():
    return {
        'current_language': get_locale()
    }

# =========================
# CAMBIO DE IDIOMA (CORREGIDO)
# =========================
@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['language'] = lang
    
    # CORRECCIÓN: Usamos request.referrer para volver a la página anterior
    # Si no hay referencia (ej. acceso directo), volvemos a 'inicio' por defecto
    return redirect(request.referrer or url_for('inicio'))

# =========================
# RUTAS
# =========================
@app.route('/')
def index():
    return redirect(url_for('inicio'))

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

# PASO 1
@app.route('/orden/nombre', methods=['GET', 'POST'])
def paso1_nombre():
    if request.method == 'POST':
        session['nombre_usuario'] = request.form.get('recipient_name')
        return redirect(url_for('paso2_telefono'))
    return render_template('crear-orden.html')

# PASO 2
@app.route('/orden/telefono', methods=['GET', 'POST'])
def paso2_telefono():
    if request.method == 'POST':
        session['telefono_usuario'] = request.form.get('recipient_phone')
        return redirect(url_for('paso3_final'))
    return render_template('crear-orden2.html')

# PASO 3
@app.route('/orden/final', methods=['GET', 'POST'])
def paso3_final():
    if request.method == 'POST':
        print(
            f"Orden creada: "
            f"{session.get('nombre_usuario')}, "
            f"{session.get('telefono_usuario')}, "
            f"Piso: {request.form.get('floor_number')}"
        )
        return redirect(url_for('orden_enviando'))

    return render_template(
        'crear-orden3.html',
        nombre=session.get('nombre_usuario'),
        telefono=session.get('telefono_usuario')
    )

@app.route('/orden/enviando')
def orden_enviando():
    return render_template('envio.html')

@app.route('/orden/completada')
def orden_completada():
    return render_template('fin.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)