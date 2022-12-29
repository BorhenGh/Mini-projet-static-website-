from flask import Flask, render_template, request, flash, url_for, session

from flask_mysqldb import MySQL
import os

import MySQLdb
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hightec'
mysql = MySQL(app)








@app.route('/')
@app.route('/Accueil.html')
def Accueil():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Produit ')

    # Fetch one record and return result
    Produits = cursor.fetchall()

    return render_template('Reseau&Connectiques.html', Produits=Produits)
    return render_template('Accueil.html')
@app.route('/contact.html')
def Contact():
    return render_template('contact.html')

@app.route('/Reseau&Connectiques.html')
def Reseau():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Produit WHERE cat = 4 ')

    # Fetch one record and return result
    Produits = cursor.fetchall()

    return render_template('Reseau&Connectiques.html',Produits=Produits)
@app.route('/Informatique.html')
def Informatique():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Produit WHERE cat = 1 ')

    # Fetch one record and return result
    Produits = cursor.fetchall()

    return render_template('Informatique.html',Produits=Produits)
@app.route('/Tv&Son.html')
def Tv():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Produit WHERE cat = 3 ')

    # Fetch one record and return result
    Produits = cursor.fetchall()
    return render_template('Tv&Son.html',Produits=Produits)
@app.route('/Add.html')
def Add():
    return render_template('Add.html')
@app.route('/Add.html',methods=['POST'])
def AjouterProduit():
    nom=request.form['nomp']
    prix=request.form['prix']
    quantite=request.form['quantite']
    image=request.form['image']
    cat=request.form['categorie']
    cursor = mysql.connection.cursor()
    cursor.execute('''insert into produit(nom, prix,quantite,image,cat) values (%s,%s,%s,%s,%s);''', [nom, prix,quantite,image,cat])
    mysql.connection.commit()
    message='Produit ajouté avec succès'
    return redirect(url_for('Accueil'))


@app.route('/Télephonie&Tablette.html')
def Telephonie():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Produit WHERE cat = 2 ')

    # Fetch one record and return result
    produits = cursor.fetchall()


    return render_template('Télephonie&Tablette.html',produits=produits)
@app.route('/Authentification.html', methods=['GET', 'POST'])
def Authentification():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE login = %s AND password = %s', (username, password,))

        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['login']
            session['role'] = account['role']
            # Redirect to home page
            return redirect(url_for('Add'))
        else:
            message="Login ou mots de passe incorrect"
            return render_template('Authentification.html',message=message)
    return render_template('Authentification.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    # Redirect to login page
    return redirect(url_for('Authentification'))

@app.route('/Register.html',methods=['GET','POST'])
def RegisterUser():
 if request.method == 'POST':
    nom= request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    login = request.form['login']
    password = request.form['password']
    role = request.form['role']
    cursor = mysql.connection.cursor()
    cursor.execute('''insert into User(nom, prenom,email,login,password,role) values (%s,%s,%s,%s,%s,%s);''',
                       [nom, prenom,email,login,password,role])
    mysql.connection.commit()
    message = 'User ajouté avec succès'
    return redirect(url_for('Authentification'))

 else:
    return render_template('Register.html')

if __name__ == '__main__':

    app.run(debug=True, port=3000)
