from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'  # Necesaria para guardar datos entre pasos

# 1. Página de Intro (Video)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Página de Inicio (Botón Empezar)
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

# 3. Paso 1: Ingresar Nombre
# Mapea a crear-orden.html
@app.route('/orden/nombre', methods=['GET', 'POST'])
def paso1_nombre():
    if request.method == 'POST':
        # Guardamos el nombre en la sesión de Python
        nombre = request.form.get('recipient_name')
        session['nombre_usuario'] = nombre
        # Python decide ir al siguiente paso
        return redirect(url_for('paso2_telefono'))
    
    return render_template('crear-orden.html')

# 4. Paso 2: Ingresar Teléfono
# Mapea a crear-orden2.html
@app.route('/orden/telefono', methods=['GET', 'POST'])
def paso2_telefono():
    if request.method == 'POST':
        telefono = request.form.get('recipient_phone')
        session['telefono_usuario'] = telefono
        return redirect(url_for('paso3_final'))
        
    return render_template('crear-orden2.html')

# 5. Paso 3: Confirmación / Piso (Final)
# Mapea a crear-orden3.html
@app.route('/orden/final', methods=['GET', 'POST'])
def paso3_final():
    if request.method == 'POST':
        # Aquí procesarías la orden final
        piso = request.form.get('floor_number')
        
        # Datos finales
        nombre = session.get('nombre_usuario')
        telefono = session.get('telefono_usuario')
        
        print(f"--- ORDEN FINALIZADA ---")
        print(f"Cliente: {nombre}")
        print(f"Teléfono: {telefono}")
        print(f"Piso: {piso}")
        print(f"------------------------")
        
        return "<h1>¡Orden Enviada al Robot JPAC2!</h1><p>Revisa la consola de Python para ver los datos.</p><a href='/inicio'>Volver</a>"
    
    # Pasamos los datos guardados a la plantilla por si queremos mostrarlos
    return render_template('crear-orden3.html', 
                           nombre=session.get('nombre_usuario'), 
                           telefono=session.get('telefono_usuario'))

if __name__ == '__main__':
    app.run(debug=True)