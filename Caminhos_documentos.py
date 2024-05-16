import os 

#traz o diretório da pasta automaticamente onde o módulo se encontra
diretorio_arquivo = os.path.dirname(os.path.realpath(__file__))
#cria o caminho da pasta do plano de integração e
diretorio_Plano_integração =  os.path.join(diretorio_arquivo,'Estacao','ESTACAO','Plano de Integração')
diretorio_Lista_IP = os.path.join(diretorio_arquivo,'Estacao','ESTACAO','Lista de IP')
#Traz o nome do arquivo do plano de integração
nome_Plano_integração = os.listdir(diretorio_Plano_integração)
nome_Lista_Ip = os.listdir(diretorio_Lista_IP)



#Diretórios dos arquivos necessário
caminho_template_plano_integração   =  os.path.join(diretorio_arquivo,'Estacao','ESTACAO','Plano de Integração',nome_Plano_integração[0])
#caminho_template_plano_integração   =  nome_Plano_integração[0]
caminho_template_lista_ip           =  os.path.join(diretorio_arquivo,'Estacao','ESTACAO','Lista de IP',nome_Lista_Ip[0])
caminho_consulta_plano_integração   =  os.path.join(diretorio_arquivo,'Documentos_macro','DADOS_PLANO_INTEGRAÇÃO_FULL.docm')
caminho_template_Lista_equipamentos =  os.path.join(diretorio_arquivo,'Documentos_macro','LM-T-08-07-01-1299_6-R11-001_Rev_A.xlsx')
caminho_lista_equipamentos          = os.path.join(diretorio_arquivo,'Estacao','ESTACAO','Lista de Equipamentos','LM-T-08-07-01-1299_6-R11-001_Rev_A.xlsx')















