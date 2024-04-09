from cryptography.fernet import Fernet
import os
from registrar_consultar import Registers


def buscar_senha(sistema):
    inst_register = Registers()
    # Gere uma chave de criptografia
    caminho_relativo = os.path.dirname(__file__)
    with open(file=os.path.join(caminho_relativo, 'chave.txt'), mode='r') as arquivo:
        key = arquivo.read()
        key = key[1:].encode('utf-8')
    cipher_suite = Fernet(key)

    # String que você deseja criptografar
    query = f''' 
    select senha from rpa.senhas
    where sistema = '{sistema}'
    '''

    # Consultando senha
    lista_resultado = inst_register.consultar_notas(sql=query)
    lista_resultado = lista_resultado[0]
    texto_original = lista_resultado['senha']
    texto_original = texto_original[1:].encode('utf-8')

    # Descriptografe a string (apenas para verificar)
    texto_descriptografado = cipher_suite.decrypt(texto_original)
    texto_descriptografado = texto_descriptografado.decode('utf-8')
    inst_register.conexao.fechar()
    return texto_descriptografado
