from pydantic import BaseModel, validator
from typing import List
from model import Livro
from datetime import datetime
import re

class LivroSchema(BaseModel):
    """ Define como um novo livro a ser inserido deve ser representado
    """
    nome_livro: str = "Harry Potter"
    nome_autor: str = "JK. Rowling"
    ja_lido: str = "Sim"
    quer_ler: str = "Não"
    previsao_leitura: str = "28/06/2023"

    @validator('previsao_leitura')
    def valida_previsao_leitura(cls, v):
        if re.search("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", v):
            return v

        raise ValueError('A data precisa ser no formato dd/mm/aaaa')
    
class LivroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do livro.
    """
    nome_livro: str = "Teste de livro"

class LivroBuscaAlteraSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do livro.
    """
    nome_livro: str = "Teste de livro"
    nome_autor: str = "Nome do autor"
    ja_lido: str = ""
    quer_ler: str = ""
    previsao_leitura: str = ""

class ListagemLivrosSchema(BaseModel):
    """ Define como uma listagem de livros será retornada.
    """
    livro:List[LivroSchema]


def apresenta_livros(livros: List[Livro]):
    """ Retorna uma representação do livro seguindo o schema definido em
        LivroViewSchema.
    """
    result = []
    for livro in livros:
        result.append({
            "id": livro.id,
            "nome_livro": livro.nome_livro,
            "nome_autor": livro.nome_autor,
            "ja_lido": livro.ja_lido,
            "quer_ler":livro.quer_ler,
            "previsao_leitura":datetime.strftime(livro.previsao_leitura, '%d/%m/%Y'),
        })

    return {"livros": result}


class LivroViewSchema(BaseModel):
    """ Define como um livro será retornado
    """
    id: int = 1
    nome_livro: str = "Harry Potter"
    nome_autor: str = "JK. Rowling"
    ja_lido: str = "Sim"
    quer_ler: str = "Não"
    previsao_leitura: str = "13/06/2023"


class LivroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_livro(livro: Livro):
    """ Retorna uma representação do livro seguindo o schema definido em 
        LivroViewSchema.
    """
    return{"id": livro.id,
        "nome_livro": livro.nome_livro,
        "nome_autor": livro.nome_autor,
        "ja_lido": livro.ja_lido,
        "quer_ler":livro.quer_ler,
        "previsao_leitura": datetime.strftime(livro.previsao_leitura, '%d/%m/%Y')}
        
