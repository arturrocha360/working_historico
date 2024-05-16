import win32com.client
from tkinter import messagebox
import os

diretorio_arquivo = os.path.dirname(os.path.realpath(__file__))
caminho = os.path.join(diretorio_arquivo,'Script Geracao.xlsm')
print(caminho)
def roda_script():
    # Iniciar uma instância do Excel
    excel = win32com.client.Dispatch("Excel.Application")

    # Abrir o arquivo Excel
    workbook = excel.Workbooks.Open(caminho)
     
    # Chamar a macro pelo nome
    excel.Application.Run("Planilha1.Gerar_Documentos")
    print('rodando')
    # Fechar o arquivo Excel sem salvar as alterações (se necessário)
    workbook.Close(False)

    # Fechar o Excel
    excel.Quit()
    messagebox.showinfo('Aviso','Arquivos Gerado')
