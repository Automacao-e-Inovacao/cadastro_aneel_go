import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os


from static.registrar_consultar import Registers
from gerenciador_etapas.etapas.extract_data_sicap.static_sicap import StaticSicap

class ExtracoesDadosSicap:
    tabela = 'cadastro_aneel_go.nota'

    def __init__(self, logger_nota: logging.Logger, inst_register: Registers) -> None:
        self.logger_nota = logger_nota
        self.conexao_datamart = inst_register
        self.inst_static_sicap = StaticSicap()
        self.link_sicap = 'http://sistemassatelites.equatorial.corp:8080/Sicap-adm/'
        
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options= chrome_options)

    def run(self):
        self.inst_static_sicap.login()
        
    def execucao(self, driver):
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options= chrome_options)