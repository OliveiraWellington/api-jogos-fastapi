
from database import obter_conexao
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Minha API de Jogos")


class Jogo(BaseModel):
    cod: int | None = None
    nome: str = Field(min_length=1, max_length=40, strip_whitespace=True)
    genero: int
    produtora: int
    descricao: str
    nota: float = Field(ge=0, le=10)
    capa: str | None = Field(default=None, max_length=40)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("O nome do jogo não pode ficar vazio.")

        return valor


class JogoCriacao(BaseModel):
    nome: str = Field(min_length=1, max_length=40)
    genero: int
    produtora: int
    descricao: str
    nota: float = Field(ge=0, le=10)
    capa: str | None = Field(default=None, max_length=40)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("O nome do jogo não pode ficar vazio.")

        return valor




@app.get("/")
def inicio():
    return {"mensagem": "Minha primeira API REST em Python!"}



@app.get("/jogos")
def listar_jogos():
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT cod, nome, genero, produtora, descricao, nota, capa
            FROM jogos
        """)
        jogos = cursor.fetchall()
        return jogos

    finally:
        cursor.close()
        conexao.close()







@app.post("/jogos", status_code=status.HTTP_201_CREATED)
def cadastrar_jogo(jogo: JogoCriacao):
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Verificar o proximo codigo
        cursor.execute(
            "SELECT COALESCE(MAX(cod), 0) + 1 AS proximo_cod FROM jogos"
        )
        resultado = cursor.fetchone()
        novo_cod = resultado["proximo_cod"]

        # Validar se o genero existe
        cursor.execute(
            "SELECT cod FROM generos WHERE cod = %s",
            (jogo.genero,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O codigo do genero nao existe."
            )

        # Validar se a produtora existe
        cursor.execute(
            "SELECT cod FROM produtoras WHERE cod = %s",
            (jogo.produtora,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O codigo da produtora nao existe."
            )

        # Cadastrar o jogo
        cursor.execute("""
            INSERT INTO jogos
                (cod, nome, genero, produtora, descricao, nota, capa)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            novo_cod,
            jogo.nome,
            jogo.genero,
            jogo.produtora,
            jogo.descricao,
            jogo.nota,
            jogo.capa
        ))

        conexao.commit()

        return {
            "mensagem": "Jogo cadastrado com sucesso!",
            "cod": novo_cod
        }

    except HTTPException:
        conexao.rollback()
        raise

    except Exception:
        conexao.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao cadastrar jogo no banco de dados."
        )

    finally:
        cursor.close()
        conexao.close()









@app.put("/jogos/{jogo_id}")
def atualizar_jogo(jogo_id: int, jogo_atualizado: JogoCriacao):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "SELECT cod FROM jogos WHERE cod = %s",
            (jogo_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="Jogo não encontrado."
            )

        # Validar gênero
        cursor.execute(
            "SELECT cod FROM generos WHERE cod = %s",
            (jogo_atualizado.genero,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=422,
                detail="O código do gênero não existe."
            )

        # Validar produtora
        cursor.execute(
            "SELECT cod FROM produtoras WHERE cod = %s",
            (jogo_atualizado.produtora,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=422,
                detail="O código da produtora não existe."
            )

        # Atualizar jogo
        cursor.execute("""
            UPDATE jogos
            SET nome = %s,
                genero = %s,
                produtora = %s,
                descricao = %s,
                nota = %s,
                capa = %s
            WHERE cod = %s
        """, (
            jogo_atualizado.nome,
            jogo_atualizado.genero,
            jogo_atualizado.produtora,
            jogo_atualizado.descricao,
            jogo_atualizado.nota,
            jogo_atualizado.capa,
            jogo_id
        ))

        conexao.commit()

        return {
            "mensagem": "Jogo atualizado com sucesso!",
            "cod": jogo_id
        }

    except HTTPException:
        conexao.rollback()
        raise

    except Exception:
        conexao.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao atualizar jogo no banco de dados."
        )

    finally:
        cursor.close()
        conexao.close()






@app.delete("/jogos/{jogo_id}")
def excluir_jogo(jogo_id: int):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "DELETE FROM jogos WHERE cod = %s",
            (jogo_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Jogo não encontrado."
            )

        conexao.commit()

        return {
            "mensagem": "Jogo excluído com sucesso!",
            "cod": jogo_id
        }

    except HTTPException:
        raise

    except Exception:
        conexao.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao excluir jogo do banco de dados."
        )

    finally:
        cursor.close()
        conexao.close()




