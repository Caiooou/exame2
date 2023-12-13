from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask import jsonify

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/bbb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://caiohenri:ormonde7@caiohenri.mysql.pythonanywhere-services.com:3306/caiohenri$bbb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_nsenha', db.String(256))
    end = db.Column('usu_ende', db.String(256))

    def __init__(self, nome, email, senha, end):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.end = end

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__ (self, nome, desc):
        self.nome = nome
        self.desc = desc

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id


class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column('per_id', db.Integer, primary_key=True)
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))
    anu_id = db.Column('anu_id',db.Integer, db.ForeignKey("anuncio.anu_id"))
    pergunta = db.Column('per_pergunta', db.String(1024))
    resposta = db.Column('per_resposta', db.String(1024))

    def __init__(self, usu_id, anu_id, pergunta, resposta):
        self.usu_id = usu_id
        self.anu_id = anu_id
        self.pergunta = pergunta
        self.resposta = resposta


class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column('fav_id', db.Integer, primary_key=True)
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))
    anu_id = db.Column('anu_id',db.Integer, db.ForeignKey("anuncio.anu_id"))

    def __init__(self, usu_id, anu_id):
        self.usu_id = usu_id
        self.anu_id = anu_id


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cad/usuario")
def usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo="Usuario")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(request.form.get('user'), request.form.get('email'),request.form.get('senha'),request.form.get('end'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('passwd')
        usuario.end = request.form.get('end')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))

    return render_template('eusuario.html', usuario = usuario, titulo="Usuario")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))     

@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/criar", methods=['POST'])
def criaranuncio():
    anuncio = Anuncio(request.form.get('nome'), request.form.get('desc'),request.form.get('qtd'),request.form.get('preco'),request.form.get('cat'),request.form.get('uso'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncio/pergunta", methods=['POST', 'GET'])
def pergunta():
    if request.method == 'POST':
        pergunta = Pergunta(request.form.get('uso'), request.form.get('anu'), request.form.get('pergunta'), request.form.get('resposta'))
        usuario = Usuario.query.get(id)
        db.session.add(pergunta)
        db.session.commit()
    return render_template('pergunta.html', perguntas = Pergunta.query.all(), id=id)

@app.route("/anuncio/compra/<int:id>", methods=['POST', 'GET'])
def compra(id):
    anuncio = Anuncio.query.get(id)

    if anuncio.qtd > 0:
        anuncio.qtd -= 1
        db.session.commit()
        return "Compra realizada com sucesso!"
    else:
        return "Não há mais unidades disponíveis para compra."

    return redirect(url_for('anuncio'))

@app.route("/anuncio/favoritar/", methods=['POST', 'GET'])
def favorito():
    favorito = Favorito(request.form.get('uso'), request.form.get('anu'))
    db.session.add(favorito)
    db.session.commit()
    return render_template('favorito.html', id=id)

@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/relatorios/vendas")
def relVendas():
    vendas = Anuncio.query.filter(Anuncio.qtd < 10).all()
    return render_template('relVendas.html', vendas=vendas, titulo='Relatório de Vendas')

@app.route("/relatorios/compras")
def relCompras():
    compras = Anuncio.query.filter(Anuncio.qtd > 0).all()
    return render_template('relCompras.html', compras=compras, titulo='Relatório de Compras')


with app.app_context():
    db.create_all()
