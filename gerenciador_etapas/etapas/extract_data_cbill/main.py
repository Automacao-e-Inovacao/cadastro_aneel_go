import logging
from selenium import webdriver
from gerenciador_etapas.etapas.extract_data_cbill.static_cbill import FuncoesCbill

class ExtracoesDadosCbill:
    def __init__(self, logger_nota: logging.Logger, inst_register) -> None:
        self.logger_nota = logger_nota
        self.conexao_datamart = inst_register
        self.driver = None  # Inicializa o driver como None para ser atribuído posteriormente
        self.inst_func_cbill = FuncoesCbill

        self.usuario_cbill = 'TATE5507011'
        self.senha_cbill = '$mbegp3jJ'
        
    def open_browser(self):
        # Define as opções do Chrome
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # Execute o navegador em modo headless (sem interface gráfica)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Inicializa o driver do Chrome
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(60)  # Define um tempo de espera implícito de 60 segundos

    def consultar_dados_cbill(self) -> None:
        # Abre o navegador se ainda não estiver aberto
        if self.driver is None:
            self.open_browser()

        try:
            self.driver.get('http://www2.aneel.gov.br/scg/gd/login.asp')
        except:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(60)
            self.driver.get('http://www2.aneel.gov.br/scg/gd/login.asp')

        titulo_da_pagina = self.driver.current_url
        if 'CPqD Energia - Atendimento ao cliente' in titulo_da_pagina:
            self.inst_func_cbill.login(self.driver, self.usuario_cbill, self.senha_cbill)
        else:
            self.logger_nota.error(f'Titulo da página é diferente do esperado :|: {titulo_da_pagina}')
