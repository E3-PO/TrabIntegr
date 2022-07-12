#from crypt import methods
from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Contrasiñal"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema_socios'
mysql.init_app(app)

@app.route('/')
def index():
    sql = "SELECT * FROM socios;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    socios = cursor.fetchall()
    conn.commit()
    return render_template('socios/index.html', socios=socios)

@app.route('/create')
def create():
    return render_template('socios/create.html')

@app.route('/store', methods=['POST'])
def store():
    _apellido=request.form['txtApellido']
    _nombres=request.form['txtNombres']
    _categoria=request.form['txtCat']
    now=datetime.now()
    _inscripcion=now.strftime("%d"+"/"+"%m"+"/"+"%Y")
    _categoria=request.form['txtCat']
    sql = "INSERT INTO socios (apellido, nombres, categoría, fecha_inscripción) VALUES (%s,%s,%s, %s);"
    datos=(_apellido, _nombres, _categoria, _inscripcion)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

@app.route('/destroy/<int:socio_nro>')
def destroy(socio_nro):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM socios WHERE socio_nro=%s;", socio_nro)
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:socio_nro>')
def edit(socio_nro):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM socios WHERE socio_nro=%s;", socio_nro)
    socios=cursor.fetchall()
    conn.commit()
    return render_template('socios/edit.html', socios=socios)

@app.route('/update', methods=['POST'])
def update():
    _apellido=request.form['txtApellido']
    _nombres=request.form['txtNombres']
    _inscripcion=request.form['datInscripcion']
    _categoria=request.form['txtCat']
    now=datetime.now()
    id=request.form['txtID']
    sql = "UPDATE socios SET apellido=%s, nombres=%s, categoría=%s, fecha_inscripción=%s WHERE socio_nro=%s;"
    datos=(_apellido, _nombres, _categoria, _inscripcion, id)
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)