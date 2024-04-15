# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import os
import re

# %%
link_cbill = 'http://10.125.6.102:11090/cbill/loginPage.do'
usuario_cbill = 'TATE5507011'
senha_cbill = '$mbegp3jJ'
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
ss_do_parecer = '164707086'

# %%
chrome_options = webdriver.ChromeOptions()
navegador = webdriver.Chrome(options= chrome_options)
navegador.implicitly_wait(200)
navegador.get(link_cbill)

# %%
#Mudando o implicity wait para testes de elemtento (ALTERAR DEPOIS)
navegador.implicitly_wait(1)

# %%
def tentativa_login(navegador, usuario_cbill, senha_cbill):
    try:
        # Preencher usuário e senha
        navegador.find_element(by=By.XPATH, value=xpath_login).send_keys(usuario_cbill)
        navegador.find_element(by=By.XPATH, value=xpath_senha).send_keys(senha_cbill)
        
        # Clicar no botão de login
        navegador.find_element(by=By.XPATH, value=xpath_enter).click()
        
    except:
        # Se houver erro, imprimir mensagem de erro
        erro_login_element = navegador.find_element(by=By.XPATH, value=erro_login)
        texto = erro_login_element.text
        print(texto)
        
tentativa_login(navegador = navegador, usuario_cbill=usuario_cbill, senha_cbill=senha_cbill)


# %%
#Clicar apenas quando o elemento estiver visível
def into_atendimento_ao_cliente():
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
into_atendimento_ao_cliente()

# %%
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

# Exemplo de uso da função

# Chamada da função passando o navegador e o título da aba desejada
select_tab(navegador)


# %%
def search_frame(navegador, mainframe_id, request_frame_id):
    while True:
        try:
            navegador.switch_to.default_content()
            navegador.switch_to.frame(mainframe_id)
            request_frame = navegador.find_element(By.ID, request_frame_id)
            navegador.switch_to.frame(request_frame)
            break
        except NoSuchElementException:
            pass

def click_if_found(navegador, element_click): 
    try_order = [By.ID, By.CLASS_NAME, By.XPATH, By.TAG_NAME, By.CSS_SELECTOR]
    for locator_type in try_order:
        try:
            element = navegador.find_element(locator_type, element_click)
            while not element.is_displayed():
                pass
            element.click()
            return  # Parar a execução se o elemento for encontrado com sucesso
        except NoSuchElementException:
            pass


# %%
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

# %%
def hist_atendimento(navegador, bottonframe):
    time.sleep(5)
    try:
        navegador.switch_to.default_content()
        navegador.switch_to.frame(bottonframe)
        element = navegador.find_element(by=By.XPATH, value='//*[@id="historico"]/div')
        while not element.is_displayed():
            pass
        element.click()
    except:
        raise Exception("Failed to click Historico de Atendimento")

# %%
navegador.find_element(by=By.XPATH, value='//*[@id="historico"]/div')

# %%
def encontrar_frame_atual(driver):
    """
    Retorna o nome do frame em que o webdriver está atualmente.
    Se não estiver em nenhum frame, retorna None.
    """
    frame_atual = None
    try:
        frame_atual = driver.execute_script("return self.name;")
    except:
        pass
    return frame_atual

frame_atual = encontrar_frame_atual(navegador)
if frame_atual:
    print("Estou no frame:", frame_atual)
else:
    print("Não estou em nenhum frame.")


# %%
def encontrar_conexao(navegador, mainframe, midframe, ss, buscar):
    hist_atendimento(navegador, botton_frame)
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
    except:
        raise Exception("Failed to Encontrar SS Parecer de Acesso")


# %%
def ver_detalhes_do_cliente(navegador, mainframe, midframe, topframe):
    time.sleep(5)
    try:
        consult_uc(navegador, topframe, midframe, control_o, uc_code, uc_cbill, buscar)
        encontrar_conexao(navegador, main_frame, mid_frame, ss, buscar)
    except:
        raise Exception("Falha ao consultar uc")
    time.sleep(5)
    ver_detalhes_do_cliente = '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td[3]/a[2]'
    while not ver_detalhes_do_cliente.is_displayed():
        pass
    navegador.switch_to.default_content()
    navegador.switch_to.frame(mainframe)
    request_frame = navegador.find_element(By.ID, midframe)
    navegador.switch_to.frame(request_frame)
    while True:
        try:
            click_if_found(navegador, ver_detalhes_do_cliente)
            break
        except:
            raise Exception("Falha ao ir para ver detalhes do cliente")


# %%
def extrair_nome_e_cpf(navegador):
    ver_detalhes_do_cliente(navegador, main_frame, mid_frame)
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

        return nome, cpf
    else:
        print("Não há elementos suficientes para acessar o segundo.")
        return None, None



# %%
nome, cpf = extrair_nome_e_cpf(navegador)
if nome and cpf:
    print("Nome:", nome)
    print("CPF:", cpf)
else:
    print("Não foi possível extrair o Nome e o CPF.")

# %%
def get_first_element_and_matching_element(driver, class_name, ss_do_parecer_value):
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
                # Compare o texto com o valor de ss_do_parecer_value
                if cell_text == ss_do_parecer_value:
                    # Se forem iguais, guarde o elemento correspondente
                    matching_element = row
                    break  # Pare a iteração, uma vez que encontrou um valor igual
        
        return first_element_id, matching_element
    
    except Exception as e:
        print("Erro ao encontrar o elemento:", e)
        return None, None

# Nome da classe do elemento que você está procurando
class_name = 'tableHV'

# Valor do objeto "ss_do_parecer"
ss_do_parecer_value = ss_do_parecer

# Obtenha o ID do primeiro elemento e o elemento correspondente
first_element_id, matching_element = get_first_element_and_matching_element(navegador, class_name, ss_do_parecer_value)

if matching_element:
    # Encontre o elemento <a> dentro do quinto elemento (matching_element)
    link_element = matching_element.find_element(By.TAG_NAME, 'a')
    # Execute a ação desejada com o elemento <a> (por exemplo, clique nele)
    link_element.click()
else:
    print("Nenhum quinto elemento correspondente encontrado.")


# %%
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
            except NoSuchElementException:
                pass
    except:
        pass  # Não fazer nada se o campo UC não for encontrado

    try:
        search_frame(navegador, main_frame, midframe)
        click_if_found(navegador, buscar)
    except:
        raise Exception("Failed to click Buscar")

def hist_atendimento(navegador, bottonframe):
    time.sleep(5)
    try:
        navegador.switch_to.default_content()
        navegador.switch_to.frame(bottonframe)
        element = navegador.find_element(by=By.XPATH, value='//*[@id="historico"]/div')
        while not element.is_displayed():
            pass
        element.click()
    except NoSuchElementException:
        raise Exception("Failed to click Historico de Atendimento")

def encontrar_conexao(navegador, mainframe, midframe, ss, buscar):
    hist_atendimento(navegador, botton_frame)
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
            except NoSuchElementException:
                pass
    except NoSuchElementException:
        raise Exception("Failed to Encontrar SS Parecer de Acesso")

def ver_detalhes_do_cliente(navegador, mainframe, midframe, topframe):
    time.sleep(5)
    try:
        consult_uc(navegador, topframe, midframe, control_o, uc_code, uc_cbill, buscar)
        encontrar_conexao(navegador, main_frame, mid_frame, ss, buscar)
    except:
        raise Exception("Falha ao consultar uc")
    ver_detalhes_do_cliente = '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td[3]/a[2]'

    navegador.switch_to.default_content()
    navegador.switch_to.frame(mainframe)
    request_frame = navegador.find_element(By.ID, midframe)
    navegador.switch_to.frame(request_frame)
    while True:
        try:
            navegador.find_element(by=By.XPATH, value= ver_detalhes_do_cliente).click()
            break
        except NoSuchElementException:
            raise Exception("Falha ao ir para ver detalhes do cliente")

def extrair_nome_e_cpf(navegador):
    ver_detalhes_do_cliente(navegador, main_frame, mid_frame, top_frame)
    # Consulta os elementos pela classe 'textCellBdr'
    time.sleep(5)
    class_element_cpf = navegador.find_elements(by=By.XPATH, value='//*[@class="textCellBdr"]')

    # Verifica se há pelo menos dois elementos
    if len(class_element_cpf) >= 1:  # Mudei de 2 para 1, pois você deseja acessar o primeiro elemento
        # Acessa o primeiro elemento
        primeiro_elemento = class_element_cpf[0]
        # Obtém o texto do primeiro elemento
        texto_primeiro_elemento = primeiro_elemento.text

        # Regex para extrair o CPF
        cpf_regex = r"CPF\s+(\d{3}\.\d{3}\.\d{3}-\d{2})"
        cpf_match = re.search(cpf_regex, texto_primeiro_elemento)
        if cpf_match:
            cpf = cpf_match.group(1)
        else:
            cpf = "CPF não encontrado"

        # Regex para extrair o nome
        nome_regex = r"Nome:\s+(.*?)\s*Data de nascimento:"
        nome_match = re.search(nome_regex, texto_primeiro_elemento)
        if nome_match:
            nome = nome_match.group(1).strip()
        else:
            nome = "Nome não encontrado"

        return nome, cpf
    else:
        print("Não há elementos suficientes para acessar o segundo.")
        return None, None


# %%
extrair_nome_e_cpf(navegador)

# %%
class_consultar_email = navegador.find_elements(by=By.XPATH, value='//*[@class="tableHV"]')

# %%
def obter_texto_primeira_tabela(navegador):
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
                    # Retornar o texto da primeira tabela encontrada com conteúdo
                    return texto_tabela
            # Se nenhuma tabela tiver conteúdo, retornar uma mensagem indicando isso
            return "Nenhuma tabela com conteúdo encontrado."
        else:
            # Se nenhuma tabela for encontrada, retornar uma mensagem indicando isso
            return "Nenhuma tabela encontrada."
    except Exception as e:
        # Se ocorrer algum erro, retornar a mensagem de erro
        return f"Erro ao obter texto da tabela: {e}"

# Exemplo de uso:
texto_tabela = obter_texto_primeira_tabela(navegador)
print(texto_tabela)


# %%


# %%
encontrar_frame_atual(navegador)

# %%
ver_detalhes_do_cliente = '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td[3]/a[2]'

# %%
navegador.find_element(by=By.XPATH, value= ver_detalhes_do_cliente)

# %%

def get_first_element_and_matching_element(driver, class_name,):
    try:
        # Encontre todos os elementos com a classe especificada
        elements = driver.find_elements(By.CLASS_NAME, class_name)
        
        # Verifique se há elementos encontrados
        if elements:
            # Pegue o ID do primeiro elemento
            first_element_id = elements[1].get_attribute('id')
    
    except Exception as e:
        print("Erro ao encontrar o elemento:", e)
        return None, None

# %%
try:
    nome, cpf = extrair_nome_e_cpf(navegador)
    if nome and cpf:
        print("Nome:", nome)
        print("CPF:", cpf)
    else:
        print("Não foi possível extrair o Nome e o CPF.")
except Exception as e:
    print("Erro:", e)


