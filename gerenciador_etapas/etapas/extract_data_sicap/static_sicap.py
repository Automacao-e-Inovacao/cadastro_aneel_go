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

class StaticSicap:
    tabela = 'cadastro_aneel_go.nota'

    def __init__(self, logger_nota: logging.Logger, inst_register: Registers) -> None:
        self.logger_nota = logger_nota
        self.conexao_datamart = inst_register
        
    def click_if_found(self, navegador, element_click): 
        try_order = [By.ID, By.CLASS_NAME, By.XPATH, By.TAG_NAME, By.CSS_SELECTOR]
        for locator_type in try_order:
            try:
                element = navegador.find_element(locator_type, element_click)
                while not element.is_displayed():
                    pass
                element.click()
                return  # Parar a execução se o elemento for encontrado com sucesso
            except:
                pass
            
    def write_if_found(self, navegador, element, msg): 
        try_order = [By.ID, By.CLASS_NAME, By.XPATH, By.TAG_NAME, By.CSS_SELECTOR]
        for locator_type in try_order:
            try:
                element = navegador.find_element(locator_type, element)
                while not element.is_displayed():
                    pass
                element.click()
                element.clear()
                element.send_keys(msg)
                return  # Parar a execução se o elemento for encontrado com sucesso
            except:
                pass
        
    def login(self, navegador, link_sicap):
        self.element_user = '//*[@id="input_username"]'
        self.element_pwrd = '//*[@id="input_password"]'
        self.usuario_sicap = 'u5512983'
        self.senha_sicap = 'Ft$85Gb13:<f>@#$'
        
        try:
            #Botão Login, antes de inserir o usuario/senha
            element_login = navegador.find_element(by=By.XPATH, value='//*[@class="btn btn-default"]')
            id_button_login = element_login.get_attribute("id")
            element_login.click()
            #Preencher usuário
            self.write_if_found(navegador, self.element_user, self.usuario_sicap)

            #Preencher senha e pressionar Enter
            password = navegador.find_element(by=By.XPATH, value=self.element_pwrd)
            password.click()
            password.clear()
            password.send_keys(self.senha_sicap, Keys.ENTER)
            return id_button_login
        except:
            pass
        
    def search_ss(self, element_liken):
        self.element_liken = element_liken
        try:
            #Botão buscar SS do parecer
            element_search = self.navegador.find_element(by=By.XPATH, value='//*[@class="btn btn-default"]')
            id_button_search = element_search.get_attribute("id")
            if id_button_search != self.element_liken:
                element_search.click()
                return True
            else:
                return False
        except:
            pass