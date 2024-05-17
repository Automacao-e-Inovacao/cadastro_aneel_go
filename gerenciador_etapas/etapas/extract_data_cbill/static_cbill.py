import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re
from static.erros import ErroPrevisto

from static.registrar_consultar import Registers

class FuncoesCbill:
    def __init__(self, logger_nota: logging.Logger, inst_register=Registers) -> None:
        self.logger_nota = logger_nota
        self.navegador = None
        self.conexao_datamart = inst_register
        self.main_frame = 'contentCRM'
        self.top_frame = 'sessionheader'
        self.mid_frame = 'principal'
        self.botton_frame = 'active_browser_funcs'
        
    def open_browser(self):
        # Define as opções do Chrome
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # Execute o navegador em modo headless (sem interface gráfica)
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")

        # Inicializa o driver do Chrome
        navegador = webdriver.Chrome(options=chrome_options)
        navegador.implicitly_wait(60)  # Define um tempo de espera implícito de 60 segundos
        
        navegador.get('http://bm4e.equatorialenergia.com.br/cbill/loginPage.do')
        
        return navegador

    def buscar_no_banco(self):
        sql_consulta_nota = f'''
        select id, repetir from cadastro_aneel_go.nota
        where nota = ''
        '''
        self.conexao_datamart.consultar_notas(
            sql=sql_consulta_nota
            
        )
        pass

    def login(self, navegador):
        xpath_login = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input'
        xpath_senha = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/input'
        xpath_enter = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td[3]/table/tbody/tr/td[2]'

        navegador.find_element(by=By.XPATH, value=xpath_login).send_keys('TATE5507011')
        navegador.find_element(by=By.XPATH, value=xpath_senha).send_keys('$mbegp3jJ')
        
        # Clicar no botão de login
        navegador.find_element(by=By.XPATH, value=xpath_enter).click()

        try:
            for _ in range(2):
                try:
                    navegador.implicitly_wait(1)
                    navegador.find_element(By.XPATH, value = "//a[text()='Fechar']")
                    navegador.get('http://bm4e.equatorialenergia.com.br/cbill/loginPage.do')
                    # Preencher usuário e senha
                    navegador.find_element(by=By.XPATH, value=xpath_login).send_keys('TATE5507011')
                    navegador.find_element(by=By.XPATH, value=xpath_senha).send_keys('$mbegp3jJ')
                    # Clicar no botão de login
                    navegador.find_element(by=By.XPATH, value=xpath_enter).click()
                    break
                except:
                    navegador.implicitly_wait(60)
                    pass
        except:
            raise Exception('Erro ao efetuar login')
        
    def search_frame(self, navegador, mainframe_id, request_frame_id):
        while True:
            try:
                navegador.switch_to.default_content()
                navegador.switch_to.frame(mainframe_id)
                request_frame = navegador.find_element(By.ID, request_frame_id)
                navegador.switch_to.frame(request_frame)
                break
            except:
                pass

    def click_if_found(self, navegador, element_click, max_attempts=10): 
        try_order = [By.XPATH, By.ID, By.CLASS_NAME,By.TAG_NAME, By.CSS_SELECTOR]
        for locator_type in try_order:
            for _ in range(max_attempts):
                try:
                    element = navegador.find_element(locator_type, element_click)
                    while not element.is_displayed():
                        pass
                    element.click()
                    return True  # Indica que o clique foi bem-sucedido
                except:
                    time.sleep(1)  # Espera 1 segundo antes de tentar novamente
        raise ErroPrevisto("Erro ao clicar no elemento", (element_click))

    def into_atendimento_ao_cliente(self, navegador):
        titulo_aba_desejada = "CPqD Energia"
        all_windows = navegador.window_handles

        # Itera sobre cada identificador de janela/aba
        for window_handle in all_windows:
            # Alterna para cada janela/aba
            navegador.switch_to.window(window_handle)
            # Verifica se o título da aba é o desejado
            if navegador.title == titulo_aba_desejada:
                # Agora estamos na aba desejada
                break
            
        button_atendimento = '//*[@id="cswmMBtnmenuGroup1"]'
        button_atendimento_ao_cliente = '//*[@id="cswmItmmenuGroup1_0"]'
        while True:
            try:
                elemento_button_atendimento = navegador.find_element(by=By.XPATH, value=button_atendimento)
                while not elemento_button_atendimento.is_displayed():
                    pass
                self.click_if_found(navegador, button_atendimento)      
                navegador.find_element(by=By.XPATH, value=button_atendimento_ao_cliente).click()
                break
            except:
                raise ErroPrevisto('Erro ao clicar em ir para atendimento ao cliente')
            
    def select_tab(self,navegador):
        # Obtem todos os identificadores de janelas/abas abertas
        titulo_aba_desejada = "CPqD Energia - Atendimento ao cliente"
        all_windows = navegador.window_handles

        # Itera sobre cada identificador de janela/aba
        for window_handle in all_windows:
            # Alterna para cada janela/aba
            navegador.switch_to.window(window_handle)
            # Verifica se o título da aba é o desejado
            if navegador.title == titulo_aba_desejada:
                # Agora estamos na aba desejada
                return
            
    def consult_uc(self, navegador, mainframe, topframe, midframe, uc_cbill):
        buscar = '//*[@id="btFind"]'
        control_o = '//*[@id="receptionType6"]'
        uc_code = '//*[@id="ucCode"]'
        try:
            self.search_frame(navegador, mainframe, topframe)
            self.click_if_found(navegador, control_o)
        except:
            raise Exception("Failed to click Control + O")

        try:
            self.search_frame(navegador, mainframe, midframe)
            while True:
                try:
                    uc_input = navegador.find_element(By.XPATH, uc_code)
                    uc_input.send_keys(uc_cbill)
                    break
                except:
                    pass
        except:
            pass  # Não fazer nada se o campo UC não for encontrado

        try:
            self.search_frame(navegador, mainframe, midframe)
            self.click_if_found(navegador, buscar)
        except:
            raise ErroPrevisto("Failed to click Buscar")
        
    def hist_atendimento(self,navegador):
        try:
            actions = ActionChains(navegador)
            actions.key_down(Keys.CONTROL).send_keys(Keys.F10).key_up(Keys.CONTROL).perform()
        except:
            raise ErroPrevisto("Failed to click Historico de Atendimento")
        
    def consultar_leitura(self,navegador, mainframe, midframe):
        try:
            #Clicar em Consulta de Leituras (Ctrl + F8)
            actions = ActionChains(navegador)
            actions.key_down(Keys.CONTROL).send_keys(Keys.F8).key_up(Keys.CONTROL).perform()
            
            self.search_frame(navegador, mainframe, midframe)
            dados_da_uc = '//div[@id="FoldersActive"]/table/tbody/tr/td[1]/div[1]/table/tbody/tr/td[2]/p/a'
            element = navegador.find_element(by=By.XPATH, value = dados_da_uc)
            while not element.is_displayed():
                pass
            ActionChains(navegador).key_down(Keys.ALT).send_keys('u').key_up(Keys.ALT).perform()
        except:
            return ErroPrevisto("Erro ao identificar texto da tabela: {e}")
        
    def encontrar_conexao(self, navegador, mainframe, midframe, ss_da_planilha):
        ss = '//*[@id="SS"]'
        buscar = '//*[@id="btFind"]'
        try:
            navegador.switch_to.default_content()
            navegador.switch_to.frame(mainframe)
            request_frame = navegador.find_element(By.ID, midframe)
            navegador.switch_to.frame(request_frame)
            while True:
                try:
                    navegador.find_element(by=By.XPATH, value=ss).click()
                    self.click_if_found(navegador, buscar)
                    break
                except:
                    pass
            # Encontrar o ID do primeiro elemento e o elemento correspondente
            first_element_id, matching_element = self.get_first_element_and_matching_element(navegador, ss_da_planilha)

            if matching_element:
                # Encontre o elemento <a> dentro do quinto elemento (matching_element)
                link_element = matching_element.find_element(By.TAG_NAME, 'a')
                # Execute a ação desejada com o elemento <a> (por exemplo, clique nele)
                link_element.click()
            else:
                print("Nenhum quinto elemento correspondente encontrado.")
                
        except:
            raise ErroPrevisto("Failed to Encontrar SS Parecer de Acesso")

    def get_first_element_and_matching_element(self, navegador, ss_da_planilha):
        # Nome da classe do elemento que você está procurando
        class_name = 'tableHV'
        try:
            first_element_id = None
            matching_element = None
            
            # Encontre todos os elementos com a classe especificada
            elements = navegador.find_elements(By.CLASS_NAME, class_name)
            
            # Verifique se há elementos encontrados
            if elements:
                # Pegue o ID do primeiro elemento
                first_element_id = elements[1].get_attribute('id')
                
                # Encontre o elemento pelo ID
                first_element = navegador.find_element(By.ID, first_element_id)
                
                # Encontre todas as linhas na tabela
                rows = first_element.find_elements(By.TAG_NAME, 'tr')

                for row in rows:
                    # Encontre o quinto elemento td em cada linha
                    cell = row.find_elements(By.TAG_NAME, 'td')[4]  # índice 4 corresponde ao quinto elemento
                    # Obtenha o texto do quinto elemento td
                    cell_text = cell.text
                    # Compare o texto com o valor de ss_da_planilha
                    if cell_text == ss_da_planilha:
                        # Se forem iguais, guarde o elemento correspondente
                        matching_element = row
                        break  # Pare a iteração, uma vez que encontrou um valor igual
            
            return first_element_id, matching_element
            
        except Exception as e:
            print("Erro ao encontrar o elemento:", e)
            return None, None

    def ver_detalhes_do_cliente(self,navegador, mainframe, midframe):
        actions = ActionChains(navegador)
        actions.key_down(Keys.CONTROL).send_keys(Keys.F9).key_up(Keys.CONTROL).perform()
        
        self.search_frame(navegador, mainframe, midframe)
        
        actions = ActionChains(navegador)
        actions.key_down(Keys.CONTROL).send_keys(Keys.F10).key_up(Keys.CONTROL).perform()
        ver_detalhes_do_cliente = '//a[contains(@href, "/crm-atendimento/protected/crm/customer/customerIdentificationDetail.do")]'
        elemento = navegador.find_element(by=By.XPATH, value = ver_detalhes_do_cliente)
        while not elemento.is_displayed():
            pass
        while True:
            try:
                self.click_if_found(navegador, ver_detalhes_do_cliente)
                break
            except:
                raise ErroPrevisto("Falha ao ir para ver detalhes do cliente")

    def identificar_texto_tabela(self, navegador, mainframe, midframe, num_table):
        self.search_frame(navegador, mainframe, midframe)
        try:
            # Consulta os elementos pela classe 'textCellBdr'
            elementos = navegador.find_elements(by=By.XPATH, value='//*[@class="textCellBdr"]')
            
            # Verifica se há pelo menos um elemento encontrado
            if len(elementos) > num_table:
                # Retorna o texto do elemento correspondente ao número da tabela
                texto = elementos[num_table].text
                return texto
            else:
                return f"Número da tabela {num_table} inválido."
        except:
            raise ErroPrevisto("Erro ao identificar texto da tabela")

    def extrair_nome_e_cpf(self,navegador):
        identificacao = '//*[@id="FoldersActive"]/table/tbody/tr[2]/td[1]/div[1]/table/tbody/tr/td[2]/a'
        elemento_identificacao = navegador.find_element(by=By.XPATH, value = identificacao)
        while not elemento_identificacao.is_displayed():
            pass
        elemento_identificacao.click()
        # Consulta os elementos pela classe 'textCellBdr'
        class_element_cpf = navegador.find_elements(by=By.XPATH, value='//*[@class="textCellBdr"]')

        # Verifica se há pelo menos dois elementos
        if len(class_element_cpf) >= 2:
            # Acessa o primeiro elemento ()
            segundo_elemento = class_element_cpf[0]
            # Obtém o texto do primeiro elemento
            texto_segundo_elemento = segundo_elemento.text

            # Regex para extrair o CPF
            cpf_regex = r"CPF\s+(\d{3}\.\d{3}\.\d{3}-\d{2})"
            cpf_match = re.search(cpf_regex, texto_segundo_elemento)
            if cpf_match:
                cpf = cpf_match.group(1)
            else:
                cpf = "CPF não encontrado"

            # Regex para extrair o nome
            nome_regex = r"Nome:\s+(.*?)\s*Data de nascimento:"
            nome_match = re.search(nome_regex, texto_segundo_elemento)
            if nome_match:
                nome = nome_match.group(1).strip()
            else:
                nome = "Nome não encontrado"

            return {'nome_cliente' : nome, 'cpf' :  cpf}
        else:
            print("Não há elementos suficientes para acessar o segundo.")
            return None, None
        
    def extrair_email_e_tel(self,navegador):
        contato = '//*[@id="FoldersActive"]/table/tbody/tr[2]/td[2]/div[1]/table/tbody/tr/td[2]/a'
        element_contato = navegador.find_element(by=By.XPATH, value = contato)
        while not element_contato.is_displayed:
            pass
        element_contato.click()
        try:
            # Encontrar todas as tabelas com a classe "tableHV"
            tabelas = navegador.find_elements(by=By.XPATH, value='//*[@class="tableHV"]')
            
            # Verificar se há pelo menos uma tabela encontrada
            if tabelas:
                # Iterar sobre as tabelas encontradas
                for tabela in tabelas:
                    # Obter o texto da tabela
                    texto_tabela = tabela.text
                    # Verificar se a tabela tem texto
                    if texto_tabela:
                        # Regex para extrair email
                        email_regex = r"E-mail:\s+(\S+@\S+)"
                        # Regex para extrair número de telefone celular
                        celular_regex = r"\(?(?<!\d)(\d{2})\)?\s*(?:|-|\.)?(\d{5})\s*(?:|-|\.)?(\d{4})"

                        # Procurar por email no texto da tabela
                        email_match = re.search(email_regex, texto_tabela)
                        if email_match:
                            email = email_match.group(1)
                        else:
                            email = None

                        # Procurar por número de telefone celular no texto da tabela
                        celular_match = re.search(celular_regex, texto_tabela)
                        if celular_match:
                            celular = f"{celular_match.group(1)} {celular_match.group(2)}-{celular_match.group(3)}"
                        else:
                            celular = None

                        return {'email': email, 'tel_movel' : celular}
                # Se nenhuma tabela tiver conteúdo, retornar uma mensagem indicando isso
                return "Nenhuma tabela com conteúdo encontrado."
            else:
                # Se nenhuma tabela for encontrada, retornar uma mensagem indicando isso
                return "Nenhuma tabela encontrada."
        except:
            raise ErroPrevisto('Erro ao extrair email e telefone')

    def extrair_dados_da_uc(self, navegador, mainframe, midframe, num_table):
        texto_tabela = self.identificar_texto_tabela(navegador, mainframe, midframe, num_table)
        try:
            # Dividir o texto da tabela em linhas
            linhas = texto_tabela.split('\n')
            
            # Valor (Grupo/Subgrupo)
            grupo_subgrupo = linhas[2].strip()
            grupo_subgrupo = grupo_subgrupo.split(' - ')[1].strip()  # Apenas a segunda parte do texto
            
            classe_consumo_linha = linhas[17].strip()
            partes = classe_consumo_linha.split('|', 1)
            if len(partes) >= 1:
                classe_consumo = partes[0].strip()
                classe_consumo = re.sub(r"[^a-zA-Z]", "", classe_consumo).capitalize()
            else:
                classe_consumo = None
            
            # Inicializar variáveis para o CEP e a localidade
            cep = None
            localidade = None
            linha_cep_encontrada = None

            # Iterar sobre todas as linhas para encontrar o padrão do CEP
            for linha_index, linha in enumerate(linhas):
                cep_match = re.search(r"\b\d{5}-\d{3}\b", linha)
                if cep_match:
                    # Se encontrar o padrão do CEP, guardar a linha e extrair o CEP
                    cep = cep_match.group()
                    localidade_match = re.search(r"^\w+(?:\s+\w+)*", linha.lower())
                    localidade = localidade_match.group() if localidade_match else None
                    linha_cep_encontrada = linha_index
                    break

            # Retornar os valores encontrados
            return {'gru_tar': grupo_subgrupo, 'municipio': localidade, 'cep': cep, 'classe_consumo': classe_consumo}
            
        except Exception as e:
            raise ErroPrevisto("Erro ao extrair dados da UC:", {e})
        
    def extrair_uc_e_endereco(self,navegador, mainframe, midframe, num_table):
        texto_tabela = self.identificar_texto_tabela(navegador, mainframe, midframe, num_table)
        try:
            # Dividir o texto da primeira tabela em linhas
            linhas_1 = texto_tabela.split('\n')

            # Valor da UC
            uc = linhas_1[2].split(" - ")[0].strip()

            # Encontrar o índice onde o endereço começa
            indice_inicio_endereco = linhas_1[2].find(" - ") + len(" - ")

            # Encontrar o índice onde o endereço termina
            indice_fim_endereco = linhas_1[2].find(" Razão/Rota/Roteiro:")

            # Valor do endereço, removendo a primeira palavra
            endereco = linhas_1[2][indice_inicio_endereco:indice_fim_endereco].strip().split(' ', 1)[1]

            # Retornar os valores
            return {'conta_contrato': uc, 'endereco': endereco}
            
        except Exception as e:
            ErroPrevisto("Erro ao extrair informações de contato:", e)
            return None, None

    def extrair_data_da_construcao(self,navegador, mainframe, midframe):
        data_da_construcao = '/html/body/form/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/span'
        try:
            self.search_frame(navegador, mainframe, midframe)
            # Encontrar o segundo elemento
            elemento = navegador.find_element(by=By.XPATH, value=data_da_construcao)
            # Extrair o texto do segundo elemento
            data_completa = elemento.text

            # Dividir a string no espaço em branco e selecionar apenas a parte da data
            data = data_completa.split()[0]

            # Criar o dicionário com a chave 'data_da_construcao' e o valor completo
            return {'data_solicitacao_conexao_gd': data}
        except Exception as e:
            ErroPrevisto("Erro ao encontrar data da construção:", e)
            return None
        
    def extrair_data_da_conexao(self,navegador, mainframe, midframe):
        element = navegador.find_element(by=By.XPATH, value= '//*[@id="dados_gerais"]/tbody/tr/td[5]/div/table/tbody/tr/td[2]')
        while not element.is_displayed():
            pass
        element.click()
        try:
            self.search_frame(navegador, mainframe, midframe)
            # Encontrar o iframe pelo ID
            iframe_element = navegador.find_element(By.ID, 'write_off_date_frame')

            # Mudar para o contexto do iframe
            navegador.switch_to.frame(iframe_element)

            # Encontrar todos os elementos <tr> dentro do iframe
            elementos_tr = navegador.find_elements(By.TAG_NAME, 'tr')

            # Contar quantos elementos <tr> foram encontrados
            numero_tr = len(elementos_tr)

            # Verificar se há pelo menos dois elementos <tr>
            if numero_tr >= 2:
                # Ler o texto do segundo elemento <tr>
                texto_segundo_tr = elementos_tr[1].text
                
                data_da_conexao = texto_segundo_tr.split()[3]
                
                return {'data_aprov_p_conexao': data_da_conexao}
            else:
                return numero_tr, "Não há elementos suficientes"
        except Exception as e:
            print("Erro ao encontrar elemento e contar tr:", e)
            return None, None
    
    def extrair_modalidade(self, navegador, mainframe, midframe, uc_cbill):
        try:
            actions = ActionChains(navegador)
            actions.key_down(Keys.CONTROL).send_keys(Keys.F3).key_up(Keys.CONTROL).perform()
            self.search_frame(navegador, mainframe, midframe)
            element = navegador.find_element(by=By.XPATH, value='//*[@id="consultCompensationLink"]')
            element.click()
            elemento_tr = navegador.find_element(By.XPATH, f'//td[text()="{uc_cbill}"]/ancestor::tr')
            texto = elemento_tr.text
            tabela = texto.split('\n')
                
            # Remove as duas primeiras e as duas últimas linhas do texto
            linhas_restantes = tabela[2:-2]

            # Calcula a quantidade de linhas restantes
            quantidade_linhas = len(linhas_restantes)

            if len(linhas_restantes) > 2:
                return {'modalidade': 'Autoconsumo remoto', 'qtd_gd': quantidade_linhas}
            else:
                return {'modalidade': 'Geração na própria UC', 'qtd_gd': quantidade_linhas}
        except Exception as e:
            return f"Erro ao identificar texto da tabela: {e}"
        
    def inserir_dados_no_banco(self,navegador, midframe, mainframe, ss_da_planilha, uc_cbill):
        dicionario_principal = {}
        dicionario_principal = dicionario_principal | self.extrair_email_e_tel(navegador)
        dicionario_principal = dicionario_principal | self.extrair_nome_e_cpf(navegador)
        self.consultar_leitura(navegador, mainframe, midframe)
        dicionario_principal = dicionario_principal | self.extrair_uc_e_endereco(navegador, mainframe, midframe, num_table=0)
        dicionario_principal = dicionario_principal | self.extrair_dados_da_uc(navegador, mainframe, midframe, num_table=1)
        self.hist_atendimento(navegador)
        self.encontrar_conexao(navegador, mainframe, midframe, ss_da_planilha)
        dicionario_principal = dicionario_principal | self.extrair_data_da_conexao(navegador, mainframe, midframe)
        dicionario_principal = dicionario_principal | self.extrair_data_da_construcao(navegador, mainframe, midframe)
        dicionario_principal = dicionario_principal | self.extrair_modalidade(navegador, mainframe, midframe, uc_cbill)
            
        return dicionario_principal

    def scraping(self, uc_cbill, ss_da_planilha):
        
        navegador = self.open_browser()
        
        self.login(navegador)
        
        self.into_atendimento_ao_cliente(navegador)
        
        self.select_tab(navegador)
        
        self.consult_uc(navegador, self.main_frame, self.top_frame, self.mid_frame, uc_cbill)

        self.ver_detalhes_do_cliente(navegador, self.main_frame, self.mid_frame)

        dicionario_principal = self.inserir_dados_no_banco(navegador, self.mid_frame, self.main_frame, ss_da_planilha, uc_cbill)

        navegador.quit()

        return dicionario_principal