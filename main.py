import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
from tkinter import messagebox
from classificacao_lista_ip import gerar_sistemas_ip
from gerador_excel import Lista_equipamentos
from Plano_integração import Gerar_Plano_integração
from Caminhos_documentos import caminho_template_plano_integração,caminho_consulta_plano_integração
from Historico_Estacao import consulta_tabelas
def gerador_ips(ip_inicial,quantidade):
  lista_ip=[]
  for i in range(0, quantidade):
      lista_ip.append(f"{ip_inicial.rsplit('.', 1)[0]}.{int(ip_inicial.rsplit('.', 1)[1]) + i}")
  return lista_ip

def on_select(event):
   
    if listbox.curselection():
        # Se houver uma seleção, habilita o botão
        botao_excel.config(state=tk.NORMAL)
    else:
        # Se não houver seleção, desabilita o botão
        botao_excel.config(state=tk.DISABLED)
    
def adicionar_dados():
    sistema              =   entrada_sistema.get()
    subsistema           =   entrada_subsistema.get()
    equipamento          =   entrada_equipamento.get()
    protocolo            =   entrada_protocolo.get()
    modelo               =   entrada_modelo.get()
    fabricante           =   entrada_fabricante.get()
    meio_fisico          =   entrada_meio.get()
    descricao            =   entrada_descricao.get()
    subsistema           =   entrada_subsistema.get()
    sistemas_lista_ip    =   entrada_sistema_lista_ips.get()
    grupo_equipamento_ip =   entrada_grupo_ip.get()
    
    # Conexão com o banco de dados SQLite3
    conexao = sqlite3.connect('dados.db')
    
    # Cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Comando SQL para inserir dados na tabela
   
    # Executar o comando SQL para inserir os dados
    cursor.execute( "INSERT INTO tabela_dados (Sistema, EQUIPAMENTO, PROTOCOLO, MODELO, FABRICANTE, MEIO_FISICO, DESCRIÇÃO, SUBSISTEMA, Sistemas_Lista_de_Ips, Grupo_de_equipamentos_Lista_de_IP)"+
                    "VALUES (?, ?, ?, ?,?, ?, ?, ?, ?, ?)",(sistema, equipamento, protocolo, modelo,fabricante, meio_fisico, descricao, subsistema,sistemas_lista_ip,grupo_equipamento_ip))
    
    # Commit para salvar as alterações no banco de dados
    conexao.commit()
    # Fechar a conexão
    conexao.close()
def adicionar_lista_estacao():
    print("estacao")

def adiconar_equipamento():
    
    linhas_selecionadas = tabela.selection()
    
    if linhas_selecionadas:
        linhas_indices = [int(tabela.index(item)) for item in linhas_selecionadas]
        
        df_selecionados = df_consulta.iloc[linhas_indices]
        tabela2.insert("","end",values=df_selecionados.values.tolist()[0])
        messagebox.showinfo('Mensagem','Eqipamento '+str(df_selecionados.values.tolist()[0][2])+' adicionado com sucesso')
    else:
        status_var.set("Nenhuma linha selecionada.")

def consultar_dados():
    dado_procurado = entrada_consulta.get()
    consulta = f"""
                SELECT *
                FROM tabela_dados
                WHERE Sistema LIKE '%{dado_procurado}%' OR
                EQUIPAMENTO LIKE '%{dado_procurado}%'  OR 
                PROTOCOLO LIKE '%{dado_procurado}%'    OR 
                MODELO LIKE '%{dado_procurado}%'       OR
                FABRICANTE LIKE '%{dado_procurado}%'   OR
                MEIO_FISICO LIKE  '%{dado_procurado}%' OR
                DESCRIÇÃO  LIKE   '%{dado_procurado}%' OR
                SUBSISTEMA LIKE '%{dado_procurado}%'   OR
                Sistemas_Lista_de_Ips LIKE '%{dado_procurado}%'   OR
                Grupo_de_equipamentos_Lista_de_IP LIKE '%{dado_procurado}%'

               """
    
    # Conexão com o banco de dados SQLite3
    conexao = sqlite3.connect('dados.db')

    # Executar a consulta
    global df_consulta
    df_consulta = pd.read_sql_query(consulta, conexao)

    # Preencher a tabela com os resultados
    preencher_tabela(df_consulta)

    # Fechar a conexão
    conexao.close()

def remover_linha():
    selecao = tabela2.selection()
    if selecao:
        tabela2.delete(selecao)
    
    else:
        messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma linha para excluir.")

def preencher_tabela(df):
    # Limpar a tabela
    tabela.delete(*tabela.get_children())
    
    # Preencher a tabela com os resultados
    for index, row in df.iterrows():
        tabela.insert("", "end", text=index, values=list(row))

def adicionar_enderecos_ip(lista_equipamentos):
    enderecos_ip = {}

    for equipamento, endereco_ip in lista_equipamentos.items():
        enderecos_ip[equipamento] = endereco_ip

    return enderecos_ip

def gerar_documentos():
    #selected_item é o nome da estação que foi selecionado pelo usuário no list box, esse nome é usado para retornar o endereço de ip'
    index = listbox.curselection()[0]
   

    estacao = listbox.get(index)
    #tabela2 detem os equipamentos selecionados  pelo usuário na interface,valores é a lista que recebe esses dados 

    lista_equipamentos = []#
    
    for row in tabela2.get_children():
        valores = tabela2.item(row)['values']
        lista_equipamentos.append(valores)

    for indice, sublist in enumerate(lista_equipamentos, start=1):#enumera os intens na lista.
        sublist.insert(0, indice)

    #Geração do Documento Lista de IPs
    gerar_sistemas_ip(lista_equipamentos,estacao)
    #Geração do Documento Lista de equipamentos
    Lista_equipamentos(lista_equipamentos)

    lista_TITULOS= []

    for i in range(len(lista_equipamentos)):
        lista_TITULOS.append(lista_equipamentos[i][11])

    lista_sem_repeticao = list(set(lista_TITULOS))
    print(lista_sem_repeticao)
    Gerar_Plano_integração(lista_sem_repeticao,caminho_consulta_plano_integração,caminho_template_plano_integração)
    messagebox.showinfo("Aviso", "Plano de Integração gerado!")
#================================================================================================#
#                                  INTERFACE GRÁFICA                                             #
#================================================================================================#
    
# Criar a janela principal
janela = tk.Tk()
janela.title("Sistema de Gerenciamento")

# Criar o notebook para as abas
notebook = ttk.Notebook(janela)
notebook.pack(fill=tk.BOTH, expand=True)

# Segunda aba
aba_consulta = ttk.Frame(notebook)
notebook.add(aba_consulta, text="Consulta")

# aba que adiciona um equipamento que não existe ao banco
aba_adicao = ttk.Frame(notebook)
notebook.add(aba_adicao, text="Adição de novo equipamento")

# Terceira aba
aba_viw = ttk.Frame(notebook)
notebook.add(aba_viw, text="Equipamentos Selecionados")

#Aba de recuperação de dados de estação já criada

aba_historico_estacao = ttk.Frame(notebook)
notebook.add(aba_historico_estacao, text="Histórico de Estações")

listbox = tk.Listbox(aba_viw)
listbox.grid(row=0, column=0, padx=10, pady=10)
lista_estacoes=['Amador Bueno', 'Antônio João', 'Autódromo', 'Barueri', 
                'Berrini', 'Brás', 'Carapicuíba', 'Ceasa', 'Cidade Jardim', 
                'Cidade Universitária', 'Comandante Sampaio', 'Domingos de Moraes', 
                'Engenheiro Cardoso', 'General Miguel Costa', 'Grajaú', 'Granja Julieta', 
                'Hebraica–Rebouças', 'Imperatriz Leopoldina', 'Itapevi', 'Jandira', 'Jardim Belval', 
                'Jardim Silveira', 'João Dias', 'Jurubatuba', 'Júlio Prestes', 'Lapa', 'Mendes–Vila Natal',
                  'Morumbi', 'Osasco', 'Palmeiras–Barra Funda', 'Patio Presidente Altino', 'Pinheiros', 
                  'Presidente Altino', 'Primavera–Interlagos', 'Quitaúna', 'Sagrado Coração', 'Santa Rita', 
                  'Santa Terezinha', 'Santo Amaro', 'Socorro', 'Varginha', 'Vila Lobos–Jaguaré', 'Vila Olímpia']


#cria uma lista para o usuário escolher qual estação que vai gerar lista de ip
for item in lista_estacoes:
    listbox.insert(tk.END, item)
# Associa a função on_select ao evento de seleção no listbox
listbox.bind('<<ListboxSelect>>', on_select)
label = tk.Label(aba_viw, text="")
label.grid(row=1, column=0, padx=10, pady=10)


#entrada para novo nome de sistema
rotulo_sistema = ttk.Label(aba_adicao, text="Sistema:")
rotulo_sistema.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

entrada_sistema = ttk.Entry(aba_adicao)
entrada_sistema.grid(row=0, column=1, padx=5, pady=5)

#entrada para novo nome de subsistema
rotulo_subsistema = ttk.Label(aba_adicao, text="Subsistema:")
rotulo_subsistema.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

entrada_subsistema = ttk.Entry(aba_adicao)
entrada_subsistema.grid(row=1, column=1, padx=5, pady=5)
#entrada para novo nome de Equipamento
rotulo_equipamento = ttk.Label(aba_adicao, text="Equipamento:")
rotulo_equipamento.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

entrada_equipamento = ttk.Entry(aba_adicao)
entrada_equipamento.grid(row=2, column=1, padx=5, pady=5)
#entrada para novo nome de Fabricante
rotulo_fabricante = ttk.Label(aba_adicao, text="Fabricante:")
rotulo_fabricante.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

entrada_fabricante = ttk.Entry(aba_adicao)
entrada_fabricante.grid(row=3, column=1, padx=5, pady=5)
#entrada para novo nome de Modelo
rotulo_modelo = ttk.Label(aba_adicao, text="Modelo:")
rotulo_modelo.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

entrada_modelo = ttk.Entry(aba_adicao)
entrada_modelo.grid(row=4, column=1, padx=5, pady=5)
#entrada para novo nome de Meio Físico
rotulo_meio = ttk.Label(aba_adicao, text="Meio Físico:")
rotulo_meio.grid(row=5 ,column=0, padx=5, pady=5, sticky=tk.W)

entrada_meio = ttk.Entry(aba_adicao)
entrada_meio.grid(row=5, column=1, padx=5, pady=5)
#entrada para novo nome de Protocolo
rotulo_protocolo = ttk.Label(aba_adicao, text="Protocolo:")
rotulo_protocolo.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)

entrada_protocolo = ttk.Entry(aba_adicao)
entrada_protocolo.grid(row=6, column=1, padx=5, pady=5)
#entrada para novo nome de Descrição
rotulo_descricao = ttk.Label(aba_adicao, text="Descrição:")
rotulo_descricao.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

entrada_descricao = ttk.Entry(aba_adicao)
entrada_descricao.grid(row=7, column=1, padx=5, pady=5)
#entrada para novo nome de Protocolo
rotulo_sistema_lista_ips = ttk.Label(aba_adicao, text="Sistemas Lista de IP's:")
rotulo_sistema_lista_ips.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)

entrada_sistema_lista_ips = ttk.Entry(aba_adicao)
entrada_sistema_lista_ips.grid(row=8, column=1, padx=5, pady=5)
#entrada para novo nome de Descrição
rotulo_grupo_ip = ttk.Label(aba_adicao, text="Grupo de equipamentos Lista de IP:")
rotulo_grupo_ip.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)

entrada_grupo_ip = ttk.Entry(aba_adicao)
entrada_grupo_ip.grid(row=9, column=1, padx=5, pady=5)

botao_adicionar_banco = ttk.Button(aba_adicao, text="Adicionar Equipamento ao Banco", command=adicionar_dados)
botao_adicionar_banco.grid(row=10, column=0, padx=5, pady=5)

rotulo_consulta = ttk.Label(aba_consulta, text="Consulta:")
rotulo_consulta.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

entrada_consulta = ttk.Entry(aba_consulta)
entrada_consulta.grid(row=0, column=1, padx=5, pady=5)

botao_consultar = ttk.Button(aba_consulta, text="Consultar", command=consultar_dados)
botao_consultar.grid(row=1, column=1, padx=5, pady=5)

botao_adicionar = ttk.Button(aba_consulta, text="Adicionar equipamento a lista", command=adiconar_equipamento)
botao_adicionar.grid(row=3, column=0, padx=5, pady=5)

# Criar a tabela para mostrar os resultados
tabela2 = ttk.Treeview(aba_viw, columns=("Sistema", "Subsistema","Equipamento", "Fabricante","Modelo","Meio Físico","Protocolo","Descrição"))
tabela2.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configurar as colunas da tabela
tabela2.heading("#0", text="Item")
tabela2.heading("Sistema", text="Sistema")
tabela2.heading("Subsistema", text="Subsistema")
tabela2.heading("Equipamento", text="Equipamento")
tabela2.heading("Fabricante", text="Fabricante")
tabela2.heading("Modelo", text="Modelo")
tabela2.heading("Meio Físico", text="Meio Físico")
tabela2.heading("Protocolo", text="Protocolo")
tabela2.heading("Descrição", text="Descrição")
# Configurar as colunas da tabela para redimensionar com o conteúdo
tabela2.column("#0",width=50, minwidth=100, stretch=tk.NO)
for col in tabela2["columns"]:
    tabela2.column(col,width=150, minwidth=100, stretch=tk.YES)

# Criar a tabela para mostrar os resultados
tabela = ttk.Treeview(aba_consulta, columns=("Sistema", "Subsistema","Equipamento", "Fabricante","Modelo","Meio Físico","Protocolo","Descrição"))
tabela.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configurar as colunas da tabela
tabela.heading("#0", text="Item")
tabela.heading("Sistema", text="Sistema")
tabela.heading("Subsistema", text="Subsistema")
tabela.heading("Equipamento", text="Equipamento")
tabela.heading("Fabricante", text="Fabricante")
tabela.heading("Modelo", text="Modelo")
tabela.heading("Meio Físico", text="Meio Físico")
tabela.heading("Protocolo", text="Protocolo")
tabela.heading("Descrição", text="Descrição")

# Configurar as colunas da tabela para redimensionar com o conteúdo
tabela.column("#0",width=50, minwidth=100, stretch=tk.NO)
for col in tabela["columns"]:
    tabela.column(col,width=150, minwidth=100, stretch=tk.YES)

# Botão para gerar arquivo Excel com os dados selecionados
botao_excel = ttk.Button(aba_viw, text="Gerar Documentos",state=tk.DISABLED, command=gerar_documentos)
botao_excel.grid(row=3, column=1, sticky="w")

# Botão para remover equipamento da lista
botao_remover = ttk.Button(aba_viw, text="Remover Equipamento", command=remover_linha)
botao_remover.grid(row=1, column=0, sticky="w")

# Botão para trazer lista do historico
botao_remover = ttk.Button(aba_viw, text="Retornar Estação", command=adicionar_lista_estacao)
botao_remover.grid(row=1, column=1, sticky="w")

# Variável de status para exibir mensagens
status_var = tk.StringVar()
status_label = ttk.Label(aba_viw, textvariable=status_var)

# Botão para remover equipamento da lista
botao_remover = ttk.Button(aba_historico_estacao, text="Selecionar Estação", command=remover_linha)
botao_remover.grid(row=2, column=0, sticky="n")

listbox2 = tk.Listbox(aba_historico_estacao)
listbox2.grid(row=0, column=0, padx=10, pady=10)

for item in consulta_tabelas():
    listbox2.insert(tk.END, item)

# Treeview
tabela3 = ttk.Treeview(aba_historico_estacao, columns=("Item", "Estação"), show="headings")
tabela3.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Definindo cabeçalhos das colunas
tabela3.heading("Item", text="Item")
tabela3.heading("Estação", text="Estação")

# Ajustando a expansão da Treeview
aba_historico_estacao.grid_rowconfigure(2, weight=1)
aba_historico_estacao.grid_columnconfigure(0, weight=1)

# Exemplo de inserção de dados na Treeview
tabela3.insert('', 'end', values=("1", "Estação A"))
tabela3.insert('', 'end', values=("2", "Estação B"))

# Iniciar a interface
janela.mainloop()
