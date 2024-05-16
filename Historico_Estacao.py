import pandas as pd
import sqlite3

def historico_estacao(lista,estacao):
    df1=pd.DataFrame(lista)
    conexao = sqlite3.connect('historico.db')
    df1.to_sql(estacao, conexao, index=False, if_exists='replace')
    conexao.close()


def retorna_historico_estacao(estacao):
    conexao = sqlite3.connect('historico.db')
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM {estacao}")
    resultados = cursor.fetchall()
    conexao.close()
    lista_de_listas = [list(resultado) for resultado in resultados]
    return lista_de_listas

def consulta_tabelas():
    conexao = sqlite3.connect('historico.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    tabela_historico=[]
    for i in range(len(tabelas)):
        tabela_historico.append(tabelas[i][0])
    return tabela_historico

def apagar_tabela(nome_da_tabela):
    conexao = sqlite3.connect('historico.db')
    cursor = conexao.cursor()
    cursor.execute( f"DROP TABLE IF EXISTS {nome_da_tabela};")
    conexao.close()

arquivo='dados_R01.xlsx'
df = pd.read_excel(arquivo)

estação="Atibaia"
estação=estação.replace(" ","_")


cinco_primeiras_linhas = df.head()

# Converter as cinco primeiras linhas em uma lista de listas
#lista_de_listas = [cinco_primeiras_linhas.columns.tolist()] + cinco_primeiras_linhas.values.tolist()
#print(lista_de_listas)
#historico_estacao(lista_de_listas,estação).
#apagar_tabela(estação)
#print(consulta_tabelas())
#print(retorna_historico_estacao(estação))
#print(type(retorna_historico_estacao(estacao="Barueri")))