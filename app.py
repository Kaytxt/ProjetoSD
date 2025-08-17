from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename 
import os 


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
    imagem_url = db.Column(db.String(200), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Tela de login
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    return render_template('index.html')


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

# Rota para adicionar uma nova moto
@app.route('/add_moto', methods=['POST'])
@login_required
def add_moto():
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    ano = request.form.get('ano')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')

    # Lógica para o upload da imagem
    imagem_salva = None
    if 'imagem' in request.files:
        imagem = request.files['imagem']
        if imagem.filename != '':
            filename = secure_filename(imagem.filename)
            upload_folder = os.path.join(app.root_path, 'static', 'uploads')
            imagem.save(os.path.join(upload_folder, filename))
            imagem_salva = filename

    nova_moto = Moto(marca=marca, modelo=modelo, ano=ano, preco=preco, descricao=descricao, imagem_url=imagem_salva)
    db.session.add(nova_moto)
    db.session.commit()

    flash('Moto adicionada com sucesso!', 'success')
    return redirect(url_for('admin_panel'))

# Rota para remover uma moto
@app.route('/delete_moto/<int:moto_id>', methods=['POST'])
@login_required
def delete_moto(moto_id):
    moto_a_remover = Moto.query.get_or_404(moto_id)

    if moto_a_remover.imagem_url:
        caminho_imagem = os.path.join(app.root_path, 'static', 'uploads', moto_a_remover.imagem_url)
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)

    db.session.delete(moto_a_remover)
    db.session.commit()
    
    flash('Moto removida com sucesso!', 'success')
    return redirect(url_for('admin_panel'))

# Rota para editar uma moto
@app.route('/edit_moto/<int:moto_id>', methods=['GET', 'POST'])
@login_required
def edit_moto(moto_id):
    moto = Moto.query.get_or_404(moto_id)
    
    if request.method == 'POST':
        # Processa o formulário enviado
        moto.marca = request.form['marca']
        moto.modelo = request.form['modelo']
        moto.ano = request.form['ano']
        moto.preco = request.form['preco']
        moto.descricao = request.form['descricao']
        
        db.session.commit()
        flash('Moto atualizada com sucesso!', 'success')
        return redirect(url_for('admin_panel'))
    
    # Renderiza a página de edição no método GET
    return render_template('edit_moto.html', moto=moto)

# Rota painel adm
@app.route('/admin')
@login_required
def admin_panel():
    motos = Moto.query.all()
    print(f"Motos encontradas no banco de dados: {motos}")
    return render_template('admin_panel.html', motos=motos)

# Rota para pagina publica
@app.route('/home')
def home():
    # Pega os termos de pesquisa do formulário (se existirem)
    marca_busca = request.args.get('marca')
    modelo_busca = request.args.get('modelo')
    ano_busca = request.args.get('ano')
    
    # Começa com uma consulta para todas as motos
    motos_query = Moto.query
    
    # Filtra com base nas info das motos
    if marca_busca:
        motos_query = motos_query.filter(Moto.marca.like(f'%{marca_busca}%'))
    if modelo_busca:
        motos_query = motos_query.filter(Moto.modelo.like(f'%{modelo_busca}%'))
    if ano_busca:
        motos_query = motos_query.filter(Moto.ano == ano_busca)
    
    motos = motos_query.all()
    
    return render_template('home.html', motos=motos)

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