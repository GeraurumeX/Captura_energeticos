from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL Connection
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'energy_consumption'
mysql.init_app(app)

# Settings
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM monthly_consumption_energy')
    data = cursor.fetchall()
    return render_template('index.html', consumptions=data)

# Agregar equipos
@app.route('/add_consumption', methods=['POST'])
def add_consumption():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        water_consumption = request.form['water_consumption']
        electricity_consumption = request.form['electricity_consumption']
        gasoline_consumption = request.form['gasoline_consumption']
        gas_consumption = request.form['gas_consumption']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO monthly_consumption_energy (year, month, water_consumption, electricity_consumption, gasoline_consumption, gas_consumption) VALUES (%s, %s, %s, %s, %s, %s)',
                       (year, month, water_consumption, electricity_consumption, gasoline_consumption, gas_consumption))
        conn.commit()
        conn.close()
        flash('Consumption Added Successfully')
        return redirect(url_for('Index'))

# Obtener equipo para editar
@app.route('/edit/<id>')
def get_consumption(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM monthly_consumption_energy WHERE id = %s', (id))
    data = cursor.fetchall()
    return render_template('edit_consumption.html', consumption=data[0])


# Update equipo
@app.route('/update/<id>', methods=['POST'])
def update_consumption(id):
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        water_consumption = request.form['water_consumption']
        electricity_consumption = request.form['electricity_consumption']
        gasoline_consumption = request.form['gasoline_consumption']
        gas_consumption = request.form['gas_consumption']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE monthly_consumption_energy
            SET year = %s,
                month = %s,
                water_consumption = %s,
                electricity_consumption = %s,
                gasoline_consumption = %s,
                gas_consumption = %s
            WHERE id = %s
        """, (year, month, water_consumption, electricity_consumption, gasoline_consumption, gas_consumption, id))
        conn.commit()
        conn.close()
        flash('Consumption Update Successfully')
        return redirect(url_for('Index'))

# Borrar equipos
@app.route('/delete/<string:id>')
def delete_consumption(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM monthly_consumption_energy WHERE id = {0}'.format(id))
    conn.commit()
    conn.close()
    flash('Consumption Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
