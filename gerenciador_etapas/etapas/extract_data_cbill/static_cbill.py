from selenium.webdriver.common.by import By

xpath_login = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input'
xpath_senha = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/input'
xpath_enter = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td[3]/table/tbody/tr/td[2]'
button_atendimento = '//*[@id="cswmMBtnmenuGroup1"]'
button_atendimento_ao_cliente = '//*[@id="cswmItmmenuGroup1_0"]'
erro_login = '//*[@id="MensagemErro"]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/span'
uc_code = '//*[@id="ucCode"]'
uc_cbill = '10005016140'
buscar = 'btFind'
main_frame = 'contentCRM'
top_frame = 'sessionheader'
mid_frame = 'principal'
botton_frame = 'active_browser_funcs'
historico_de_atendimento = '//*[@id="historico"]/div'
control_o = 'receptionType6'
ss = '//*[@id="SS"]'
class_name = 'tableHV'

def into_atendimento_ao_cliente(self, navegador):
    while True:
        try:
            elemento_button_atendimento = navegador.find_element(By.XPATH, self.inst_elementos_cbill.button_atendimento)
            while not elemento_button_atendimento.is_displayed():
                pass
            elemento_button_atendimento.click()       
            navegador.find_element(By.XPATH, self.inst_elementos_cbill.button_atendimento_ao_cliente).click()
            break
        except:
            pass    

def select_tab(self, navegador):
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

def login_cbill(self, driver):
    try:
        # Encontrar os campos de login e senha e preenchê-los
        driver.find_element(By.XPATH, self.inst_elementos_cbill.xpath_login).send_keys(self.usuario_cbill)
        driver.find_element(By.XPATH, self.inst_elementos_cbill.xpath_senha).send_keys(self.senha_cbill)

        # Clicar no botão de login
        driver.find_element(By.XPATH, self.inst_elementos_cbill.xpath_enter).click()
        
        # Executar as próximas etapas
        self.into_atendimento_ao_cliente(driver)
        self.select_tab(driver)
        
    except Exception as e:
        print("Erro ao fazer login no CBILL:", e)
   
def search_frame(navegador, mainframe_id, request_frame_id):
    while True:
        try:
            navegador.switch_to.default_content()
            navegador.switch_to.frame(mainframe_id)
            request_frame = navegador.find_element(By.ID, request_frame_id)
            navegador.switch_to.frame(request_frame)
            break
        except:
            pass

def click_if_found(navegador, element_click): 
    try_order = [By.ID, By.XPATH, By.TAG_NAME, By.CSS_SELECTOR]
    for locator_type in try_order:
        try:
            element = navegador.find_element(locator_type, element_click)
            while not element.is_displayed():
                pass
            element.click()
            return  # Parar a execução se o elemento for encontrado com sucesso
        except:
            pass
        
def consult_uc(navegador, topframe, midframe, control_o, uc_code, uc_cbill, buscar):
    try:
        search_frame(navegador, main_frame, topframe)
        click_if_found(navegador, control_o)
    except:
        raise Exception("Failed to click Control + O")

    try:
        search_frame(navegador, main_frame, midframe)
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
        search_frame(navegador, main_frame, midframe)
        click_if_found(navegador, buscar)
    except:
        raise Exception("Failed to click Buscar")
    
def hist_atendimento(navegador, bottonframe):
    try:
        navegador.switch_to.default_content()
        navegador.switch_to.frame(bottonframe)
        element = navegador.find_element(by=By.XPATH, value='//*[@id="historico"]/div')
        while not element.is_displayed():
            pass
        element.click()
    except:
        raise Exception("Failed to click Historico de Atendimento")
    
def encontrar_conexao(navegador, mainframe, midframe, ss, buscar):
    navegador.switch_to.default_content()
    navegador.switch_to.frame(mainframe)
    request_frame = navegador.find_element(By.ID, midframe)
    navegador.switch_to.frame(request_frame)
    try:
        navegador.find_element(by=By.XPATH, value=ss).click()
        while True:
            try:
                click_if_found(navegador, buscar)
                break
            except:
                pass
    except:
        raise Exception("Failed to Encontrar SS Parecer de Acesso")

def find_ss_do_parecer(driver, ss_do_parecer_value):
    try:
        first_element_id = None
        matching_element = None
        class_name = 'tableHV'
        
        # Encontre todos os elementos com a classe especificada
        elements = driver.find_elements(By.CLASS_NAME, class_name)
        
        # Verifique se há elementos encontrados
        if elements:
            # Pegue o ID do primeiro elemento
            first_element_id = elements[1].get_attribute('id')
            
            # Encontre o elemento pelo ID
            first_element = driver.find_element(By.ID, first_element_id)
            
            # Encontre todas as linhas na tabela
            rows = first_element.find_elements(By.TAG_NAME, 'tr')

            for row in rows:
                # Encontre o quinto elemento td em cada linha
                cell = row.find_elements(By.TAG_NAME, 'td')[4]  # índice 4 corresponde ao quinto elemento
                # Obtenha o texto do quinto elemento td
                cell_text = cell.text
                # Compare o texto com o valor de ss_do_parecer_value
                if cell_text == ss_do_parecer_value:
                    # Se forem iguais, guarde o elemento correspondente
                    matching_element = row
                    break  # Pare a iteração, uma vez que encontrou um valor igual
                
        return first_element_id, matching_element
    
    except Exception as e:
        print("Erro ao encontrar o elemento:", e)
        return None, None

def click_ss_do_parecer(navegador, class_name, ss_do_parecer_value):
    try:
        # Chama a função find_ss_do_parecer para obter o first_element_id
        first_element_id, matching_element = find_ss_do_parecer(navegador, class_name, ss_do_parecer_value)
        if matching_element:
            # Encontre o elemento <a> dentro do quinto elemento (matching_element)
            link_element = matching_element.find_element(By.TAG_NAME, 'a')
            # Execute a ação desejada com o elemento <a> (por exemplo, clique nele)
            link_element.click()
    except Exception as e:
        print("Erro ao clicar no elemento:", e)

def extrair_email_e_tel(navegador):
    element_contato = '//*[@id="FoldersActive"]/table/tbody/tr[2]/td[2]/div[1]/table/tbody/tr/td[2]/a'
    navegador.find_element(by=By.XPATH, value=element_contato).click()
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

                    return email, celular
            # Se nenhuma tabela tiver conteúdo, retornar uma mensagem indicando isso
            return "Nenhuma tabela com conteúdo encontrado."
        else:
            # Se nenhuma tabela for encontrada, retornar uma mensagem indicando isso
            return "Nenhuma tabela encontrada."
    except Exception as e:
        # Se ocorrer algum erro, retornar a mensagem de erro
        return f"Erro ao extrair email e telefone: {e}"


