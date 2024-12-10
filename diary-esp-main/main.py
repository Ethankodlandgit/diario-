# Importar  
from flask import Flask, render_template, request, redirect  
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.security import generate_password_hash, check_password_hash  

app = Flask(__name__)  
# Conectando SQLite  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
# Creando una base de datos  
db = SQLAlchemy(app)  

# Creación de la tabla Card  
class Card(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  # ID  
    title = db.Column(db.String(100), nullable=False)  # Título  
    subtitle = db.Column(db.String(300), nullable=False)  # Descripción  
    text = db.Column(db.Text, nullable=False)  # Texto  

    def __repr__(self):  
        return f'<Card {self.id}>'  

# Creación de la tabla User  
class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  # ID  
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email único  
    password = db.Column(db.String(100), nullable=False)  # Contraseña hasheada  

    def __repr__(self):  
        return f'<User {self.email}>'  

# Ejecutar la página de inicio de sesión  
@app.route('/', methods=['GET', 'POST'])  
def login():  
    error = ''  
    if request.method == 'POST':  
        form_login = request.form['email']  # Captura el email del formulario  
        form_password = request.form['password']  # Captura la contraseña del formulario  
        
        # Obtener todos los usuarios de la base de datos  
        users_db = User.query.all()  
        for user in users_db:  
            if form_login == user.email and check_password_hash(user.password, form_password):  # Verificar email y contraseña  
                return redirect('/index')  # Redirigir a la página principal  

        # Si no se encuentra coincidencia, mostramos un mensaje de error  
        error = 'Nombre de usuario o contraseña incorrectos'  

    return render_template('login.html', error=error)  # Renderiza el formulario de inicio de sesión  

# Ejecutar la página de registro  
@app.route('/reg', methods=['GET', 'POST'])  
def reg():  
    if request.method == 'POST':  
        login = request.form['email']  # Captura el email del formulario  
        password = request.form['password']  # Captura la contraseña del formulario  
        
        # Crear el objeto usuario con la contraseña hasheada  
        user = User(email=login, password=generate_password_hash(password))  
        db.session.add(user)  # Añadir el usuario a la sesión  
        db.session.commit()  # Guardar cambios en la base de datos  
        
        return redirect('/')  # Redirigir a la página de inicio de sesión al finalizar el registro  
    else:    
        return render_template('registration.html')  # Renderiza el formulario de registro  

# Ejecutar la página principal  
@app.route('/index')  
def index():  
    cards = Card.query.order_by(Card.id).all()  # Obtiene todas las tarjetas de la base de datos  
    return render_template('index.html', cards=cards)  # Renderiza la página con las entradas  

# Ejecutar la página con la entrada  
@app.route('/card/<int:id>')  
def card(id):  
    card = Card.query.get(id)  # Obtiene la tarjeta correspondiente al ID  
    return render_template('card.html', card=card)  # Renderiza la página de la tarjeta  

# Ejecutar la página de creación de entradas  
@app.route('/create')  
def create():  
    return render_template('create_card.html')  # Renderiza el formulario de creación de entradas  

# El formulario para crear una tarjeta  
@app.route('/form_create', methods=['GET', 'POST'])  
def form_create():  
    if request.method == 'POST':  
        title = request.form['title']  # Captura el título de la tarjeta  
        subtitle = request.form['subtitle']  # Captura la descripción  
        text = request.form['text']  # Captura el texto  

        # Creación de un objeto que se enviará a la base de datos  
        card = Card(title=title, subtitle=subtitle, text=text)  
        db.session.add(card)  # Añadir la tarjeta a la sesión  
        db.session.commit()  # Guardar cambios en la base de datos  
        return redirect('/index')  # Redirigir a la página principal  
    else:  
        return render_template('create_card.html')  # Renderiza el formulario de creación de tarjetas  

if __name__ == "__main__":  
    # Crear todas las tablas en la base de datos (EJECUTAR UNA VEZ)  
    with app.app_context():  
        db.create_all()  # Crea las tablas  
    app.run(debug=True)  # Inicia la aplicación