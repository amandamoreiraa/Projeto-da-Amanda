from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user, logout_user
import sqlite3

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)
lm = LoginManager(app)

@lm.user_loader
def get_user(cliente_id):
	return Cliente.query.filter_by(id=cliente_id).first()

class Cliente(db.Model):
	__tablename__ = 'clientes'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome = db.Column(db.String(45), nullable=True)
	email = db.Column(db.String(150), nullable=True, unique=True)
	pais = db.Column(db.String(45), nullable=True)
	estado = db.Column(db.String(45), nullable=True)
	municipio = db.Column(db.String(45), nullable=True)
	cep = db.Column(db.String(45), nullable=True)
	rua = db.Column(db.String(150), nullable=True)
	numero = db.Column(db.String(150), nullable=True)
	complemento = db.Column(db.String(45), nullable=False)
	cpf = db.Column(db.String(11), nullable=True, unique=True)
	pis = db.Column(db.String(150), nullable=True, unique=True)
	senha = db.Column(db.String(150), nullable=True, unique=True)


	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False
	
	@property
	def get_id(self):
		return str(self.id)	
	

	
	def __init__(self, nome,email, pais, estado, municipio, cep, rua, numero,
		complemento, cpf, pis, senha):
		self.nome = nome
		self.email = email
		self.pais = pais
		self.estado = estado
		self.municipio = municipio
		self.cep = cep
		self.rua = rua
		self.numero = numero
		self.complemento = complemento
		self.cpf = cpf
		self.pis = pis
		self.senha = senha


@app.route('/index')
def index():
	clientes = Cliente.query.all()
	return render_template('index.html', clientes=clientes)

@app.route('/', methods=['GET', 'POST'])
def home():
	clientes = Cliente.query.all()
	return render_template('home.html', clientes=clientes)	


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		cpf = request.form['cpf']
		pis = request.form['pis']
		senha = request.form['senha']
		
		cliente = Cliente.query.filter_by(email=email, cpf=cpf, pis=pis).first()

        
		return redirect(url_for('home'))

	return render_template('login.html')


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))



@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
	if request.method == 'POST':
		cliente = Cliente(
				request.form['nome'], 
				request.form['email'],
        		request.form['pais'],
        		request.form['estado'],
        		request.form['municipio'],
        		request.form['cep'],
        		request.form['rua'],
        		request.form['numero'],
	    		request.form['complemento'],
	    		request.form['cpf'],
	    		request.form['pis'],
				request.form['senha'])
		db.session.add(cliente)
		db.session.commit()
		return redirect(url_for('index'))
	return	render_template('cadastrarcliente.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
	cliente = Cliente.query.get(id)
	if request.method == 'POST':
		cliente.nome = request.form['nome']
		cliente.email = request.form['email']
		cliente.pais = request.form['pais']
		cliente.estado = request.form['estado']
		cliente.municipio = request.form['municipio']
		cliente.cep = request.form['cep']
		cliente.rua = request.form['rua']
		cliente.numero = request.form['numero']
		cliente.complemento = request.form['complemento']
		cliente.cpf = request.form['cpf']
		cliente.pis = request.form['pis']
		cliente.senha = request.form['senha']
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('editarcliente.html',cliente=cliente)	


@app.route('/excluir/<int:id>')
def excluir(id):
	cliente = Cliente.query.get(id)	
	db.session.delete(cliente)
	db.session.commit()
	return redirect(url_for('cadastro'))


if __name__ == '__main__':
	db.create_all()	
	app.run(debug=True)		