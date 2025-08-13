from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Sdmotos2022'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index' 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Moto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(200), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Tela de login
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    return render_template('index.html')

# Pagina publica
@app.route('/home')
def home():
    return render_template('home.html')

# rota para processar o login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('admin_panel'))
    else:
        flash('Usuario ou senha incorretos.')
    return redirect(url_for('index'))

# Rota painel adm
@app.route('/admin')
@login_required
def admin_panel():
    return render_template('admin_panel.html')

# rota para logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='gerente').first():
            admin_user = User(username='gerente')
            admin_user.set_password('Sdmotos2022')
            db.session.add(admin_user)
            db.session.commit()
            print("Usuario 'gerente' cirado com sucesso. Senha é: 'Sdmotos2022'")

    app.run(debug=True)