from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/database/farmacia.db'
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Crear la carpeta database si no existe
if not os.path.exists('database'):
    os.makedirs('database')

# BASE DE DATOS
class Especialidades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    medicos = db.relationship('Medicos', backref='especialidad', lazy=True, cascade="all, delete-orphan")

class Estatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    medicos = db.relationship('Medicos', backref='estatus', lazy=True, cascade="all, delete-orphan")

class Medicos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ap = db.Column(db.String(100), nullable=False)
    am = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    estatus_id = db.Column(db.Integer, db.ForeignKey('estatus.id'), nullable=False)
    recetas = db.relationship('Recetas', backref='medico', lazy=True, cascade="all, delete-orphan")

class Pacientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ap = db.Column(db.String(100), nullable=False)
    am = db.Column(db.String(100), nullable=False)
    fecha_nac = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    recetas = db.relationship('Recetas', backref='paciente', lazy=True, cascade="all, delete-orphan")

class Recetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    detalles = db.relationship('Detalles_receta', backref='receta', lazy=True, cascade="all, delete-orphan")

class Medicamentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    detalles = db.relationship('Detalles_receta', backref='medicamento', lazy=True, cascade="all, delete-orphan")

class Detalles_receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'), nullable=False)
    dosis = db.Column(db.String(100), nullable=False)
    frecuencia = db.Column(db.String(100), nullable=False)
    duracion = db.Column(db.String(100), nullable=False)

class Empleados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    ap = db.Column(db.String(50), nullable=False)
    am = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    ventas = db.relationship('Ventas', backref='empleado', lazy=True, cascade="all, delete-orphan")

class Ventas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

# --- ESPECIALIDADES ---
@app.route('/especialidades')
def especialidades():
    especialidades = Especialidades.query.all()
    return render_template('especialidades.html', especialidades=especialidades)

# Crear especialidades
@app.route('/crear_especialidad', methods=['POST'])
def crear_especialidad():
    especialidad = Especialidades(nombre=request.form['nom_esp'])
    db.session.add(especialidad)
    db.session.commit()
    return redirect(url_for('especialidades'))

# Editar especialidad
@app.route('/editar_especialidad/<int:id>')
def editar_especialidad(id):
    especialidad = Especialidades.query.get(id)
    return render_template('editar_especialidad.html', especialidad=especialidad)

# Actualizar especialidades
@app.route('/actualizar_especialidad/<int:id>', methods=['POST'])
def actualizar_especialidad(id):
    especialidad = Especialidades.query.get(id)
    if especialidad:
        especialidad.nombre = request.form['nom_esp']
        db.session.commit()
    return redirect(url_for('especialidades'))

# Borrar especialidades
@app.route('/borrar_especialidad/<int:id>', methods=['POST'])
def borrar_especialidad(id):
    especialidad = Especialidades.query.get(id)
    if especialidad:
        db.session.delete(especialidad)
        db.session.commit()
    return redirect(url_for('especialidades'))

# --- ESTATUS ---
@app.route('/estatus')
def estatus():
    estatus = Estatus.query.all()
    return render_template('estatus.html', estatus=estatus)

# Crear estatus
@app.route('/crear_estatus', methods=['POST'])
def crear_estatus():
    estatus = Estatus(nombre=request.form['nom_estatus'])
    db.session.add(estatus)
    db.session.commit()
    return redirect(url_for('estatus'))

# Editar estatus
@app.route('/editar_estatus/<int:id>')
def editar_estatus(id):
    estatus = Estatus.query.get(id)
    return render_template('editar_estatus.html', estatus=estatus)

# Actualizar estatus
@app.route('/actualizar_estatus/<int:id>', methods=['POST'])
def actualizar_estatus(id):
    estatus = Estatus.query.get(id)
    if estatus:
        estatus.nombre = request.form['nom_estatus']
        db.session.commit()
    return redirect(url_for('estatus'))

# Borrar estatus
@app.route('/borrar_estatus/<int:id>', methods=['POST'])
def borrar_estatus(id):
    estatus = Estatus.query.get(id)
    if estatus:
        db.session.delete(estatus)
        db.session.commit()
    return redirect(url_for('estatus'))

# --- MEDICOS ---

@app.route('/medicos')
def medicos():
    medicos = Medicos.query.all()
    especialidades = Especialidades.query.all()
    estatus = Estatus.query.all()
    return render_template('medicos.html', medicos=medicos, especialidades=especialidades, estatus=estatus)

@app.route('/crear_medico', methods=['POST'])
def crear_medico():
    medico = Medicos(
        nombre=request.form['nombre'],
        ap=request.form['ap'],
        am=request.form['am'],
        telefono=request.form['telefono'],
        correo_electronico=request.form['correo_electronico'],
        especialidad_id=request.form['especialidad_id'],
        estatus_id=request.form['estatus_id']
    )
    db.session.add(medico)
    db.session.commit()
    return redirect(url_for('medicos'))

@app.route('/editar_medico/<int:id>')
def editar_medico(id):
    medico = Medicos.query.get(id)
    especialidades = Especialidades.query.all()
    estatus = Estatus.query.all()
    return render_template('editar_medico.html', medico=medico, especialidades=especialidades, estatus=estatus)

@app.route('/actualizar_medico/<int:id>', methods=['POST'])
def actualizar_medico(id):
    medico = Medicos.query.get(id)
    if medico:
        medico.nombre = request.form['nombre']
        medico.ap = request.form['ap']
        medico.am = request.form['am']
        medico.telefono = request.form['telefono']
        medico.correo_electronico = request.form['correo_electronico']
        medico.especialidad_id = request.form['especialidad_id']
        medico.estatus_id = request.form['estatus_id']
        db.session.commit()
    return redirect(url_for('medicos'))


@app.route('/borrar_medico/<int:id>', methods=['POST'])
def borrar_medico(id):
    medico = Medicos.query.get(id)
    if medico:
        db.session.delete(medico)
        db.session.commit()
    return redirect(url_for('medicos'))

# --- PACIENTES ---

@app.route('/pacientes')
def pacientes():
    pacientes = Pacientes.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/crear_paciente', methods=['POST'])
def crear_paciente():
    fecha_nac = datetime.strptime(request.form['fecha_nac'], '%Y-%m-%d').date()
    paciente = Pacientes(
        nombre=request.form['nombre'],
        ap=request.form['ap'],
        am=request.form['am'],
        fecha_nac=fecha_nac,
        genero=request.form['genero'],
        telefono=request.form['telefono'],
        correo=request.form['correo']
    )
    db.session.add(paciente)
    db.session.commit()
    return redirect(url_for('pacientes'))

@app.route('/editar_paciente/<int:id>')
def editar_paciente(id):
    paciente = Pacientes.query.get(id)
    return render_template('editar_paciente.html', paciente=paciente)

@app.route('/actualizar_paciente/<int:id>', methods=['POST'])
def actualizar_paciente(id):
    paciente = Pacientes.query.get(id)
    if paciente:
        paciente.nombre = request.form['nombre']
        paciente.ap = request.form['ap']
        paciente.am = request.form['am']
        paciente.fecha_nac = datetime.strptime(request.form['fecha_nac'], '%Y-%m-%d').date()
        paciente.genero = request.form['genero']
        paciente.telefono = request.form['telefono']
        paciente.correo = request.form['correo']
        db.session.commit()
    return redirect(url_for('pacientes'))

@app.route('/borrar_paciente/<int:id>', methods=['POST'])
def borrar_paciente(id):
    paciente = Pacientes.query.get(id)
    if paciente:
        db.session.delete(paciente)
        db.session.commit()
    return redirect(url_for('pacientes'))

# --- RECETAS ---
@app.route('/recetas')
def recetas():
    recetas = Recetas.query.all()
    pacientes = Pacientes.query.all()
    medicos = Medicos.query.all()
    return render_template('recetas.html', recetas=recetas, pacientes=pacientes, medicos=medicos)

@app.route('/crear_receta', methods=['POST'])
def crear_receta():
    fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
    receta = Recetas(
        fecha=fecha,
        paciente_id=request.form['paciente_id'],
        medico_id=request.form['medico_id']
    )
    db.session.add(receta)
    db.session.commit()
    return redirect(url_for('recetas'))

@app.route('/editar_receta/<int:id>')
def editar_receta(id):
    receta = Recetas.query.get(id)
    pacientes = Pacientes.query.all()
    medicos = Medicos.query.all()
    return render_template('editar_receta.html', receta=receta, pacientes=pacientes, medicos=medicos)

@app.route('/actualizar_receta/<int:id>', methods=['POST'])
def actualizar_receta(id):
    receta = Recetas.query.get(id)
    if receta:
        receta.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        receta.paciente_id = request.form['paciente_id']
        receta.medico_id = request.form['medico_id']
        db.session.commit()
    return redirect(url_for('recetas'))

@app.route('/borrar_receta/<int:id>', methods=['POST'])
def borrar_receta(id):
    receta = Recetas.query.get(id)
    if receta:
        db.session.delete(receta)
        db.session.commit()
    return redirect(url_for('recetas'))

# --- MEDICAMENTOS ---
@app.route('/medicamentos')
def medicamentos():
    medicamentos = Medicamentos.query.all()
    return render_template('medicamentos.html', medicamentos=medicamentos)

# Crear medicamento
@app.route('/crear_medicamento', methods=['POST'])
def crear_medicamento():
    medicamento = Medicamentos(
        nombre=request.form['nombre'],
        descripcion=request.form.get('descripcion', '')  # descripción puede ser vacía
    )
    db.session.add(medicamento)
    db.session.commit()
    return redirect(url_for('medicamentos'))

# Editar medicamento
@app.route('/editar_medicamento/<int:id>')
def editar_medicamento(id):
    medicamento = Medicamentos.query.get(id)
    return render_template('editar_medicamento.html', medicamento=medicamento)

# Actualizar medicamento
@app.route('/actualizar_medicamento/<int:id>', methods=['POST'])
def actualizar_medicamento(id):
    medicamento = Medicamentos.query.get(id)
    if medicamento:
        medicamento.nombre = request.form['nombre']
        medicamento.descripcion = request.form.get('descripcion', '')  # descripción puede ser vacía
        db.session.commit()
    return redirect(url_for('medicamentos'))

# Borrar medicamento
@app.route('/borrar_medicamento/<int:id>', methods=['POST'])
def borrar_medicamento(id):
    medicamento = Medicamentos.query.get(id)
    if medicamento:
        db.session.delete(medicamento)
        db.session.commit()
    return redirect(url_for('medicamentos'))

# --- DETALLES_RECETAS
@app.route('/detalles_receta')
def detalles_receta():
    detalles = Detalles_receta.query.all()
    recetas = Recetas.query.all()
    medicamentos = Medicamentos.query.all()
    return render_template('detalles_receta.html', detalles=detalles, recetas=recetas, medicamentos=medicamentos)

# Crear detalles de receta
@app.route('/crear_detalle_receta', methods=['POST'])
def crear_detalle_receta():
    detalle = Detalles_receta(
        receta_id=request.form['receta_id'],
        medicamento_id=request.form['medicamento_id'],
        dosis=request.form['dosis'],
        frecuencia=request.form['frecuencia'],
        duracion=request.form['duracion']
    )
    db.session.add(detalle)
    db.session.commit()
    return redirect(url_for('detalles_receta'))

# Editar detalle de receta
@app.route('/editar_detalle_receta/<int:id>')
def editar_detalle_receta(id):
    detalle = Detalles_receta.query.get(id)
    if detalle:
        recetas = Recetas.query.all()
        medicamentos = Medicamentos.query.all()
        return render_template('editar_detalle_receta.html', detalle=detalle, recetas=recetas, medicamentos=medicamentos)
    return redirect(url_for('detalles_receta'))


# Actualizar detalle de receta
@app.route('/actualizar_detalle_receta/<int:id>', methods=['POST'])
def actualizar_detalle_receta(id):
    detalle = Detalles_receta.query.get(id)
    if detalle:
        detalle.receta_id = request.form['receta_id']
        detalle.medicamento_id = request.form['medicamento_id']
        detalle.dosis = request.form['dosis']
        detalle.frecuencia = request.form['frecuencia']
        detalle.duracion = request.form['duracion']
        db.session.commit()
    return redirect(url_for('detalles_receta'))

# Borrar detalle de receta
@app.route('/borrar_detalle_receta/<int:id>', methods=['POST'])
def borrar_detalle_receta(id):
    detalle = Detalles_receta.query.get(id)
    if detalle:
        db.session.delete(detalle)
        db.session.commit()
    return redirect(url_for('detalles_receta'))

# --- EMPLEADOS ---

# Listar empleados
@app.route('/empleados')
def empleados():
    empleados = Empleados.query.all()
    return render_template('empleados.html', empleados=empleados)

# Crear empleado
@app.route('/crear_empleado', methods=['POST'])
def crear_empleado():
    empleado = Empleados(
        nombre=request.form['nombre'],
        ap=request.form['ap'],
        am=request.form['am'],
        telefono=request.form['telefono'],
        correo=request.form['correo']
    )
    db.session.add(empleado)
    db.session.commit()
    return redirect(url_for('empleados'))

# Editar empleado
@app.route('/editar_empleado/<int:id>')
def editar_empleado(id):
    empleado = Empleados.query.get(id)
    return render_template('editar_empleado.html', empleado=empleado)

# Actualizar empleado
@app.route('/actualizar_empleado/<int:id>', methods=['POST'])
def actualizar_empleado(id):
    empleado = Empleados.query.get(id)
    if empleado:
        empleado.nombre = request.form['nombre']
        empleado.ap = request.form['ap']
        empleado.am = request.form['am']
        empleado.telefono = request.form['telefono']
        empleado.correo = request.form['correo']
        db.session.commit()
    return redirect(url_for('empleados'))

# Borrar empleado
@app.route('/borrar_empleado/<int:id>', methods=['POST'])
def borrar_empleado(id):
    empleado = Empleados.query.get(id)
    if empleado:
        db.session.delete(empleado)
        db.session.commit()
    return redirect(url_for('empleados'))

# --- VENTAS ---

# Listar ventas
@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    if request.method == 'POST':
        empleado_id = request.form['empleado_id']
        fecha_str = request.form['fecha']

        # Convertir la fecha de cadena a objeto date
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        nueva_venta = Ventas(empleado_id=empleado_id, fecha=fecha)
        db.session.add(nueva_venta)
        db.session.commit()
        return redirect(url_for('ventas'))

    ventas = Ventas.query.all()
    empleados = Empleados.query.all()
    return render_template('ventas.html', ventas=ventas, empleados=empleados)


# Crear venta
@app.route('/crear_venta', methods=['POST'])
def crear_venta():
    empleado_id = request.form['empleado_id']
    fecha_str = request.form['fecha']

    # Convertir la fecha de cadena a objeto date
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

    venta = Ventas(
        empleado_id=empleado_id,
        fecha=fecha
    )
    db.session.add(venta)
    db.session.commit()
    return redirect(url_for('ventas'))


# Editar venta
@app.route('/editar_venta/<int:id>')
def editar_venta(id):
    venta = Ventas.query.get(id)
    empleados = Empleados.query.all()
    return render_template('editar_venta.html', venta=venta, empleados=empleados)


# Actualizar venta
@app.route('/actualizar_venta/<int:id>', methods=['POST'])
def actualizar_venta(id):
    venta = Ventas.query.get(id)
    if venta:
        venta.empleado_id = request.form['empleado_id']

        # Convertir la fecha de cadena a objeto date
        fecha_str = request.form['fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        venta.fecha = fecha

        db.session.commit()
    return redirect(url_for('ventas'))


# Borrar venta
@app.route('/borrar_venta/<int:id>', methods=['POST'])
def borrar_venta(id):
    venta = Ventas.query.get(id)
    if venta:
        db.session.delete(venta)
        db.session.commit()
    return redirect(url_for('ventas'))

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database Created")
        except Exception as e:
            print(f"Error: {e}")
    app.run(debug=True)
