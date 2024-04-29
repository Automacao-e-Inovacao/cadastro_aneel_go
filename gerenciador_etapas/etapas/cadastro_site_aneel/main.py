import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


from static.registrar_consultar import Registers
from gerenciador_etapas.etapas.cadastro_site_aneel.static_site_aneel import StaticSiteAneel

class CadastroSiteAneel:
    tabela = 'cadastro_aneel_go.nota'

    def __init__(self, logger_nota: logging.Logger, inst_register: Registers, inst_static_site_aneel: StaticSiteAneel) -> None:
        self.logger_nota = logger_nota
        self.conexao_datamart = inst_register
        self.static_site_aneel = inst_static_site_aneel
        self.driver = None  # Inicializa o driver como None para ser atribuído posteriormente
        self.usuario_aneel = 'gd.goias@equatorialenergia.com.br'
        self.senha_aneel = 'EQTL01'
        self.empresa_abreviado = 'GO'
        
    def open_browser(self):
        # Define as opções do Chrome
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # Execute o navegador em modo headless (sem interface gráfica)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Inicializa o driver do Chrome
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(60)  # Define um tempo de espera implícito de 60 segundos
    
    def consultar_notas(self, sql_consulta):
        lista_de_notas = self.conexao_datamart.consultar_notas(sql=sql_consulta)
        return lista_de_notas

    def retornar_a_tela_de_busca(self) -> None:
        try:
            self.driver.get('http://www2.aneel.gov.br/scg/gd/login.asp')
        except:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(60)
            self.driver.get('http://www2.aneel.gov.br/scg/gd/login.asp')
        titulo_da_pagina = self.driver.current_url
        if 'login' in titulo_da_pagina:
            self.static_site_aneel.login(self.driver, self.usuario_aneel, self.senha_aneel)
        else:
            self.logger_nota.error(f'Titulo da página é diferente de login :|: {titulo_da_pagina}')

        titulo_da_pagina = self.driver.current_url
        if 'links' in titulo_da_pagina:
            lista_de_elementos_botao = self.driver.find_elements(by=By.NAME, value='botao')
            for elemento in lista_de_elementos_botao:
                titulo_do_elemento = elemento.get_attribute('title')
                if titulo_do_elemento == 'Ver, alterar, incluir fonte ou excluir UC com GD cadastradas':
                    elemento.click()
                    break
            else:
                self.logger_nota.error(f'Não foi possível encontrar o elemento com o nome "Ver, alterar, incluir '
                                           f'fonte ou excluir UC com GD cadastradas" na tela de menu ')
        else:
            self.logger_nota.error(f'Titulo da página é diferente de links :|: {titulo_da_pagina}')

    def tratamento_dos_dados_da_tupla(self, tupla):
        tupla['data_solicitacao_conexao_gd'] = '{:02d}/{:02d}/{:04d}'.format(tupla['data_solicitacao_conexao_gd'].day,
                                                                             tupla['data_solicitacao_conexao_gd'].month,
                                                                             tupla['data_solicitacao_conexao_gd'].year)
        tupla['data_aprov_p_conexao'] = '{:02d}/{:02d}/{:04d}'.format(tupla['data_aprov_p_conexao'].day,
                                                                      tupla['data_aprov_p_conexao'].month,
                                                                      tupla['data_aprov_p_conexao'].year)
        tupla['endereco_da_uc'] = f"{tupla['endereco']}, {tupla['numero']} / {tupla['bairro']}"
        tupla['municipio'] = f"{tupla['municipio']} / {self.empresa_abreviado}"

        latitude = tupla['grau_latitude']

        latitude = latitude.replace(' ', '')
        split_1 = latitude.split('°')
        if '-' in split_1[0]:
            latitude_grau = '-' + ''.join(filter(str.isdigit, split_1[0]))
        else:
            latitude_grau = ''.join(filter(str.isdigit, split_1[0]))
        split_2 = split_1[1].split('"')
        latitude_minuto = ''.join(filter(str.isdigit, split_2[0]))
        latitude_segundo = split_2[1].replace('"', '')
        if '.' in latitude_segundo:
            split_3 = latitude_segundo.split('.')
            latitude_segundo = ''.join(filter(str.isdigit, split_3[0])) + '.' + ''.join(filter(str.isdigit, split_3[1]))
        else:
            latitude_segundo = ''.join(filter(str.isdigit, latitude_segundo))

        tupla['latitude_segundo'] = latitude_segundo
        tupla['latitude_minuto'] = latitude_minuto
        tupla['latitude_grau'] = latitude_grau

        try:
            del split_1
        except:
            pass
        try:
            del split_2
        except:
            pass
        try:
            del latitude
        except:
            pass
        try:
            del split_3
        except:
            pass

        longitude = tupla['grau_longitude']

        longitude = longitude.replace(' ', '')
        split_1 = longitude.split('°')
        if '-' in split_1[0]:
            longitude_grau = '-' + ''.join(filter(str.isdigit, split_1[0]))
        else:
            longitude_grau = ''.join(filter(str.isdigit, split_1[0]))
        split_2 = split_1[1].split('"')
        longitude_minuto = ''.join(filter(str.isdigit, split_2[0]))
        longitude_segundo = split_2[1].replace('"', '')
        if '.' in longitude_segundo:
            split_3 = longitude_segundo.split('.')
            longitude_segundo = ''.join(filter(str.isdigit, split_3[0])) + '.' + ''.join(
                filter(str.isdigit, split_3[1]))
        else:
            longitude_segundo = ''.join(filter(str.isdigit, longitude_segundo))

        tupla['longitude_segundo'] = longitude_segundo
        tupla['longitude_minuto'] = longitude_minuto
        tupla['longitude_grau'] = longitude_grau

    def tratamento_da_nota(self, tupla_notas: dict):
        self.tratamento_dos_dados_da_tupla(tupla=tupla_notas)
        self.retornar_a_tela_de_busca()

        titulo_da_pagina = self.driver.current_url
        if 'adm_empreendimento' not in titulo_da_pagina:
            raise AssertionError(
                f'Página não contem a string adm_empreendimento, como era esperado: {titulo_da_pagina}')

        resultado_funcao = self.static_site_aneel.consultar_registro(self.driver, tupla_notas['instalacao'])
        if 'Incompleta' not in resultado_funcao and not resultado_funcao == 'Não cadastrado':
            split_4 = resultado_funcao.split(' ')
            resultado_funcao = split_4[len(split_4) - 3]
            self.logger_nota.critical(
                f'Status do registro na ANEEL é diferente do padrão :|: {resultado_funcao}'
            )
            raise AssertionError('')

        if resultado_funcao == 'Não cadastrado':
            titulo_da_pagina = self.driver.current_url
            if 'links' in titulo_da_pagina:
                lista_de_elementos_botao = self.driver.find_elements(by=By.NAME, value='botao')
                for elemento in lista_de_elementos_botao:
                    titulo_do_elemento = elemento.get_attribute('title')
                    if titulo_do_elemento == 'Cadastrar nova UC com GD (Unidades Consumidoras com Geração ' \
                                             'Distribuída)':
                        elemento.click()
                        break
            else:
                raise AssertionError(
                    f'Página não contem a string links, como era esperado: {titulo_da_pagina}'
                )

            # %%
            titulo_da_pagina = self.driver.current_url
            if 'Inclui_Usina' in titulo_da_pagina:
                if tupla_notas['cpf'] is None and tupla_notas['cnpj'] is None:
                    raise AssertionError('cpf e cnpj é vazio')
                elif tupla_notas['cnpj'] is None:
                    cpf_cnpj = tupla_notas['cpf']
                else:
                    cpf_cnpj = tupla_notas['cnpj']

                telefone = tupla_notas['tel_movel'] + ';' + tupla_notas['tel_fixo']
                telefone = [var for var in telefone.split(';')]
                telefone.sort()

                if telefone[0] == '':
                    if telefone[1] != '':
                        telefone[0] = str(telefone[1])
                    else:
                        telefone[0] = '99999999999'

                email = [var for var in tupla_notas['email'].split(';')]

                self.static_site_aneel.formulario_cadastro(self.driver, tupla_notas['municipio'],
                                    tupla_notas['instalacao'],
                                    tupla_notas['qtd_gd'], tupla_notas['endereco_da_uc'],
                                    tupla_notas['cep'],
                                    email[0], tupla_notas['nome_cliente'], cpf_cnpj,
                                    telefone[0], tupla_notas['modalidade'],
                                    tupla_notas['longitude_segundo'],
                                    tupla_notas['latitude_segundo'],
                                    tupla_notas['gru_tar'], tupla_notas['tipo_fonte'],
                                    tupla_notas['latitude_grau'], tupla_notas['longitude_grau'],
                                    tupla_notas['classe_consumo'], tupla_notas['longitude_minuto'],
                                    tupla_notas['latitude_minuto'], self.logger_nota)
            else:
                raise AssertionError(
                    f'Página não contem a string Inclui_Usina (tela de cadasto ), como era esperado: {titulo_da_pagina}'
                )
        time.sleep(5)
        try:
            titulo_da_pagina = self.driver.current_url
        except:
            texto_alert = self.driver.switch_to.alert.text
            self.driver.switch_to.alert.accept()
            self.logger_nota.critical(f'Erro com o alerta :|: {texto_alert}')
            raise AssertionError('')

        if 'Inclui_Dados' in titulo_da_pagina:
            self.static_site_aneel.formulario_tecnico(self.driver, tupla_notas['pot_modulos_kwp'], tupla_notas['quantidade_modulos'],
                               tupla_notas['pot_inversor_kw'], tupla_notas['qtde_inversores'],
                               tupla_notas['area_arranjos'], tupla_notas['fabricante_modulos'],
                               tupla_notas['modelo_modulo'], tupla_notas['fab_inversor'],
                               tupla_notas['modelo_inversor'], tupla_notas['data_aprov_p_conexao'],
                               tupla_notas['data_solicitacao_conexao_gd'], self.logger_nota)
        elif 'Inclui_Usina' in titulo_da_pagina:
            msg_erro = self.driver.find_element(by=By.CLASS_NAME, value='mensagemErro').text
            self.logger_nota.critical(f'Erro no formulário de cadastro :|: {msg_erro}')
            raise AssertionError('')
        else:
            raise AssertionError(f'Página não contem a string Inclui_Dados, como era esperado: {titulo_da_pagina}')

        time.sleep(5)
        try:
            titulo_da_pagina = self.driver.current_url
        except:
            texto_alert = self.driver.switch_to.alert.text
            self.driver.switch_to.alert.accept()
            self.logger_nota.critical(f'Erro com o alerta :|: {texto_alert}')
            raise AssertionError('')
        if 'Inclui_CEGanterior' in titulo_da_pagina:
            self.static_site_aneel.tel_dados_usina(self.driver)
        else:
            raise AssertionError(
                f'Página não contem a string Inclui_CEGanterior, como era esperado: {titulo_da_pagina}')

        # Tela Conclusão do cadastro

        titulo_da_pagina = self.driver.current_url
        if 'Conclusao' in titulo_da_pagina:
            return self.static_site_aneel.tela_para_obtencao_codigo_gd(self.driver, empresa_abreviado=self.empresa_abreviado)
        else:
            raise AssertionError(
                f'Página não contem a string Inclui_CEGanterior, como era esperado: {titulo_da_pagina}')

    def run(self, id_nota):
        sql_consulta = f""" select *
        from {self.__class__.tabela}
        where id = {id_nota} """
        lista_notas = self.consultar_notas(sql_consulta=sql_consulta)
        if len(lista_notas) == 1:
            tupla_notas = lista_notas[0]
            
            codigo_gd_final = self.tratamento_da_nota(tupla_notas)
            if codigo_gd_final is not None and ''.join(filter(str.isalnum, codigo_gd_final)) != '':
                self.conexao_datamart.atualizar_registro(
                    id_=id_nota, dicionario={'num_cadastro_gd': codigo_gd_final},
                    tabela=self.__class__.tabela
                )
            else:
                raise AssertionError('Houve um erro ao receber o código gd final da função tratamento da nota')
        else:
            raise AssertionError(f'Não consegui achar a nota pelo id_nota, ou a nota está duplicada na tabela :|: {len(lista_notas)}')

    def verificar_cadastro(self, id_nota):
        sql_consulta_uc = f'''
            SELECT id, uc FROM cadastro_aneel_go.nota
            where id = {id_nota}
            '''
        uc = self.conexao_datamart.consultar_notas(sql=sql_consulta_uc)
        try:
            self.driver.get('http://www2.aneel.gov.br/scg/gd/login.asp')
        except:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(60)
            self.driver.get('http://www2.aneel.gov.br/scg/gd/login.asp')
        self.static_site_aneel.login(self.driver, self.usuario_aneel, self.senha_aneel)
        
        for tupla in uc:
            id_, uc = tupla  # Desempacotando a tupla
            self.static_site_aneel.consultar_registro(self.driver, codigo_gd=None, uc=uc)  # Passando o uc corretamente
