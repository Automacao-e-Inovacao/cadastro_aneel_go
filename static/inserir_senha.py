from cryptography.fernet import Fernet
import os
from registrar_consultar import Registers
import datetime

inst_register = Registers()
sistema = 'EQTLINFO'
senha_nova = 'JWshqL716'
tabela = 'rpa.senhas'

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
inst_register.registro_sucesso(
    dicionario=dicionario, tabela=tabela
)
