from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# conección Mysql 
app.config ["MYSQL_HOST"] = 'localhost'
app.config ["MYSQL_USSER"] = 'root'
app.config ["MYSQL_PASSWORD"] = ''
app.config ["MYSQL_DB"] = 'syspe'
mysql = MySQL(app)


#Inicio Sesión
app.secret_key = 'mysecretkey'

@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('index.html', clientes = data)
    

@app.route("/altaCliente")
def altaCLiente():
    return render_template('altaCliente.html')


@app.route("/add_cliente", methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        razonsocial = request.form['razonsocial']
        nombrefantsia = request.form['nombrefantsia']
        telefono = request.form['telefono']
        cuit = request.form['cuit']
        direccion = request.form['direccion']
        mail = request.form['mail']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clientes (razonsocial, nombrefantsia, telefono, cuit, direccion, mail) VALUES (%s, %s, %s)',(razonsocial, nombrefantsia, telefono, cuit, direccion, mail))
        mysql.connection.commit ()
        flash("Contacto agregado")
        return redirect(url_for('altaCLiente'))
        

@app.route('/altaCliente')
def alta_cliente():
    return render_template('altaCliente.html')

@app.route("/edit/<id>")
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute ('SELECT * FROM clientes WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', clientes = data[0])


@app.route('/update/<id>', methods = ['POST'])
def update_clientes(id):
    if request.method == 'POST':
        razonsocial = request.form['razonsocial']
        nombrefantsia = request.form['nombrefantsia']
        telefono = request.form['telefono']
        cuit = request.form['cuit']
        direccion = request.form['direccion']
        mail = request.form['mail']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes
            SET razonsocial = %s,
                nombrefantsia =%s,
                telefono =%s,
                cuit =%s,
                direccion =%s,
                mail =%s
            WHERE id =%s

        """,  (razonsocial, nombrefantsia, telefono, cuit, direccion, mail,id))   
        mysql.connection.commit()
        flash('Cliente modificado')
        return redirect(url_for('Index'))

@app.route("/delete/<string:id>")
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id =  {0}'.format(id))
    mysql.connection.commit()
    flash('Cliente eliminado')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)