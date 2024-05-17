import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from static.registrar_consultar import Registers

class ExtracoesDadosSicap:
    tabela = 'cadastro_aneel_go.nota'

    def __init__(self, logger_nota: logging.Logger, inst_register: Registers) -> None:
        self.logger_nota = logger_nota
        self.conexao_datamart = inst_register

    def open_browser(self):
        # Define as opções do Chrome
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # Execute o navegador em modo headless (sem interface gráfica)
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        # Inicializa o driver do Chrome
        navegador = webdriver.Chrome(options=chrome_options)
        navegador.maximize_window()
        navegador.implicitly_wait(60)  # Define um tempo de espera implícito de 60 segundos
        
        navegador.get('http://sistemassatelites.equatorial.corp:8080/Sicap-adm/')
        
        return navegador

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

    def click_if_found(self, element_click, navegador, max_attempts=10): 
        try_order = [By.XPATH, By.ID, By.CLASS_NAME, By.TAG_NAME, By.CSS_SELECTOR]
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
        return False  

    def login(self, navegador):
        element_user = '//*[@id="input_username"]'
        element_pwrd = '//*[@id="input_password"]'
        usuario_sicap = 'u5512983'
        senha_sicap = 'Ft$85Gb13:<f>@#$'
        try:
            # Botão Login, antes de inserir o usuário/senha
            element_login = navegador.find_element(by=By.XPATH, value='//*[@class="btn btn-default"]')
            element_login.click()
            
            # Preencher usuário
            self.write_if_found(navegador, element_user, usuario_sicap)

            # Preencher senha e pressionar Enter
            password = navegador.find_element(by=By.XPATH, value=element_pwrd)
            password.click()
            password.clear()
            password.send_keys(senha_sicap, Keys.ENTER)
        except:
            pass

    def click_lupa(self, navegador):
        clicar_lupa = '//*[@class="btn btn-default"]'
        id_elemento = 'templateForm_dropMenuExample_inner'
        try:
            elemento = navegador.find_element(By.ID, id_elemento)
            texto = elemento.text
            if texto:
                try:
                    element_to_click = navegador.find_element(By.XPATH, clicar_lupa)
                    element_to_click.click()
                except:
                    pass
            else:
                print("Não foi possível ler o texto do elemento.")
        except Exception as e:
            print(f"Erro ao ler texto do elemento com ID {id_elemento}: {str(e)}")

    def find_ss(self, navegador, ss_do_parecer):
        try:
            navegador.find_element(by=By.XPATH, value = '//*[@id="novasEntradas:interessadoFilter"]').send_keys(ss_do_parecer)
            # Encontrar o botão "Consultar" pelo texto
            botao_consultar = navegador.find_element(By.XPATH, "//div[@class='modal-footer']//button[contains(text(),'Consultar')]")
            botao_consultar.click()
        except Exception as e:
            print(f"Erro ao clicar no botão 'Consultar': {str(e)}")

    def click_projeto(self, navegador):
        classe = 'panel-title-link'
        
        try:
            # Encontrar o elemento pelo nome da classe
            elemento = navegador.find_element(By.CLASS_NAME, classe)
            
            # Verificar se a classe do elemento é 'panel-title-link collapsed'
            if 'collapsed' in elemento.get_attribute('class'):
                # Clicar no elemento
                elemento.click()
            else:
                print(f"Elemento com classe '{classe}' não está no estado 'collapsed'.")
        except Exception as e:
            print(f"Erro ao clicar no elemento com classe '{classe}': {str(e)}")

    def click_lupinha(self, navegador):
        xpath_tabela = '//*[@class="table table-bordered table-striped table-hover novasEntradasj_idt164Table dataTable no-footer"]'
        try:
            tabela = navegador.find_element(By.XPATH, xpath_tabela)
            linhas = tabela.find_elements(By.XPATH, "./tbody/tr")
            
            for linha in linhas:
                colunas = linha.find_elements(By.XPATH, "./td")
                ultimo_td = colunas[-1]
                link = ultimo_td.find_element(By.XPATH, ".//a[starts-with(@href, '/Sicap-adm/projeto')]")
                link.click()
                
        except Exception as e:
            print(f"Erro ao clicar ou ler o último <td> da tabela: {str(e)}")

    def click_dados_de_projeto(self, navegador):
        xpath_detalhes = '//*[@class="panel-title-link  collapsed"]'
        texto_alvo = 'Dados de Projeto'
        try:
            elementos = navegador.find_elements(By.XPATH, xpath_detalhes)

            for elemento in elementos:
                if texto_alvo in elemento.text:
                    elemento.click()
                    break
            else:
                print(f"Não foi encontrado nenhum elemento com o texto '{texto_alvo}'.")
                
        except Exception as e:
            print(f"Erro ao clicar no elemento com o texto '{texto_alvo}': {str(e)}")

    def tipo_de_fonte_da_geracao(self, navegador):
        xpath_tipo_de_geracao = '//*[@id="dadosProjetoForm:selectTipoGeracaoInner"]'
        try:
            # Encontrar o elemento pelo XPath fornecido
            elemento = navegador.find_element(By.XPATH, xpath_tipo_de_geracao)

            # Obter o texto do elemento
            fonte_da_geracao = elemento.text
            
            if 'Solar' in fonte_da_geracao:
                fonte_da_geracao = 'UFV - Solar - Radiação solar'
            
            return {'tipo_fonte': fonte_da_geracao}
            
        except Exception as e:
            print(f"Erro ao obter texto do elemento pelo XPath: {str(e)}")
            return None

    def find_latitude(self, navegador):
        elemento_latitude = navegador.find_element(By.XPATH, "//div[text()='Latitude']")
        
        graus_latitude = elemento_latitude.find_elements(By.XPATH, "//label[text()='Graus']")[0]
        elemento_minutos = elemento_latitude.find_elements(By.XPATH, "//label[text()='Minutos']")[0]
        elemento_segundos = elemento_latitude.find_elements(By.XPATH, "//label[text()='Segundos']")[0]
        
        # Encontre o elemento input dentro do elemento label
        input_graus_latitude = graus_latitude.find_element(By.XPATH, "./following-sibling::input")
        input_segundos_latitude = elemento_minutos.find_element(By.XPATH, "./following-sibling::input")
        input_minutos_latitude = elemento_segundos.find_element(By.XPATH, "./following-sibling::input")

        # Obtenha o valor do atributo value do elemento input
        graus_value = input_graus_latitude.get_attribute("value")
        segundos_value = input_segundos_latitude.get_attribute("value")
        minutos_value = input_minutos_latitude.get_attribute("value")

        # Ajustar o valor dos minutos
        minutos_value = minutos_value.replace(",", ".").replace("_", "") + "00"

        # Construir a representação final da latitude com o sinal de menos
        latitude_formatada = f"""-{graus_value}°{segundos_value}"{minutos_value}"""

        return {'grau_latitude': latitude_formatada}

    def find_longitude(self, navegador):
        elemento_longitude = navegador.find_element(By.XPATH, "//div[text()='Longitude']")
        
        graus_longitude = elemento_longitude.find_elements(By.XPATH, "//label[text()='Graus']")[1]
        elemento_minutos = elemento_longitude.find_elements(By.XPATH, "//label[text()='Minutos']")[1]
        elemento_segundos = elemento_longitude.find_elements(By.XPATH, "//label[text()='Segundos']")[1]
        
        # Encontre o elemento input dentro do elemento label
        input_graus_longitude = graus_longitude.find_element(By.XPATH, "./following-sibling::input")
        input_segundos_longitude = elemento_minutos.find_element(By.XPATH, "./following-sibling::input")
        input_minutos_longitude = elemento_segundos.find_element(By.XPATH, "./following-sibling::input")

        # Obtenha o valor do atributo value do elemento input
        graus_value = input_graus_longitude.get_attribute("value")
        segundos_value = input_segundos_longitude.get_attribute("value")
        minutos_value = input_minutos_longitude.get_attribute("value")

        # Ajustar o valor dos minutos
        minutos_value = minutos_value.replace(",", ".").replace("_", "") + "00"

        # Construir a representação final da longitude
        longitude_formatada = f"""-{graus_value}°{segundos_value}"{minutos_value}"""

        return {'grau_longitude': longitude_formatada}

    def find_arranjos(self, navegador):
        elemento_arranjo = navegador.find_element(By.ID, "dadosProjetoForm:areaArranjos_input")
        arranjo_value = elemento_arranjo.get_attribute("value")
        
        # Substitui vírgulas por pontos no valor numérico
        arranjo_value = arranjo_value.replace(',', '.')

        return {'area_arranjo': arranjo_value}

    def extract_value_modulos(self, navegador, texto_base):
        # Função que faz a extração dos dados de quandidade de modulos e inversores e a potência dos mesmos
        tabela_modulos = 'dadosProjetoForm:totalizadorModulos'
        elemento = navegador.find_element(by=By.ID, value=tabela_modulos)
        texto_tabela = elemento.text
        texto_tabela = texto_tabela.replace('\n', ' ')
        
        # Encontrar a posição do texto_base na string
        posicao_base = texto_tabela.find(texto_base)
        
        # Se o texto_base for encontrado
        if posicao_base != -1:
            # Pegar o texto após o texto_base
            texto_apos = texto_tabela[posicao_base + len(texto_base):].strip()
            
            # Encontrar o primeiro espaço em branco após o texto
            posicao_espaco = texto_apos.find(" ")
            
            # Se não houver espaço em branco após o texto
            if posicao_espaco == -1:
                # Retornar o valor completo após o texto_base
                valor = texto_apos
            else:
                # Extrair o valor até o espaço em branco
                valor = texto_apos[:posicao_espaco]
                
            valor = ''.join(caractere for caractere in valor if not caractere.isalpha())
            
            return valor
        else:
            return None

    def find_quantidade_de_modulos(self, navegador):
        texto_base = "Quantidade Total de Módulos"
        quantidade_de_modulos = self.extract_value_modulos(navegador, texto_base)
        if quantidade_de_modulos is not None:
            
            quantidade_de_modulos = float(quantidade_de_modulos.replace(',', '.'))
            quantidade_de_modulos = int(quantidade_de_modulos)

            return {'quantidade_modulos': quantidade_de_modulos}  
        else:
            print(f"Texto não encontrado na string.")
            
    def find_potencia_total_dos_modulos(self, navegador):
        texto_base = "Potência Total dos Módulos (KW):"
        pot_modulos_kwp = self.extract_value_modulos(navegador, texto_base)
        if pot_modulos_kwp is not None:
            
            pot_modulos_kwp = pot_modulos_kwp.replace(',', '.')

            return {'pot_modulos_kwp': pot_modulos_kwp}  
        else:
            print(f"Texto não encontrado na string.")

    def find_fabricante_modulos(self, navegador):
        fabricantes = []
        
        tabela_modulos = 'dadosProjetoForm:tabelaModuloDados_data'
        elemento = navegador.find_element(by=By.ID, value=tabela_modulos)
        texto_tabela = elemento.text
        linhas = texto_tabela.split('\n')
        
        for linha in linhas:
            palavras = linha.split()
            if palavras:
                primeira_palavra = palavras[1]
                fabricantes.append(primeira_palavra)
        
        if fabricantes:
            fabricantes_str = ' / '.join(fabricantes)
            return {'fabricante_modulos': fabricantes_str}
        else:
            return None

    def find_modelos_modulos(self, navegador):
        modelos = []
        tabela_modulos = 'dadosProjetoForm:tabelaModuloDados_data'
        elemento = navegador.find_element(by=By.ID, value=tabela_modulos)
        texto_tabela = elemento.text
        linhas = texto_tabela.split('\n')
        
        for linha in linhas:
            palavras = linha.split()
            if palavras:
                primeira_palavra = palavras[2]
                modelos.append(primeira_palavra)
        
        if modelos:
            modelos_str = ' / '.join(modelos)
            return {'modelo_modulo': modelos_str}
        else:
            return None

    def extract_value_inversores(self, navegador, texto_base):
        # Função que faz a extração dos dados de quandidade de modulos e inversores e a potência dos mesmos
        tabela_modulos = 'dadosProjetoForm:totalizadorInversores'
        elemento = navegador.find_element(by=By.ID, value=tabela_modulos)
        texto_tabela = elemento.text
        texto_tabela = texto_tabela.replace('\n', ' ')
        
        # Encontrar a posição do texto_base na string
        posicao_base = texto_tabela.find(texto_base)
        
        # Se o texto_base for encontrado
        if posicao_base != -1:
            # Pegar o texto após o texto_base
            texto_apos = texto_tabela[posicao_base + len(texto_base):].strip()
            
            # Encontrar o primeiro espaço em branco após o texto
            posicao_espaco = texto_apos.find(" ")
            
            # Se não houver espaço em branco após o texto
            if posicao_espaco == -1:
                # Retornar o valor completo após o texto_base
                valor = texto_apos
            else:
                # Extrair o valor até o espaço em branco
                valor = texto_apos[:posicao_espaco]
                
            valor = ''.join(caractere for caractere in valor if not caractere.isalpha())
            
            return valor
        else:
            return None

    def find_quantidade_de_inversores(self, navegador):
        texto_base = "Quantidade Total de Inversores:"
        quantidade_de_inversores = self.extract_value_inversores(navegador, texto_base)
        if quantidade_de_inversores is not None:

            quantidade_de_inversores = float(quantidade_de_inversores.replace(',', '.'))

            quantidade_de_inversores = int(quantidade_de_inversores)

            return {'qtde_inversores': quantidade_de_inversores}  
        else:
            print(f"Texto não encontrado na string.")
            
    def find_potencia_total_dos_inversores(self, navegador):
        texto_base = "Potência Total dos Inversores (KW):"
        pot_inversores_kwp = self.extract_value_inversores(navegador, texto_base)
        if pot_inversores_kwp is not None:

            pot_inversores_kwp = pot_inversores_kwp.replace(',', '.')

            return {'pot_inversores_kwp': pot_inversores_kwp}  
        else:
            print(f"Texto não encontrado na string.")

    def find_modelos_inversores(self, navegador):
        dados = []

        id_tabela = 'dadosProjetoForm:tabelaInversorDados_data'
        tabela = navegador.find_element(By.ID, id_tabela)
        linhas = tabela.find_elements(By.TAG_NAME, "tr")

        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if colunas:
                primeira_palavra = colunas[2].text.split()[0]  # Extrai a primeira palavra da primeira coluna
                dados.append(primeira_palavra)

        if dados:
            valores_str = ' / '.join(dados)
            return {'modelo_inversor': valores_str}
        else:
            return None

    def find_fabricante_inversores(self, navegador):
        dados = []

        id_tabela = 'dadosProjetoForm:tabelaInversorDados_data'
        tabela = navegador.find_element(By.ID, id_tabela)
        linhas = tabela.find_elements(By.TAG_NAME, "tr")

        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if colunas:
                primeira_palavra = colunas[1].text.split()[0]  # Extrai a primeira palavra da primeira coluna
                dados.append(primeira_palavra)

        if dados:
            valores_str = ' / '.join(dados)
            return {'fab_inversor': valores_str}
        else:
            return None

    def find_infos_sicap(self, navegador):
        dicionario_principal = {}
        dicionario_principal.update(self.tipo_de_fonte_da_geracao(navegador))
        dicionario_principal.update(self.find_latitude(navegador))
        dicionario_principal.update(self.find_longitude(navegador))
        dicionario_principal.update(self.find_arranjos(navegador))
        
        dicionario_principal.update(self.find_potencia_total_dos_modulos(navegador))
        dicionario_principal.update(self.find_potencia_total_dos_inversores(navegador))
        
        dicionario_principal.update(self.find_quantidade_de_modulos(navegador))
        dicionario_principal.update(self.find_quantidade_de_inversores(navegador))
        
        dicionario_principal.update(self.find_fabricante_modulos(navegador))
        dicionario_principal.update(self.find_fabricante_inversores(navegador))
        
        dicionario_principal.update(self.find_modelos_modulos(navegador))
        dicionario_principal.update(self.find_modelos_inversores(navegador))
        
        return dicionario_principal
    
    def scraping(self, ss_do_parecer):
        navegador = self.open_browser()
    
        self.login(navegador)
        self.click_lupa(navegador)
        self.find_ss(navegador, ss_do_parecer)
        self.click_projeto(navegador)
        self.click_lupinha(navegador)
        self.click_dados_de_projeto(navegador)
        # time.sleep(2)
        dicionario_principal = self.find_infos_sicap(navegador)

        navegador.quit()
        
        return dicionario_principal
    
    def execucao(self, id_nota):
        sql_consulta_uc = f'''
            SELECT id, uc, ss_do_parecer FROM cadastro_aneel_go.nota
            WHERE id = {id_nota}
            '''
            
        tupla_uc = self.conexao_datamart.consultar_notas(sql=sql_consulta_uc)
        ss_do_parecer = tupla_uc[0]['ss_do_parecer']
        
        dicionario_principal = self.scraping(ss_do_parecer=ss_do_parecer)
        print(dicionario_principal)
        self.conexao_datamart.atualizar_registro(dicionario=dicionario_principal, tabela='cadastro_aneel_go.nota', id_=id_nota)
        
           