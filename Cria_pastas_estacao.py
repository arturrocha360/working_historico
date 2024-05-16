import tkinter as tk
from tkinter import ttk, filedialog
import shutil
import os
from macro import roda_script



diretorio_arquivo = os.path.dirname(os.path.realpath(__file__))



caminho = os.path.join(diretorio_arquivo,'Estacao','ESTACAO')

shutil.rmtree(caminho)

pastas=["Lista de Cabos","Lista de Entradas","Lista de Equipamentos","Lista de IP","Lista de Materiais","Mapa de Comunicação",
        "Plano de Integração","Procedimentos de Comissionamento","Procedimentos de Pré","Relatório de Levamentamento"]
# Especifica o caminho da pasta a ser criada

# Verifica se o diretório não existe e, em seguida, o cria
for pasta in pastas:
    os.makedirs(caminho+"/"+pasta)


def selecionar_arquivo():
    arquivo_selecionado = filedialog.askopenfilename(initialdir="/", title="Selecione o arquivo")
    if arquivo_selecionado:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, arquivo_selecionado)

def copiar_arquivo():
   
    origem = entrada_arquivo.get()
    destino = caminho
    if origem and destino:
        shutil.copy(origem, destino)
        lbl_status.config(text="Arquivo copiado com sucesso para {}".format(destino))
    else:
        lbl_status.config(text="Por favor, selecione um arquivo e uma pasta de destino")
    roda_script()
    

# Configuração da janela principal
root = tk.Tk()
root.title("Copiar Arquivo")

# Notebook para as abas
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Primeira aba
aba1 = ttk.Frame(notebook)
notebook.add(aba1, text="Primeira Aba")

# Frame para a seleção de arquivo na primeira aba
frame_arquivo = tk.Frame(aba1)
frame_arquivo.pack(padx=10, pady=10, fill=tk.X)

lbl_arquivo = tk.Label(frame_arquivo, text="Arquivo:")
lbl_arquivo.pack(side=tk.LEFT)

entrada_arquivo = tk.Entry(frame_arquivo, width=50)
entrada_arquivo.pack(side=tk.LEFT, padx=(5, 0))

btn_selecionar_arquivo = tk.Button(frame_arquivo, text="Selecionar", command=selecionar_arquivo)
btn_selecionar_arquivo.pack(side=tk.LEFT, padx=(5, 0))



# Botão para copiar o arquivo na primeira aba
btn_copiar = tk.Button(aba1, text="Copiar Arquivo", command=copiar_arquivo)
btn_copiar.pack(pady=(0, 10))


# Label para exibir status na primeira aba
lbl_status = tk.Label(aba1, text="", fg="green")
lbl_status.pack()


root.mainloop()

