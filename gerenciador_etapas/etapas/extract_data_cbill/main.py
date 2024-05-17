import logging
from selenium import webdriver
from gerenciador_etapas.etapas.extract_data_cbill.static_cbill import FuncoesCbill

from static.registrar_consultar import Registers

class ExtracoesDadosCbill:
    def __init__(self, logger_nota: logging.Logger, inst_register: Registers) -> None:
        self.logger_nota = logger_nota
        self.conexao_datamart = inst_register
        self.inst_func_cbill = FuncoesCbill(logger_nota, inst_register)
        self.usuario_cbill = 'TATE5507011'
        self.senha_cbill = '$mbegp3jJ'
    
    def execucao(self, id_nota):
        sql_consulta_uc = f'''
            SELECT id, uc, ss_da_planilha FROM cadastro_aneel_go.nota
            WHERE id = {id_nota}
            '''
            
        tupla_uc = self.conexao_datamart.consultar_notas(sql=sql_consulta_uc)
        uc = tupla_uc[0]['uc']
        ss_da_planilha = tupla_uc[0]['ss_da_planilha']
        
        dicionario_principal = self.inst_func_cbill.scraping(uc_cbill=uc, ss_da_planilha=ss_da_planilha)
        # print(dicionario_principal)
        self.conexao_datamart.atualizar_registro(dicionario=dicionario_principal, tabela='cadastro_aneel_go.nota', id_=id_nota)
            

