#from email.mime import base
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Livro
from logger import logger
from schemas import *
from flask_cors import CORS

from datetime import datetime

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
livro_tag = Tag(name="Livro", description="Adição, visualização e remoção de livros à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/livro', tags=[livro_tag],
          responses={"200": LivroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_livro(form: LivroSchema):
    """Adiciona um novo livro à base de dados

    Retorna uma representação dos livros cadastrados
    """
    # criando conexão com a base
    session = Session()
    livro = Livro(
        nome_livro=form.nome_livro,
        nome_autor=form.nome_autor,
        ja_lido=form.ja_lido,
        quer_ler=form.quer_ler,
        previsao_leitura=datetime.strptime(form.previsao_leitura, '%d/%m/%Y')
        )
    logger.debug(f"Adicionando livro: '{livro.nome_livro}'")
    try:
        
        # adicionando livro
        session.add(livro)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado livro: '{livro.nome_livro}'")
        return apresenta_livro(livro), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Já existe um livro com o mesmo nome na base, favor verificar :)"
        logger.warning(f"Erro ao adicionar o livro: '{livro.nome_livro}', na biblioteca. {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não conseguimos salvar seu livro na base :/"
        logger.warning(f"Erro ao adicionar o livro: '{livro.nome_livro}', na biblioteca. {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/livros', tags=[livro_tag],
         responses={"200": ListagemLivrosSchema, "404": ErrorSchema})
def get_livros():
    """Faz a busca por todos os Livros cadastrados na base de dados

    Retorna uma representação da listagem de livros.
    """
    logger.debug(f"Coletando livros ")
   # criando conexão com a base
    session = Session()
    # fazendo a busca
    livros = session.query(Livro).all()

    if not livros:
        # se não há livros cadastrados
        return {"livros": []}, 200
    else:
        logger.debug(f"%d livros econtrados" % len(livros))
        # retorna a representação de livro
        print(livros)
        return apresenta_livros(livros), 200
    

@app.delete('/livro', tags=[livro_tag],
            responses={"200": LivroDelSchema, "404": ErrorSchema})
def del_livro(query: LivroBuscaSchema):
    """Deleta um livro a partir do nome do livro informado

    Retorna uma mensagem de confirmação da remoção.
    """
    livro_nome = unquote(unquote(query.nome_livro))
    print(livro_nome)
    logger.debug(f"Deletando dados sobre o livro #{livro_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Livro).filter(Livro.nome_livro == livro_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado livro #{livro_nome}")
        return {"mesage": "Livro removido", "nome do livro": livro_nome}
    else:
        # se o livro não foi encontrado
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao deletar livro #'{livro_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.put('/alteralivro', tags=[livro_tag],
         responses={"200": LivroViewSchema, "404": ErrorSchema})
def altera_livro(query: LivroBuscaAlteraSchema):
    """Busca um livro e alterar a partir de seu nome

    Retorna uma representação do livro alterado
    """
    nome_livro = query.nome_livro
    nome_autor = query.nome_autor
    ja_lido = query.ja_lido
    quer_ler = query.quer_ler
    previsao_leitura = datetime.strptime(query.previsao_leitura, '%d/%m/%Y')
    logger.debug(f"Coletando dados sobre o livro: #{nome_livro}")
    session = Session()
    livro = session.query(Livro).filter(Livro.nome_livro == nome_livro).first()

    if not livro:
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao buscar livro '{nome_livro}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"O livro: '{livro.nome_livro}', foi encontrado! :)")

        if ja_lido.lower() == "sim":
            livro.ja_lido = "Sim"
        elif ja_lido.lower() == "não" or ja_lido.lower() == "nao":
            livro.ja_lido = "Não"
        elif ja_lido != "":
            error_msg = "Favor preencher o campo 'ja_lido' com 'Sim' ou 'Não'."
            logger.warning(f"{error_msg} Livro: '{livro.nome_livro}'")
            return {"message": error_msg}, 400

        if quer_ler.lower() == "sim":
            livro.quer_ler = "Sim"
        elif quer_ler.lower() == "não" or quer_ler.lower() == "nao":
            livro.quer_ler = "Não"
        elif quer_ler != "":
            error_msg = "Favor preencher o campo 'quer_ler' com 'Sim' ou 'Não'."
            logger.warning(f"{error_msg} Livro: '{livro.nome_livro}'")
            return {"message": error_msg}, 400

        livro.previsao_leitura = previsao_leitura
    try:
        session.commit()
        logger.debug(f"Livro '{livro.nome_livro}' atualizado com sucesso")
        return apresenta_livro(livro), 200
    except Exception as e:
        error_msg = "Não foi possível atualizar o livro na base :/"
        logger.warning(f"Erro ao atualizar livro '{livro.nome_livro}', {error_msg}")
        return {"message": error_msg}, 400
