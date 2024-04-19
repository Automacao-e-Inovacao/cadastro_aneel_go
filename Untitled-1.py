
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pyautogui
import os
import time
import re

main_frame = 'contentCRM'
top_frame = 'sessionheader'
mid_frame = 'principal'
botton_frame = 'active_browser_funcs'

uc_cbill = '10006787760'
ss_da_planilha = '163890270'

def iniciar_navegador():
    chrome_options = webdriver.ChromeOptions()
    navegador = webdriver.Chrome(options=chrome_options)
    navegador.implicitly_wait(200)
    navegador.get('http://10.125.6.102:11090/cbill/loginPage.do')
    return navegador

def login(navegador):
    erro_login = '//*[@id="MensagemErro"]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/span'
    xpath_login = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input'
    xpath_senha = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/input'
    xpath_enter = '//*[@id="bodyDiv"]/div/form/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td[3]/table/tbody/tr/td[2]'
   
    try:
        # Preencher usuário e senha
        navegador.find_element(by=By.XPATH, value=xpath_login).send_keys('TATE5507011')
        navegador.find_element(by=By.XPATH, value=xpath_senha).send_keys('$mbegp3jJ')
        
        # Clicar no botão de login
        navegador.find_element(by=By.XPATH, value=xpath_enter).click()
        
    except:
        # Se houver erro, imprimir mensagem de erro
        erro_login_element = navegador.find_element(by=By.XPATH, value=erro_login)
        texto = erro_login_element.text
        print(texto)
       
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

def click_if_found(navegador, element_click, max_attempts=10): 
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
    return False  # Indica que não foi possível realizar o clique após o número máximo de tentativas

def into_atendimento_ao_cliente(navegador):
    button_atendimento = '//*[@id="cswmMBtnmenuGroup1"]'
    button_atendimento_ao_cliente = '//*[@id="cswmItmmenuGroup1_0"]'
    while True:
        try:
            elemento_button_atendimento = navegador.find_element(by=By.XPATH, value=button_atendimento)
            while not elemento_button_atendimento.is_displayed():
                pass
            elemento_button_atendimento.click()       
            navegador.find_element(by=By.XPATH, value=button_atendimento_ao_cliente).click()
            break
        except:
            pass
        
def select_tab(navegador):
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
        
def consult_uc(navegador, mainframe, topframe, midframe, uc_cbill):
    buscar = 'btFind'
    control_o = 'receptionType6'
    uc_code = '//*[@id="ucCode"]'
    try:
        search_frame(navegador, mainframe, topframe)
        click_if_found(navegador, control_o)
    except:
        raise Exception("Failed to click Control + O")

    try:
        search_frame(navegador, mainframe, midframe)
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
        search_frame(navegador, mainframe, midframe)
        click_if_found(navegador, buscar)
    except:
        raise Exception("Failed to click Buscar")
    
def hist_atendimento(navegador, bottonframe, mainframe, midframe):
    try:
        search_frame(navegador, mainframe, midframe)
        navegador.find_elements(by=By.XPATH, value='//*[@class="textCellBdr"]')
        element = navegador.find_element(by=By.XPATH, value='//a[contains(@href, "/crm-atendimento/protected/crm/customer/customerIdentificationDetail.do")]')
        while not element.is_displayed():
            pass
        navegador.switch_to.default_content()
        navegador.switch_to.frame(bottonframe)
        element = '//*[@id="historico"]/div'
        click_if_found(navegador, element)
    except:
        raise Exception("Failed to click Historico de Atendimento")
    
def consultar_leitura(navegador, bottonframe, mainframe, midframe):
    try:
        #Clicar em Consulta de Leituras (Ctrl + F8)
        navegador.switch_to.default_content()
        navegador.switch_to.frame(bottonframe)
        navegador.find_element(by=By.XPATH, value='//*[@id="leituras"]/div').click()
        
        search_frame(navegador, mainframe, midframe)
        dados_da_uc = '//*[@id="FoldersActive"]/table/tbody/tr/td[1]/div[1]/table/tbody/tr/td[2]/p/a'
        element = navegador.find_element(by=By.XPATH, value = dados_da_uc)
        while not element.is_displayed():
            pass
        element.click()
        navegador.find_element(by=By.XPATH, value= dados_da_uc).click()
    except Exception as e:
        return f"Erro ao identificar texto da tabela: {e}"
        
def consulta_de_contas(navegador, bottonframe, mainframe, midframe):
    try:
        search_frame(navegador, mainframe, midframe)
        navegador.find_elements(by=By.XPATH, value='//*[@class="textCellBdr"]')
        element = navegador.find_element(by=By.XPATH, value='//a[contains(@href, "/crm-atendimento/protected/crm/customer/customerIdentificationDetail.do")]')
        while not element.is_displayed():
            pass
        navegador.switch_to.default_content()
        navegador.switch_to.frame(bottonframe)
        element = navegador.find_element(by=By.XPATH, value='//*[@id="contas"]')
        element.click()
        pass
    except Exception as e:
        return f"Erro ao identificar texto da tabela: {e}"
    
def encontrar_conexao(navegador, mainframe, midframe,  buscar, ss_da_planilha):
    ss = '//*[@id="SS"]'
    try:
        navegador.switch_to.default_content()
        navegador.switch_to.frame(mainframe)
        request_frame = navegador.find_element(By.ID, midframe)
        navegador.switch_to.frame(request_frame)
        while True:
            try:
                navegador.find_element(by=By.XPATH, value=ss).click()
                click_if_found(navegador, buscar)
                break
            except:
                pass
        # Encontrar o ID do primeiro elemento e o elemento correspondente
        first_element_id, matching_element = get_first_element_and_matching_element(navegador, ss_da_planilha)

        if matching_element:
            # Encontre o elemento <a> dentro do quinto elemento (matching_element)
            link_element = matching_element.find_element(By.TAG_NAME, 'a')
            # Execute a ação desejada com o elemento <a> (por exemplo, clique nele)
            link_element.click()
        else:
            print("Nenhum quinto elemento correspondente encontrado.")
            
    except:
        raise Exception("Failed to Encontrar SS Parecer de Acesso")
    
def get_first_element_and_matching_element(driver, ss_da_planilha):
        # Nome da classe do elemento que você está procurando
    class_name = 'tableHV'
    try:
        first_element_id = None
        matching_element = None
        
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
                # Compare o texto com o valor de ss_da_planilha
                if cell_text == ss_da_planilha:
                    # Se forem iguais, guarde o elemento correspondente
                    matching_element = row
                    break  # Pare a iteração, uma vez que encontrou um valor igual
        
        return first_element_id, matching_element
    
    except Exception as e:
        print("Erro ao encontrar o elemento:", e)
        return None, None

def ver_detalhes_do_cliente(navegador, mainframe, midframe):
    search_frame(navegador, mainframe, midframe)
    ver_detalhes_do_cliente = '//a[contains(@href, "/crm-atendimento/protected/crm/customer/customerIdentificationDetail.do")]'
    while True:
        try:
            click_if_found(navegador, ver_detalhes_do_cliente)
            break
        except:
            raise Exception("Falha ao ir para ver detalhes do cliente")

def identificar_texto_tabela(navegador, mainframe, midframe):
    search_frame(navegador, mainframe, midframe)
    try:
        # Consulta os elementos pela classe 'textCellBdr'
        elementos = navegador.find_elements(by=By.XPATH, value='//*[@class="textCellBdr"]')
        
        # Verifica se há pelo menos dois elementos encontrados
        if len(elementos) >= 2:
            # Retorna o texto do primeiro e do segundo elemento encontrados
            texto_1 = elementos[0].text
            texto_2 = elementos[1].text
            return texto_1, texto_2
        else:
            return "Menos de dois elementos encontrados com a classe 'textCellBdr'."
    except Exception as e:
        return f"Erro ao identificar texto da tabela: {e}"    

def extrair_nome_e_cpf(navegador):
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
    
def extrair_email_e_tel(navegador):
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
    except Exception as e:
        # Se ocorrer algum erro, retornar a mensagem de erro
        return f"Erro ao extrair email e telefone: {e}"

def extrair_dados_da_uc(texto_tabela):
    try:
        # Dividir o texto da tabela em linhas
        linhas = texto_tabela.split('\n')
        
        # Valor (Grupo/Subgrupo)
        grupo_subgrupo = linhas[2].strip()
        grupo_subgrupo = grupo_subgrupo.split(' - ')[1].strip()  # Apenas a segunda parte do texto
        
        # Tentar extrair o CEP e a localidade da linha 27
        linha_cep_localidade = linhas[27]

        # Extrair o CEP usando expressão regular
        cep_match = re.search(r"\b\d{5}-\d{3}\b", linha_cep_localidade)
        if cep_match:
            cep = cep_match.group()
        else:
            # Se não encontrar o CEP na linha 27, tentar na linha 28
            linha_cep_localidade = linhas[28]
            cep_match = re.search(r"\b\d{5}-\d{3}\b", linha_cep_localidade)
            cep = cep_match.group() if cep_match else None

        # Extrair a localidade
        localidade_match = re.search(r"^\w+", linha_cep_localidade.lower())
        localidade = localidade_match.group() if localidade_match else None

        # Retornar os valores encontrados
        return {'gru_tar': grupo_subgrupo, 'localidade': localidade, 'cep': cep}
        
    except Exception as e:
        print("Erro ao extrair dados da UC:", e)
        return None
    
def extrair_uc_e_endereco(texto_tabela):
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
        print("Erro ao extrair informações de contato:", e)
        return None, None

def extrair_data_da_construcao(navegador, mainframe, midframe):
    data_da_construcao = '/html/body/form/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/span'
    try:
        search_frame(navegador, mainframe, midframe)
        # Encontrar o segundo elemento
        elemento = navegador.find_element(by=By.XPATH, value=data_da_construcao)
        # Extrair o texto do segundo elemento
        data_completa = elemento.text

        # Dividir a string no espaço em branco e selecionar apenas a parte da data
        data = data_completa.split()[0]

        # Criar o dicionário com a chave 'data_da_construcao' e o valor completo
        return {'data_da_construcao': data}
    except Exception as e:
        print("Erro ao encontrar data da construção:", e)
        return None
    
def extrair_data_da_conexao(navegador, mainframe, midframe):
    element = navegador.find_element(by=By.XPATH, value= '//*[@id="dados_gerais"]/tbody/tr/td[5]/div/table/tbody/tr/td[2]')
    while not element.is_displayed():
        pass
    element.click()
    try:
        search_frame(navegador, mainframe, midframe)
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
            
            return {'data_da_conexao': data_da_conexao}
        else:
            return numero_tr, "Não há elementos suficientes"
    except Exception as e:
        print("Erro ao encontrar elemento e contar tr:", e)
        return None, None
    
def inserir_dados_no_banco(navegador):
    dicionario_principal = {}
    dicionario_principal = dicionario_principal | extrair_email_e_tel(navegador)
    dicionario_principal = dicionario_principal | extrair_nome_e_cpf(navegador)
    consultar_leitura(navegador, botton_frame, main_frame, mid_frame)
    texto_1, texto_2 = identificar_texto_tabela(navegador, main_frame, mid_frame)
    dicionario_principal = dicionario_principal | extrair_uc_e_endereco(texto_1)
    dicionario_principal = dicionario_principal | extrair_dados_da_uc(texto_2)
    hist_atendimento(navegador, botton_frame, main_frame, mid_frame)
    encontrar_conexao(navegador, main_frame, mid_frame, ss, buscar, ss_do_parecer)
    dicionario_principal = dicionario_principal | extrair_data_da_conexao(navegador, main_frame, mid_frame)
    dicionario_principal = dicionario_principal | extrair_data_da_construcao(navegador, main_frame, mid_frame)
        
    return dicionario_principal

navegador = iniciar_navegador()
navegador.implicitly_wait(1)
login(navegador)

into_atendimento_ao_cliente(navegador)

select_tab(navegador)

def scraping():

    consult_uc(navegador, main_frame, top_frame, mid_frame, uc_cbill,)

    hist_atendimento(navegador, botton_frame, main_frame, mid_frame)

    ver_detalhes_do_cliente(navegador, main_frame, mid_frame)

    dicionario_principal = inserir_dados_no_banco(navegador)

    return dicionario_principal