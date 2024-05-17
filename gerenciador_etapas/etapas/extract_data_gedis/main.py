from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import logging

from static.registrar_consultar import Registers

class ExtracoesDadosGedis:
    tabela = 'cadastro_aneel_go.nota'

    def __init__(self, logger_nota: logging.Logger, inst_register: Registers) -> None:
        self.logger_nota = logger_nota
        self.conexao_datamart = inst_register
        self.driver = None  # Inicializa o driver como None para ser atribuído posteriormente
        
    def open_browser(self):
        # Define as opções do Chrome
        chrome_options = webdriver.ChromeOptions()

        # Inicializa o driver do Chrome
        navegador = webdriver.Chrome(options=chrome_options)
        navegador.implicitly_wait(60)  # Define um tempo de espera implícito de 60 segundos
        
        navegador.get('https://gedis.equatorialenergia.com.br')
        
        return navegador
        
    def login(self, driver):
        element_user = '/html/body/div/div/div/div/form/div[1]/div/input'
        element_pswr = '/html/body/div[1]/div/div/div/form/div[2]/div/input'
        element_enter = '/html/body/div[1]/div/div/div/form/button'
        usuario = 'U5507011'
        senha = '123456'
        try:
            # Preencher usuário
            self.write_if_found(driver, element_user, usuario)

            # Preencher senha e pressionar Enter
            self.write_if_found(driver, element_pswr, senha)
            self.click_if_found(driver, element_enter)
        except:
            pass

    def write_if_found(self, driver, element, msg): 
        try_order = [By.XPATH, By.ID, By.CLASS_NAME, By.TAG_NAME, By.CSS_SELECTOR]
        for locator_type in try_order:
            try:
                element = driver.find_element(locator_type, element)
                while not element.is_displayed():
                    pass
                element.click()
                element.clear()
                element.send_keys(msg)
                return  # Parar a execução se o elemento for encontrado com sucesso
            except:
                pass

    def click_if_found(self, driver, element_click, max_attempts=10): 
        try_order = [By.XPATH, By.ID, By.CLASS_NAME, By.TAG_NAME, By.CSS_SELECTOR]
        for locator_type in try_order:
            for _ in range(max_attempts):
                try:
                    element = driver.find_element(locator_type, element_click)
                    while not element.is_displayed():
                        pass
                    element.click()
                    return True  # Indica que o clique foi bem-sucedido
                except:
                    time.sleep(1)  # Espera 1 segundo antes de tentar novamente
        return False  

    def click_filtros(self, driver):
        class_filtros = '//*[@class="card-header border-0 ui-sortable-handle"]'
        self.click_if_found(driver, class_filtros)
        
    def extrair_email_e_ss(self, driver):
        element_ss_do_parecer = "//label[text()='SS do Parecer de Acesso ou Orçamento de Conexão']/following-sibling::input"
        element_email = "//label[text()='E-mail']/following-sibling::input"
        
        elemento = driver.find_element(by=By.XPATH, value = element_ss_do_parecer)
        ss_do_parecer = elemento.get_attribute('value')

        elemento_email = driver.find_element(by=By.XPATH, value = element_email)
        email = elemento_email.get_attribute('value')
        
        return {'ss_do_parecer': ss_do_parecer, 'email': email}
  
    def search_uc(self, driver, uc):
        class_filtros = '//*[@class="card-header border-0 ui-sortable-handle"]'
        xpath_detalhes = '//*[@title="Detalhes"]'
        click_uc = "/html/body/div[1]/div[2]/section[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[3]/div/input"
        button_buscar = "//button[text()='Buscar']"
        try:
            ## Aqui ficam as funções que vão até a extração dos dados
            # Clica em Filtros
            self.click_if_found(driver, class_filtros)
            # Insere a UC
            self.write_if_found(driver, click_uc, uc)
            # Clica em buscar
            self.click_if_found(driver, button_buscar)
            # Clica em detalhes (Ícone de página)
            self.click_if_found(driver, xpath_detalhes)
            
            ## Extrai as informações de email e SS do parecer
            dicionario_principal = self.extrair_email_e_ss(driver)
            
            return dicionario_principal
        except:
            pass
    
    def scraping(self, uc):
        navegador = self.open_browser()
        
        self.login(navegador)
        time.sleep(2)
        dicionario_principal = self.search_uc(navegador, uc)
        time.sleep(2)
        navegador.quit()
        return dicionario_principal
        
    def execucao(self, id_nota):
        sql_consulta_uc = f'''
            SELECT id, uc FROM cadastro_aneel_go.nota
            WHERE id = {id_nota}
            '''
            
        tupla_uc = self.conexao_datamart.consultar_notas(sql=sql_consulta_uc)
        uc = tupla_uc[0]['uc']

        dicionario_principal = self.scraping(uc=uc)
        print(dicionario_principal)
        self.conexao_datamart.atualizar_registro(dicionario=dicionario_principal, tabela='cadastro_aneel_go.nota', id_=id_nota)
            
