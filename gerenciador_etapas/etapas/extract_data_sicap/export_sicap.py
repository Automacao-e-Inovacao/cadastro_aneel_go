# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os
import logging


# %%
link_sicap = 'http://sistemassatelites.equatorial.corp:8080/Sicap-adm/'
usuario_sicap = 'u5512983'
senha_sicap = 'Ft$85Gb13:<f>@#$'

chrome_options = webdriver.ChromeOptions()
navegador = webdriver.Chrome(options= chrome_options)
navegador.implicitly_wait(200)
navegador.get(link_sicap)
#Mudando o implicity wait para testes de elemtento (ALTERAR DEPOIS)
navegador.implicitly_wait(1)

# %%
def click_if_found(navegador, element_click): 
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
        
def write_if_found(navegador, element, msg): 
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

# %%
class CadastroSiteAneel:
    tabela = 'cadastro_aneel_go.nota'

    def __init__(self, logger_nota: logging.Logger) -> None:
        self.logger_nota = logger_nota

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)

        self.usuario_aneel = 'gd.goias@equatorialenergia.com.br'
        self.senha_aneel = 'EQTL01'
        self.empresa_abreviado = 'GO'


def login(self, navegador, link):
    chrome_options = webdriver.ChromeOptions()
    navegador = webdriver.Chrome(options= chrome_options)
    navegador.implicitly_wait(200)
    navegador.get(link)
    #Mudando o implicity wait para testes de elemtento (ALTERAR DEPOIS)
    navegador.implicitly_wait(1)


# %%
navegador.find_element(by=By.XPATH, value='//*[@class="btn btn-default"]').click()

# %%
def login(self, navegador=navegador):
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
        write_if_found(navegador, self.element_user, self.usuario_sicap)

        #Preencher senha e pressionar Enter
        password = navegador.find_element(by=By.XPATH, value=self.element_pwrd)
        password.click()
        password.clear()
        password.send_keys(senha_sicap, Keys.ENTER)
        return id_button_login
    except:
        pass
    
id_button_login = login(navegador)

# %%
def search_ss(self, element_liken):
    self.element_liken = element_liken
    try:
        #Botão buscar SS do parecer
        element_search = navegador.find_element(by=By.XPATH, value='//*[@class="btn btn-default"]')
        id_button_search = element_search.get_attribute("id")
        if id_button_search != self.element_liken:
            element_search.click()
            return True
        else:
            return False
    except:
        pass


# %%
# Exemplo de uso
id_button_login = login(navegador)
if id_button_login:
    if search_ss(element_liken=id_button_login):
        print("Busca realizada com sucesso.")
    else:
        print("Não foi possível realizar a busca.")

# %%
element_user_v2 = '//*[@id="username"]'
element_user = '//*[@id="input_username"]'
element_pwrd = '//*[@id="password"]'
usuario_sicap = 'u5512983'
senha_sicap = 'Ft$85Gb13:<f>@#$'


# %%
element_login = navegador.find_element(by=By.CLASS_NAME, value='fa fa-search')
element_login.click()

# %%
navegador.find_element(by=By.CLASS_NAME, value='fa fa-search')

# %%
element_user = '//*[@id="username"]'
element_pwrd = '//*[@id="password"]'
element_search = '//*[@class="fa fa-search"]'

# %%
element_login = navegador.find_element(by=By.XPATH, value='//*[@class="fa fa-search"]')

# %%
element_login.click()

# %%
#Clicar apenas quando o elemento estiver visível
def into_atendimento_ao_cliente():
    while True:
        try:
            elemento_button_atendimento = navegador.find_element(by=By.XPATH, value='')
            while not elemento_button_atendimento.is_displayed():
                pass
            elemento_button_atendimento.click()       
            navegador.find_element(by=By.XPATH, value='').click()
            break
        except:
            pass
into_atendimento_ao_cliente()

# %%
class ReadExcelFile:
    ss_do_parecer = '164707086'
    
    def __init__(self, ss_do_parecer) -> None:
        self.ss_do_parecer = ss_do_parecer
        
        pass

# %%
class Sicap:
    def __init__(self) -> None:
        self.button_find = '//*[@id="templateForm:j_idt48"]'
        self.button_insert_ss = '//*[@id="novasEntradas:interessadoFilter"]'
        self.button_consultar = '//*[@id="novasEntradas:j_idt92"]'
        
    def search_button(self, navegador, ss_do_parecer):
        try:
            # Botão Buscar
            click_if_found(navegador, element_click=self.button_find)
            # Botão Inserir SS do parecer
            ss_value = str(self.ss_do_parecer)  # Garante que o valor seja uma string
            navegador.find_element(by=By.XPATH, value=self.button_insert_ss).send_keys(ss_value)
            # Botão Consultar
            click_if_found(navegador, element_click=self.button_consultar)
        except:
            pass


# %%



