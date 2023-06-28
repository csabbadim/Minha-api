from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from  model import Base

class Livro(Base):
    __tablename__ = 'livro'

    id = Column("pk_livro", Integer, primary_key=True)
    nome_livro = Column(String(140), unique=True)
    nome_autor = Column(String)
    ja_lido = Column(String)
    quer_ler = Column(String)
    previsao_leitura = Column(DateTime, default=datetime.now())

    def __init__(self, nome_livro:str, nome_autor:str, ja_lido:str, quer_ler:str,
                 previsao_leitura:Union[DateTime, None] = None):
        """
        Cria um Livro dentro da biblioteca

        Arguments:
            nome_livro: nome do livro
            nome_autor: nome do autor
            ja_lido: se o livro já foi lido
            quer_ler: se pretender ler ou reler o livro
            previsao_leitura: data de quando leu ou quando pretende ler o livro
        """
        self.nome_livro = nome_livro
        self.nome_autor = nome_autor
        self.ja_lido = ja_lido
        self.quer_ler = quer_ler
        self.previsao_leitura = previsao_leitura
