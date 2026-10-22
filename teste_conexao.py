
import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="bd_games"
)

if conexao.is_connected():
    print("Conexão com o banco bd_games realizada com sucesso!")

conexao.close()
