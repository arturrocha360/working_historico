
from tools import gerar_listaip,ip_consulta

#essa função recebe um ip_inicial e sua quantidade e gera uma lista de ips
def gerador_ips(ip_inicial,quantidade):
  
  lista_ip=[]
 
  for i in range(0, quantidade):
     lista_ip.append(f"{ip_inicial.rsplit('.', 1)[0]}.{int(ip_inicial.rsplit('.', 1)[1]) + i}")
     
  return lista_ip

def gerar_sistemas_ip(lista,selected_item):
    
    tag_scap = []
    tag_smm  = []
    tag_sme  = []
    tag_sca  = []
    tag_scl  = []

    #matrizes de sistemas, linha 1 contem tag e linha dois contem a descrição, SCL pode possui remota 
    SCAP =[[],[]]
    SMM  =[[],[]]
    SME  =[[],[]]
    SCA  =[[],[]]
    SCL  =[[],[]]
    SCADA=[[],[]]
    
   
    #Aqui é feito a classificação dos equipamentos de acordo com o sistema a qual ele pertence

    remota1_existente= False
    remota2_existente= False
    remota3_existente= False
    remota4_existente= False
    qdbi_existente   = False
    qgd_existente    = False
    
    for i in range(len(lista)):
        
        if lista[i][9]=="SCAP" or lista[i][9]=="scap":
            SCAP[0].append(lista[i][3])
            SCAP[1].append(lista[i][8])
        elif lista[i][9]=="SMM" or lista[i][9]=="smm":
            SMM[0].append(lista[i][3])
            SMM[1].append(lista[i][8])
        elif lista[i][9]=="SME" or lista[i][9]=="sme":
            SME[0].append(lista[i][3])
            SME[1].append(lista[i][8])
        elif lista[i][9]=="SCA" or lista[i][9]=="sca":
            SCA[0].append(lista[i][3]) 
            SCA[1].append(lista[i][8])
        elif lista[i][9]=="SCL" or lista[i][9]=="scl":
           if lista[i][10]== "-":
                SCL[0].append(lista[i][3])   
                
                if lista[i][7]=="Modbus RTU" or lista[i][7]=="Alnet I":
                    SCL[1].append("Conversor")
                else:
                    SCL[1].append(lista[i][8])

           elif (lista[i][10]== "REMOTA 1" and not(remota1_existente)):
               SCL[0].insert(0,'REM_1')
               SCL[1].insert(0,'REMOTA-01')
               remota1_existente= True
           elif (lista[i][10]== "REMOTA 2" and not(remota2_existente)):
               SCL[0].insert(0,'REM_2')
               SCL[1].insert(0,'REMOTA-02')
               remota2_existente= True
           elif (lista[i][10]== "REMOTA 3" and not(remota3_existente)):
               SCL[0].insert(0,'REM_3')
               SCL[1].insert(0,'REMOTA-03')
               remota3_existente= True
           elif (lista[i][10]== "REMOTA 4" and not(remota4_existente)):
               SCL[0].insert(0,'REM_4')
               SCL[1].insert(0,'REMOTA-04')
               remota4_existente= True
           elif (lista[i][10]== "QDBI" and not(qdbi_existente)):
               SCL[0].insert(0,'QDBI')
               SCL[1].insert(0,'QDBI')
               qdbi_existente= True
           elif (lista[i][10]== "QGD" and not(qgd_existente)):
               SCL[0].insert(0,'QGD')
               SCL[1].insert(0,'QGD')
               qgd_existente= True
          
        
        elif lista[i][9]== "SCADA" or lista[i][9]=="scada":
            SCADA[0].append(lista[i][3])
            SCADA[1].append(lista[i][8])
   
    
    quantidade_equipamentos=[len(SCADA[0]),len(SCAP[0]),len(SMM[0]),len(SME[0]),len(SCA[0]),len(SCL[0])]

    quantidade_equipamentos[0]= 6 # o SCADA sempre possui 6 equipamentos generico
    
    tag_scada=[f'ES_{ip_consulta(selected_item,"SCADA")[0][1]}_SWITCHSCL_01',
            f'ES_{ip_consulta(selected_item,"SCADA")[0][1]}_SWITCHSCL_02',
            f'ES_{ip_consulta(selected_item,"SCADA")[0][1]}_SERVERSCL_01',
            f'ES_{ip_consulta(selected_item,"SCADA")[0][1]}_SERVERSCL_02',
            f'ES_{ip_consulta(selected_item,"SCADA")[0][1]}_VIEWERSCL_01',
            f'ES_{ip_consulta(selected_item,"SCADA")[0][1]}_VIEWERSCL_02'
            ]
    #listta básica de todas as estaçoes 
    
    descricao_scada=['SWITCH 1 SCL','SWITCH 1 SCL','SERVIDOR SCADA 1 SCL'
                ,'SERVIDOR SCADA 2 SCL','COMPUTADOR VIEWER 1 SCL','COMPUTADOR VIEWER 2 SCL'
                ]
    
    descricao_scap  = []
    if quantidade_equipamentos[1]!=0:#se tiver bloqueios a descrição do scap recebe um elemento unico com a quantidade de bloqueios já que o scap tem apenas um endereço de ip
        tag_scap.append(f'ES_{ip_consulta(selected_item,"SCAP")[0][1]}_SCAP')
        descricao_scap = [f'SISTEMA DE CONTROLE DE ARRECADAÇÃO DE PASSAGEIROS ({quantidade_equipamentos[1]} EQUIPAMENTOS)']
        quantidade_equipamentos[1]=1

    descricao_smm  = []
    [tag_smm.append(f'ES_{ip_consulta(selected_item,"SCAP")[0][1]}_{descricao.upper()}')    for descricao in SMM[0]]
    [descricao_smm.append(f'{descricao.upper()}')    for descricao in SMM[1]]

    descricao_sme  = []
    [tag_sme.append(f'ES_{ip_consulta(selected_item,"SCAP")[0][1]}_{descricao.upper()}')    for descricao in SME[0]]
    [descricao_sme.append(f'{descricao.upper()}')    for descricao in SME[1]]

    descricao_sca  = []
    [tag_sca.append(f'ES_{ip_consulta(selected_item,"SCAP")[0][1]}_{descricao.upper()}')    for descricao in SCA[0]]
    [descricao_sca.append(f'{descricao.upper()}')    for descricao in SCA[1]]

    descricao_scl  = []

    [tag_scl.append(f'ES_{ip_consulta(selected_item,"SCAP")[0][1]}_{descricao.upper()}')    for descricao in SCL[0]]
    [descricao_scl.append(f'{descricao.upper()}')    for descricao in SCL[1]]

    endereco_ip_lista_scada  = gerador_ips(ip_consulta(selected_item,"SCADA")[0][9],quantidade_equipamentos[0])
    endereco_ip_lista_scap   = gerador_ips(ip_consulta(selected_item,"SCAP")[0][9],quantidade_equipamentos[1] )
    endereco_ip_lista_smm    = gerador_ips(ip_consulta(selected_item,"SMM")[0][9],quantidade_equipamentos[2]  )
    endereco_ip_lista_sme    = gerador_ips(ip_consulta(selected_item,"SME")[0][9],quantidade_equipamentos[3]  )
    endereco_ip_lista_sca    = gerador_ips(ip_consulta(selected_item,"SCA")[0][9],quantidade_equipamentos[4]  )
    endereco_ip_lista_scl    = gerador_ips(ip_consulta(selected_item,"SCL")[0][9],quantidade_equipamentos[5]  )

    mascara_scada =['255.255.255.128']*len(endereco_ip_lista_scada)
    gateway_scada =[ip_consulta(selected_item,"SCADA")[0][7]]*len(endereco_ip_lista_scada)
    rede_scada    =[ip_consulta(selected_item,"SCADA")[0][5]]*len(endereco_ip_lista_scada)
    id_vlans_scada=[f'{int(ip_consulta(selected_item,"SCADA")[0][8])}']*len(endereco_ip_lista_scada)
    
    mascara_scap =['255.255.255.128']*len(endereco_ip_lista_scap)
    gateway_scap =[ip_consulta(selected_item,"SCAP")[0][7]]*len(endereco_ip_lista_scap)
    rede_scap    =[ip_consulta(selected_item,"SCAP")[0][5]]*len(endereco_ip_lista_scap)
    id_vlans_scap=[f'{int(ip_consulta(selected_item,"SCAP")[0][8])}']*len(endereco_ip_lista_scap)
        
    mascara_smm =['255.255.255.128']*len(endereco_ip_lista_smm)
    gateway_smm =[ip_consulta(selected_item,"SMM")[0][7]]*len(endereco_ip_lista_smm)
    rede_smm   =[ip_consulta(selected_item,"SMM")[0][5]]*len(endereco_ip_lista_smm)
    id_vlans_smm=[f'{int(ip_consulta(selected_item,"SMM")[0][8])}']*len(endereco_ip_lista_smm)

    mascara_sme =['255.255.255.128']*len(endereco_ip_lista_sme)
    gateway_sme =[ip_consulta(selected_item,"SME")[0][7]]*len(endereco_ip_lista_sme)
    rede_sme    =[ip_consulta(selected_item,"SME")[0][5]]*len(endereco_ip_lista_sme)
    id_vlans_sme=[f'{int(ip_consulta(selected_item,"SME")[0][8])}']*len(endereco_ip_lista_sme)
        
    mascara_sca  =['255.255.255.128']*len(endereco_ip_lista_sca)
    gateway_sca  =[ip_consulta(selected_item,"SCA")[0][7]]*len(endereco_ip_lista_sca)
    rede_sca     =[ip_consulta(selected_item,"SCA")[0][5]]*len(endereco_ip_lista_sca)
    id_vlans_sca =[f'{int(ip_consulta(selected_item,"SCA")[0][8])}']*len(endereco_ip_lista_sca)
        
    mascara_scl  =['255.255.255.128']*len(endereco_ip_lista_scl)
    gateway_scl  =[ip_consulta(selected_item,"SCL")[0][7]]*len(endereco_ip_lista_scl)
    rede_scl     =[ip_consulta(selected_item,"SCL")[0][5]]*len(endereco_ip_lista_scl)
    id_vlans_scl =[f'{int(ip_consulta(selected_item,"SCL")[0][8])}']*len(endereco_ip_lista_scl)
        
    tag              =     tag_scada+tag_scap+tag_smm+tag_sme+tag_sca+tag_scl
    descricao        =     descricao_scada+descricao_scap+descricao_smm+descricao_sme+descricao_sca+descricao_scl

    endereco_ip_lista=     endereco_ip_lista_scada+endereco_ip_lista_scap+endereco_ip_lista_smm+endereco_ip_lista_sme+endereco_ip_lista_sca+endereco_ip_lista_scl
    mascara          =     mascara_scada+mascara_scap+mascara_smm+mascara_sme+mascara_sca+mascara_scl
    gateway          =     gateway_scada+gateway_scap+gateway_smm+gateway_sme+gateway_sca+gateway_scl
    rede             =     rede_scada+rede_scap+rede_smm+rede_sme+rede_sca+rede_scl
    id_vlans         =     id_vlans_scada+id_vlans_scap+id_vlans_smm+id_vlans_sme+id_vlans_sca+id_vlans_scl

    
    gerar_listaip(tag,descricao,endereco_ip_lista,mascara,gateway,rede,id_vlans)
