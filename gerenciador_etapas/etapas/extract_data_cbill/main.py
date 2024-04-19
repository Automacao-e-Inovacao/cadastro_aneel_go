import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from gerenciador_etapas.etapas.extract_data_cbill.static_cbill import login_cbill

class ExtracoesDadosCbill:
    def __init__(self, logger_nota: logging.Logger, inst_register) -> None:
        self.logger_nota = logger_nota
        self.conexao_datamart = inst_register
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)

        self.usuario_cbill = 'TATE5507011'
        self.senha_cbill = '$mbegp3jJ'
        
        self.uc_cbill = '10006787760'
        self.ss_da_planilha = '163890270'
                
    def consultar_dados_cbill(self) -> None:
        try:
            self.driver.get('http://www2.aneel.gov.br/scg/gd/login.asp')
        except:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(60)
            self.driver.get('http://www2.aneel.gov.br/scg/gd/login.asp')
        titulo_da_pagina = self.driver.current_url
        if 'CPqD Energia - Atendimento ao cliente' in titulo_da_pagina:
            login_cbill(self.driver, self.usuario_cbill, self.senha_cbill)
        else:
            self.logger_nota.error(f'Titulo da página é diferente do esperado :|: {titulo_da_pagina}')