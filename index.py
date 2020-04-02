
#Jonathan Carrasco Toledo - 19.906.880-6

from datetime import date
from flask import Flask, render_template, jsonify, request, url_for, redirect, flash
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_DB"]  = "centrovacunas"

mysql = MySQL(app)
mysql.connect_args["autocommit"] = True
mysql.connect_args["cursorclass"] = pymysql.cursors.DictCursor

app.secret_key = "mysecretkey"

#Ruta principal que mostrara a los pacientes
@app.route('/')
def index():

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM paciente")
    pacientesdb = cursor.fetchall()
    return render_template('paciente.html', pacientes = pacientesdb)

#Mostrara el historial de X paciente
@app.route('/historial/<string:id>')
def historial_paciente(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT r.nombre_enfermedad, r.fecha_vacuna, p.nombre_pac FROM recibe_vacuna r, paciente p WHERE r.rut_pac = {0} and p.rut_pac = {0}'.format(id) )
    recibe_vacuna = cursor.fetchall()
    return render_template('paciente_historial.html', vacuna = recibe_vacuna)

#funcion para mostrar vacunas en formulario
@app.route('/vacunar/<id>', methods = ['POST', 'GET'])
def vacunar(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT nombre_enfermedad FROM vacuna")
    vacunasdb = cursor.fetchall()
    return render_template('paciente_vacunar.html', vacunas = vacunasdb, rut = id )

#funcion que recibe datos del formulario
@app.route('/paciente_vacunado', methods = ['POST'])
def vacunado():
    if request.method == 'POST':
        cursor = mysql.get_db().cursor()
        rut = request.form['id']
        vacuna = request.form['vacuna']
        fecha = date.today()
        cursor.execute('INSERT INTO recibe_vacuna VALUES (%s, %s, %s)', (rut, vacuna, fecha))
    return redirect(url_for('index'))


#Formulario para ingresar pacientes
@app.route('/agregar_paciente')
def agregar_paciente():
    return render_template('paciente_agregar.html')

#Recoje los datos e ingrsa paciente a la BD
@app.route('/agregar_pac', methods = ['POST'])
def agregar_pac():
    if request.method == 'POST':
        cursor = mysql.get_db().cursor()
        rut = request.form['rut_pac']
        nombre = request.form['nombre_pac']
        nacimiento = request.form['f_nacimiento']
        cursor.execute('INSERT INTO paciente VALUES (%s,%s,%s)', (nombre, rut, nacimiento))
    return redirect(url_for('index'))




#Ruta secundaria que mostrara todas las vacunas y su fecha de ingreso
@app.route('/vacunas_disponibles')
def vacunas_disponibles():

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM vacuna")
    vacunasdb = cursor.fetchall()
    return render_template('vacuna.html', vacunas = vacunasdb)

#Formulario para ingresar nueva vacuna
@app.route('/nueva_vacuna')
def nueva_vacuna():
    return render_template('vacuna_agregar.html')

#Toma los datos del formulario y los ingresa al BD
@app.route('/agregar_vacuna', methods = ['POST'])
def agregar_vacuna():
    if request.method == 'POST':
        cursor = mysql.get_db().cursor()
        nombre_enfermedad = request.form['nombre_enfermedad']
        fecha = date.today()
        cursor.execute('INSERT INTO vacuna VALUES (%s,%s)', (nombre_enfermedad, fecha))
    return redirect(url_for('vacunas_disponibles'))

#Mostrara el historial de X vacuna
@app.route('/historialvacuna/<string:id>')
def historial_vacuna(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT r.rut_pac, p.nombre_pac, r.fecha_vacuna FROM recibe_vacuna r, paciente p WHERE nombre_enfermedad = %s and p.rut_pac = r.rut_pac",(id) )
    recibe_vacuna = cursor.fetchall()
    return render_template('vacuna_historial.html', vacunados = recibe_vacuna)



#modo pruebass
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
