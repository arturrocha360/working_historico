import win32com.client

def Gerar_Plano_integração(equipamentos,path_consulta,path_template):
    
    #path_consulta = "C:/Users/artur.rocha/Documents/working/Documentos_macro/DADOS_PLANO_INTEGRAÇÃO_FULL.docm"
   # path_template= "C:/Users/artur.rocha/Documents/MD-T-08-10-02-1299-6-R11-002-Rev_1.docx"   #diretório do teplate usado para preenchimento do equipamento
    equipamentos_invertido=equipamentos[::-1]
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = True  # Para tornar o Word visível durante a execução
    doc = word.Documents.Open(path_consulta)  #diretório do documento de consulta
    
    #equipamentos=["Inversores", "Chave Estática", "Cabine Primária","Transformador","PESS – Painel Essencial"]

    for equipamento in equipamentos_invertido:
        word.Run("copy_paste_Plano",equipamento,path_template)

    doc.Close(SaveChanges=False)
    word.Quit()
    print("Macro executada com sucesso!")
 


