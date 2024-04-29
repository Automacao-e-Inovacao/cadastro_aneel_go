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
        # chrome_options.add_argument("--headless")  # Execute o navegador em modo headless (sem interface gráfica)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Inicializa o driver do Chrome
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(200)  # Define um tempo de espera implícito de 200 segundos

    def login(self, usuario, senha):
        element_user = '/html/body/div/div/div/div/form/div[1]/div/input'
        element_pswr = '/html/body/div[1]/div/div/div/form/div[2]/div/input'
        element_enter = '/html/body/div[1]/div/div/div/form/button'
        try:
            # Preencher usuário
            self.write_if_found(element_user, usuario)

            # Preencher senha e pressionar Enter
            self.write_if_found(element_pswr, senha)
            self.click_if_found(element_enter)
        except:
            pass

    def write_if_found(self, element, msg): 
        try_order = [By.ID, By.CLASS_NAME, By.XPATH, By.TAG_NAME, By.CSS_SELECTOR]
        for locator_type in try_order:
            try:
                element = self.driver.find_element(locator_type, element)
                while not element.is_displayed():
                    pass
                element.click()
                element.clear()
                element.send_keys(msg)
                return  # Parar a execução se o elemento for encontrado com sucesso
            except:
                pass

    def click_if_found(self, element_click, max_attempts=10): 
        try_order = [By.XPATH, By.ID, By.CLASS_NAME, By.TAG_NAME, By.CSS_SELECTOR]
        for locator_type in try_order:
            for _ in range(max_attempts):
                try:
                    element = self.driver.find_element(locator_type, element_click)
                    while not element.is_displayed():
                        pass
                    element.click()
                    return True  # Indica que o clique foi bem-sucedido
                except:
                    time.sleep(1)  # Espera 1 segundo antes de tentar novamente
        return False  

    def click_filtros(self):
        class_filtros = '//*[@class="card-header border-0 ui-sortable-handle"]'
        self.click_if_found(class_filtros)
        
    def extrair_email_e_ss(self):
        element_ss_do_parecer = "//label[text()='SS do Parecer de Acesso ou Orçamento de Conexão']/following-sibling::input"
        element_email = "//label[text()='E-mail']/following-sibling::input"
        
        elemento = self.driver.find_element(by=By.XPATH, value = element_ss_do_parecer)
        ss_do_parecer = elemento.get_attribute('value')

        elemento_email = self.driver.find_element(by=By.XPATH, value = element_email)
        email = elemento_email.get_attribute('value')
        
        return ss_do_parecer, email

    def repeat(self):
        elemento_solicitacoes = "//a[text()='Solicitações']"
        self.click_if_found(elemento_solicitacoes)   
        
    def search_uc(self, uc):
        class_filtros = '//*[@class="card-header border-0 ui-sortable-handle"]'
        xpath_detalhes = '//*[@title="Detalhes"]'
        click_uc = "/html/body/div[1]/div[2]/section[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[3]/div/input"
        button_buscar = "//button[text()='Buscar']"
        try:
            ## Aqui ficam as funções que vão até a extração dos dados
            # Clica em Filtros
            self.click_if_found(class_filtros)
            # Insere a UC
            self.write_if_found(click_uc, uc)
            # Clica em buscar
            self.click_if_found(button_buscar)
            # Clica em detalhes (Ícone de página)
            self.click_if_found(xpath_detalhes)
            
            ## Extrai as informações de email e SS do parecer
            dicionario = self.extrair_email_e_ss()
            
            #Retorna para o começo da página para fazer uma outra extração
            self.repeat()
            
            return dicionario
        except:
            pass
    
    def execucao(self, usuario, senha):
        self.open_browser()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.login(usuario, senha)

        # Criar DataFrame com as unidades
        data = {
            'Unidade': ['10003582173', '10003638454', '10006559849', '10006597422', '10009712419']
        }
        df = pd.DataFrame(data)

        # Adicionar colunas para email e SS
        df['Email'] = ''
        df['SS'] = ''

        # Iterar sobre as unidades e extrair email e SS
        for index, row in df.iterrows():
            uc = row['Unidade']
            print(f"Extraindo informações para a unidade {uc}...")
            informacoes = self.search_uc(uc)
            if informacoes:
                df.at[index, 'SS'] = informacoes[0]
                df.at[index, 'Email'] = informacoes[1]
