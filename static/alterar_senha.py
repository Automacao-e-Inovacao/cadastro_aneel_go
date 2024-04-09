from cryptography.fernet import Fernet
import os
from registrar_consultar import Registers
import datetime

inst_register = Registers()
sistema = 'SAP CRM'
senha_nova = 'Ricorico@Nefarian@1038'
tabela = 'rpa.senhas'

query = f'''
select id from {tabela}
where sistema = '{sistema}'
'''

lista_resultado = inst_register.consultar_notas(sql=query)
lista_resultado = lista_resultado[0]
id_registro = lista_resultado['id']

# Gere uma chave de criptografia
caminho_relativo = os.path.dirname(__file__)
with open(file=os.path.join(caminho_relativo, 'chave.txt'), mode='r') as arquivo:
    key = arquivo.read()
    key = key[1:].encode('utf-8')
cipher_suite = Fernet(key)

# String que você deseja criptografar
senha_nova = senha_nova.encode('utf-8')

senha_nova = cipher_suite.encrypt(senha_nova)

senha_nova = str(senha_nova)

dicionario = {
    'sistema': sistema,
    'senha': senha_nova,
    'updated_at': datetime.datetime.now()
}

# Consultando senha_nova
inst_register.atualizar_registro(
    dicionario=dicionario, tabela=tabela, id_=id_registro
)