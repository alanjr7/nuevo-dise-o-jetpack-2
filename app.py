from flask import Flask, render_template, request, redirect, url_for, session
from flask_babel import Babel, gettext as _
import os 
import serial
from datetime import datetime
import time

# --- CONFIGURACIÓN DE APP ---
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_fallback_si_no_hay_env')

# --- CONFIGURACIÓN DE IDIOMAS ---
app.config['BABEL_DEFAULT_LOCALE'] = 'en'  # Inglés por defecto
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es']

# Inicializar Babel
babel = Babel(app)

# Función para obtener el idioma desde la sesión
def get_locale():
    # Devuelve el idioma guardado en sesión, o inglés por defecto
    return session.get('language', 'en')

# Configurar Babel con nuestra función
babel.init_app(app, locale_selector=get_locale)

# Ruta para cambiar idioma - CORREGIDA
@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'es']:
        session['language'] = lang
        print(f"--- IDIOMA CAMBIADO A: {lang} ---")
    
    # CORRECCIÓN: Redirigir a la página actual, no siempre al inicio
    return redirect(request.referrer or url_for('inicio'))

# --- CONFIGURACIÓN ARDUINO ---
PUERTO_SERIAL = 'COM3' 
BAUD_RATE = 115200

def enviar_comando_arduino(comando):
    """
    Intenta enviar un comando ('A' o 'C') al Arduino a través del puerto serial.
    Retorna True si el envío fue exitoso, False en caso contrario.
    """
    comando_byte = comando.encode('utf-8')
    
    try:
        ser = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
        time.sleep(2) 
        ser.write(comando_byte)
        print(f"--- COMANDO SERIAL ENVIADO A ARDUINO: {comando} ---")
        ser.close()
        return True
    
    except serial.SerialException as e:
        print(f"--- ERROR CRÍTICO DE COMUNICACIÓN SERIAL ---")
        print(f"No se pudo conectar o enviar al puerto {PUERTO_SERIAL}.")
        print(f"Asegúrate de que Arduino está conectado y el puerto es correcto.")
        print(f"Detalle del error: {e}")
        return False
    except Exception as e:
        print(f"--- OTRO ERROR: {e} ---")
        return False

# Código de Arduino para mostrar en consola
ARDUINO_CODE_SUCCESS = """
Abriendo puerta...
servoIzquierdo.write(180); // IZQ_ABIERTO
delay(500);
servoDerecho.write(0); // DER_ABIERTO
Puerta abierta.
"""

ARDUINO_CODE_FAILURE = """
Cerrando puerta...
servoDerecho.write(90); // DER_CERRADO
delay(500);
servoIzquierdo.write(87); // IZQ_CERRADO
Puerta cerrada.
"""

# --- RUTAS DE LA APLICACIÓN ---

# 1. Página de Intro (Video)
@app.route('/')
def index():
    """Ruta: / -> index.html (Video de bienvenida)"""
    return render_template('index.html')

# 2. Página de Inicio (Botón Empezar) - ÚNICO lugar con botón de idioma
@app.route('/inicio')
def inicio():
    """Ruta: /inicio -> inicio.html (Pantalla de inicio/Empezar)"""
    return render_template('inicio.html')

# 3. Paso 2: Ingresar Teléfono/Código
@app.route('/orden/telefono', methods=['GET', 'POST'])
def paso2_telefono():
    if 'intentos' not in session:
        session['intentos'] = 0

    error_msg = None

    if request.method == 'POST':
        codigo_ingresado = request.form.get('recipient_phone')

        # CÓDIGO CORRECTO
        if codigo_ingresado == '1234':
            session.pop('intentos', None)
            enviar_comando_arduino('A')
            return redirect(url_for('orden_tiempo'))

        # CÓDIGO INCORRECTO
        else:
            session['intentos'] += 1
            enviar_comando_arduino('C')

            if session['intentos'] >= 3:
                session.pop('intentos', None)
                return redirect(url_for('orden_completada'))

            error_msg = _("Incorrect")

    intentos_restantes = 3 - session['intentos']

    return render_template(
        'crear-orden2.html',
        error_msg=error_msg,
        intentos_restantes=intentos_restantes
    )

# 4. Ruta: Pantalla de Tiempo (40s)
@app.route('/orden/tiempo')
def orden_tiempo():
    """Ruta: /orden/tiempo -> tiempo.html (Pantalla de conteo/Recoja su orden)"""
    return render_template('tiempo.html')

# 5. Ruta de Cierre de Puerta
@app.route('/orden/cerrar_puerta', methods=['POST'])
def cerrar_puerta():
    """
    Ruta: Llamada por JavaScript desde tiempo.html para enviar el comando 'C' al Arduino,
    tanto por tiempo expirado como por cierre manual.
    """
    print("--- INICIANDO CIERRE DE PUERTA (Solicitud de JavaScript) ---")
    
    # Intenta enviar 'C' (Cerrar) al Arduino
    envio_exitoso = enviar_comando_arduino('C')

    if envio_exitoso:
         print("--- COMANDO ARDUINO 'C' ENVIADO CORRECTAMENTE ---")
    else:
         print("--- FALLO EN ENVÍO SERIAL. MOSTRANDO SIMULACIÓN DE CIERRE ---")
         print(ARDUINO_CODE_FAILURE)
         
    return redirect(url_for('orden_completada'))

# 6. Ruta: Pantalla de Fin
@app.route('/orden/completada')
def orden_completada():
    """Ruta: /orden/completada -> fin.html (Pantalla de finalización/Calificación)"""
    return render_template('fin.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)