# Importando bibliotecas
from re import sub
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import unidecode

class StaticSiteAneel:
    def __init__(self):
        pass
    
    @staticmethod
    def login(driver, usuario_aneel, senha_aneel):
        """
        Realiza o login na página utilizando o usuário e senha fornecidos.

        Args:
            driver: Uma instância do driver Selenium.
            usuario_aneel (str): O nome de usuário da ANEEL.
            senha_aneel (str): A senha da ANEEL.

        Returns:
            None
        """
        driver.find_element(by=By.NAME, value='login').send_keys(usuario_aneel)
        driver.find_element(by=By.NAME, value='Senha').send_keys(senha_aneel)

        lista_de_elementos_botao = driver.find_elements(by=By.NAME, value='botao')
        for elemento in lista_de_elementos_botao:
            if 'ENTRAR' in elemento.get_attribute('accessible_name').upper():
                elemento.click()
                break

    @staticmethod
    def consultar_registro(driver, uc, tabela_encontrada=False):
        """
        Consulta um registro com base no número da Unidade Consumidora (UC).

        Args:
            driver: Uma instância do driver Selenium.
            uc (str): O número da Unidade Consumidora a ser consultado.
            tabela_encontrada (bool): Indica se a tabela foi encontrada.

        Returns:
            str: O resultado da consulta.
        """
        elemento = driver.find_element(by=By.NAME, value='CodUnidadeConsumidora')
        elemento.clear()
        elemento.send_keys(uc)

        driver.find_element(by=By.NAME, value='BUSCAR').click()

        lista_elementos = []
        while len(lista_elementos) < 3:
            lista_elementos = driver.find_elements(by=By.CLASS_NAME, value='tabelaMaior')

        for elemento in lista_elementos:
            try:
                texto_do_elemento = elemento.text
            except:
                continue
            if 'Nenhuma Unidade Consumidora localizada' in texto_do_elemento:
                tabela_encontrada = True
                break

        if tabela_encontrada:
            driver.find_element(by=By.NAME, value='inicio').click()
            return 'Não cadastrado'
        else:
            tabela_encontrada = False
            for elemento in lista_elementos:
                try:
                    texto_do_elemento = elemento.text
                except:
                    continue
                if 'UNIDADES CONSUMIDORAS COM GERAÇÃO DISTRIBUÍDA' in texto_do_elemento:
                    tabela_encontrada = True
                    break

            if tabela_encontrada:
                if 'Incompleta' in texto_do_elemento:
                    driver.find_element(by=By.CLASS_NAME, value='botaoEditar').click()
                    driver.find_element(by=By.NAME, value='PROXIMO').click()
                    return 'Incompleta'
                else:
                    driver.find_element(by=By.NAME, value='inicio').click()
                    return texto_do_elemento
            else:
                driver.find_element(by=By.NAME, value='inicio').click()
                return 'Tabela não encontrada, valor booleano = ' + tabela_encontrada

    # Preencher formulário
    @staticmethod
    def formulario_cadastro(driver, municipio_da_uc_com_estado, uc, qtd_gd, endereco_da_uc, cep, email, nome_do_titular,
                            cpf_cnpj, telefone, modalidade, longitude_segundo, latitude_segundo, subgrupo, fonte,
                            latitude_grau, longitude_grau, classe, longitude_minuto, latitude_minuto, logger):
        if 'GOVERNADOR EDSON LOBAO' in municipio_da_uc_com_estado:
            municipio_da_uc_com_estado = 'GOVERNADOR EDISON LOBAO / MA'
        municipio_da_uc = municipio_da_uc_com_estado.split('/')[0]
        try:
            driver.find_element(by=By.ID, value='NomeBusca1').send_keys(municipio_da_uc[:10])
            driver.find_element(by=By.ID, value='NomeBusca2').send_keys(municipio_da_uc[:10])
        except:
            driver.find_element(by=By.ID, value='NomeBusca1').send_keys(municipio_da_uc)
            driver.find_element(by=By.ID, value='NomeBusca2').send_keys(municipio_da_uc)
        driver.find_element(by=By.NAME, value='DscEndereco').send_keys(endereco_da_uc)
        driver.find_element(by=By.NAME, value='DscEndePessoaTitular').send_keys(endereco_da_uc)
        driver.find_element(by=By.NAME, value='NumCEP').send_keys(cep)
        driver.find_element(by=By.NAME, value='NumCEPPessoaTitular').send_keys(cep)

        driver.find_element(by=By.NAME, value='CodUnidadeConsumidora').send_keys(uc)
        elemento = driver.find_element(by=By.NAME, value='QtdUCComUC')
        elemento.clear()
        elemento.send_keys(qtd_gd)

        driver.find_element(by=By.NAME, value='DscEmail').send_keys(email)
        driver.find_element(by=By.NAME, value='NomPessoa').send_keys(nome_do_titular)
        driver.find_element(by=By.NAME, value='NumCPFCNPJ').send_keys(cpf_cnpj)
        driver.find_element(by=By.NAME, value='NumTelefone').send_keys(telefone)

        def preencher_segmento_geografico(elemento, valor_segundo, valor_int, valor_str, valor_grau):
            elemento.clear()
            try:
                valor_segundo = float(valor_segundo)
            except:
                raise AssertionError('latitude/longitude diferente de float')
            if valor_segundo > 59.480:
                valor_segundo = 59.480

            valor_segundo = str(valor_segundo)
            split_prov = valor_segundo.split('.')
            valor_segundo = '{}.{}'.format(split_prov[0], split_prov[1][:2])

            valor_int = int(split_prov[0])
            for numero_por_numero in valor_segundo:
                elemento.send_keys(numero_por_numero)
                valor_elemento = elemento.get_attribute('value')
                valor_elemento = str(valor_elemento)
                valor_elemento = valor_elemento.replace('.', ',')
                if ',' in valor_elemento:
                    split_1 = valor_elemento.split(',')
                    valor_elemento_int = int(split_1[0])
                    if valor_int == valor_elemento_int:
                        break
            tentativas = 0
            while not ',' in valor_elemento:
                elemento.send_keys(0)
                valor_elemento = elemento.get_attribute('value')
                valor_elemento = str(valor_elemento)
                valor_elemento = valor_elemento.replace('.', ',')
                tentativas += 1
                if tentativas > 20:
                    logger.critical('Numero de tentativas para preencher campo "segundo" excedido')
                    raise AssertionError('')
            split_1 = valor_elemento.split(',')
            valor_elemento_int = int(split_1[0])
            tentativas = 0
            while not valor_int == valor_elemento_int:
                elemento.send_keys(0)
                valor_elemento = elemento.get_attribute('value')
                valor_elemento = str(valor_elemento)
                valor_elemento = valor_elemento.replace('.', ',')
                split_1 = valor_elemento.split(',')
                valor_elemento_int = int(split_1[0])
                tentativas += 1
                if tentativas > 20:
                    logger.critical('Numero de tentativas para preencher campo "segundo" excedido')
                    raise AssertionError('')
            return valor_elemento

        preencher_segmento_geografico(driver.find_element(by=By.NAME, value='MdaSegundoLatitude'), 
                                    latitude_segundo, int(latitude_segundo.split('.')[0]), latitude_segundo, latitude_grau)

        preencher_segmento_geografico(driver.find_element(by=By.NAME, value='MdaSegundoLongitude'), 
                                    longitude_segundo, int(longitude_segundo.split('.')[0]), longitude_segundo, longitude_grau)

        select = Select(driver.find_element(by=By.NAME, value='MdaGrauLatitude'))
        select.select_by_visible_text(latitude_grau)
        select = Select(driver.find_element(by=By.NAME, value='MdaGrauLongitude'))
        select.select_by_visible_text(longitude_grau)
        select = Select(driver.find_element(by=By.NAME, value='MdaMinutoLatitude'))
        select.select_by_visible_text(latitude_minuto)
        select = Select(driver.find_element(by=By.NAME, value='MdaMinutoLongitude'))
        select.select_by_visible_text(longitude_minuto)

        select = Select(driver.find_element(by=By.ID, value='IdcModalidade'))
        select.select_by_visible_text(modalidade)
        select = Select(driver.find_element(by=By.NAME, value='IdeGrupoFornecimento'))
        lista_opcoes_campo = select.options
        for opcao in lista_opcoes_campo:
            elemento = opcao.text
            _elemento = elemento[:2]
            _subgrupo = subgrupo[:2]
            if _elemento == _subgrupo:
                select.select_by_visible_text(elemento)
                break
        select = Select(driver.find_element(by=By.NAME, value='IdeCombustivel'))
        select.select_by_visible_text(fonte)
        select = Select(driver.find_element(by=By.NAME, value='IdeClasseFornecimento'))
        select.select_by_visible_text(classe)

        time.sleep(1)
        tentativas = 0
        driver.implicitly_wait(10)
        while True:
            try:
                elemento = driver.find_element(by=By.ID, value='IdSelecionado1')
                break
            except:
                driver.find_element(by=By.ID, value='NomeBusca1').clear()
                try:
                    driver.find_element(by=By.ID, value='NomeBusca1').send_keys(municipio_da_uc[:10])
                except:
                    driver.find_element(by=By.ID, value='NomeBusca1').send_keys(municipio_da_uc)
            tentativas += 1
            if tentativas > 10:
                raise AssertionError('Não foi possível encontrar o elemento de seleção de município')
        driver.implicitly_wait(60)
        select = Select(elemento)
        lista_select = []
        while len(lista_select) < 1:
            try:
                lista_select = select.options
            except:
                del elemento, select, lista_select
                elemento = driver.find_element(by=By.ID, value='IdSelecionado1')
                select = Select(elemento)
                lista_select = []

        source_elemento = elemento.get_attribute('outerHTML')
        source_elemento = source_elemento.replace(' ', '')
        source_elemento = unidecode.unidecode(source_elemento)
        source_elemento = source_elemento.upper()
        municipio_da_uc_com_estado = municipio_da_uc_com_estado.replace(' ', '').upper()
        municipio_da_uc_com_estado = unidecode.unidecode(municipio_da_uc_com_estado)
        index_search = source_elemento.find(municipio_da_uc_com_estado)
        time.sleep(3)

        if index_search < 1:
            raise AssertionError('Municipio nao encontrado')
        value_elemento = ''
        count_value_elemento = 12
        while not 'OPTIONVALUE' in value_elemento:
            value_elemento = source_elemento[index_search - count_value_elemento:index_search]
            count_value_elemento += 2
        value_elemento = sub('[^0-9]', '', value_elemento)
        select = Select(elemento)
        select.select_by_value(value_elemento)

        tentativas = 0
        driver.implicitly_wait(10)
        while True:
            try:
                elemento = driver.find_element(by=By.ID, value='IdSelecionado2')
                break
            except:
                driver.find_element(by=By.ID, value='NomeBusca2').clear()
                try:
                    driver.find_element(by=By.ID, value='NomeBusca2').send_keys(municipio_da_uc[:10])
                except:
                    driver.find_element(by=By.ID, value='NomeBusca2').send_keys(municipio_da_uc)
            tentativas += 1
            if tentativas > 10:
                raise AssertionError('Não foi possível encontrar o elemento de seleção de município')
        driver.implicitly_wait(60)
        select = Select(elemento)
        lista_select = []
        while len(lista_select) < 1:
            try:
                lista_select = select.options
            except:
                del elemento, select, lista_select
                elemento = driver.find_element(by=By.ID, value='IdSelecionado2')
                select = Select(elemento)
                lista_select = []

        source_elemento = elemento.get_attribute('outerHTML')
        source_elemento = source_elemento.replace(' ', '')
        source_elemento = unidecode.unidecode(source_elemento)
        source_elemento = source_elemento.upper()
        index_search = source_elemento.find(municipio_da_uc_com_estado)
        time.sleep(3)
        if index_search < 1:
            raise AssertionError('Municipio nao encontrado')
        value_elemento = ''
        count_value_elemento = 12
        while not 'OPTIONVALUE' in value_elemento:
            value_elemento = source_elemento[index_search - count_value_elemento:index_search]
            count_value_elemento += 2
        value_elemento = sub('[^0-9]', '', value_elemento)
        select = Select(elemento)
        select.select_by_value(value_elemento)

        driver.find_element(by=By.NAME, value='PROXIMO').click()

    @staticmethod
    def tel_dados_usina(driver):
        driver.find_element(by=By.NAME, value='ENVIAR').click()

    @staticmethod
    def tela_para_obtencao_codigo_gd(driver, empresa_abreviado):
        codigo_da_pagina = driver.page_source
        indice_da_procura_string = codigo_da_pagina.find(f'GD.{empresa_abreviado}.')
        codigo_registro_gd = codigo_da_pagina[indice_da_procura_string:indice_da_procura_string + 17]
        driver.find_element(by=By.NAME, value='inicio').click()
        return codigo_registro_gd

    @staticmethod
    def formulario_tecnico(driver, potencia_total_dos_modulos, qtd_de_modulos, potencia_total_dos_inversores,
                        qtd_de_inversores, area_total_dos_arranjos, fabricante_dos_modulos, modelos_dos_modulos,
                        fabricante_dos_inversores, modelos_dos_inversores, data_da_implantacao, data_da_conexao,
                        logger):
        if fabricante_dos_inversores == 'JA':
            fabricante_dos_inversores = 'JA SOLAR'
        if fabricante_dos_modulos == 'JA':
            fabricante_dos_modulos = 'JA SOLAR'
        elemento = driver.find_element(by=By.NAME, value='MdaPotenciaModulos')
        elemento.clear()
        elemento.send_keys(potencia_total_dos_modulos)
        _texto_elemento_potencial_modulos = elemento.get_attribute('value')
        _texto_elemento_potencial_modulos = _texto_elemento_potencial_modulos.replace(',', '.')
        _texto_elemento_potencial_modulos = float(_texto_elemento_potencial_modulos)
        contagem_para_sair_do_loop = 0
        while _texto_elemento_potencial_modulos != potencia_total_dos_modulos:
            elemento.send_keys(0)
            _texto_elemento_potencial_modulos = elemento.get_attribute('value')
            _texto_elemento_potencial_modulos = _texto_elemento_potencial_modulos.replace(',', '.')
            _texto_elemento_potencial_modulos = float(_texto_elemento_potencial_modulos)
            contagem_para_sair_do_loop += 1
            if contagem_para_sair_do_loop > 60:
                logger.critical('Loop infinito no potencia total de modulos')
                raise AssertionError('')

        elemento = driver.find_element(by=By.NAME, value='MdaQtdModulos')
        elemento.clear()
        elemento.send_keys(qtd_de_modulos)

        elemento = driver.find_element(by=By.NAME, value='MdaPotenciaInversores')
        elemento.clear()
        elemento.send_keys(potencia_total_dos_inversores)
        _texto_elemento_potencial_inversores = elemento.get_attribute('value')
        _texto_elemento_potencial_inversores = _texto_elemento_potencial_inversores.replace(',', '.')
        _texto_elemento_potencial_inversores = float(_texto_elemento_potencial_inversores)
        contagem_para_sair_do_loop = 0
        while _texto_elemento_potencial_inversores != potencia_total_dos_inversores:
            elemento.send_keys(0)
            _texto_elemento_potencial_inversores = elemento.get_attribute('value')
            _texto_elemento_potencial_inversores = _texto_elemento_potencial_inversores.replace(',', '.')
            _texto_elemento_potencial_inversores = float(_texto_elemento_potencial_inversores)
            contagem_para_sair_do_loop += 1
            if contagem_para_sair_do_loop > 60:
                logger.critical('Loop infinito no potencia total de modulos')
                raise AssertionError('')

        elemento = driver.find_element(by=By.NAME, value='MdaQtdInversores')

        elemento.clear()
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        elemento.send_keys(qtd_de_inversores)
        try:
            driver.switch_to.alert.accept()
        except:
            pass

        elemento = driver.find_element(by=By.NAME, value='MdaAreaArranjo')
        elemento.clear()
        try:
            driver.switch_to.alert.accept()
        except:
            pass
        elemento.send_keys(area_total_dos_arranjos)
        _texto_elemento_arranjos = elemento.get_attribute('value')
        _texto_elemento_arranjos = _texto_elemento_arranjos.replace(',', '.')
        _texto_elemento_arranjos = float(_texto_elemento_arranjos)
        area_total_dos_arranjos_str = str(area_total_dos_arranjos)
        if len(area_total_dos_arranjos_str) > 7:
            raise Exception('tamanho de area de arranjo muito grande')
        contagem_para_sair_do_loop = 0
        while _texto_elemento_arranjos != area_total_dos_arranjos:
            elemento.send_keys(0)
            _texto_elemento_arranjos = elemento.get_attribute('value')
            _texto_elemento_arranjos = _texto_elemento_arranjos.replace(',', '.')
            _texto_elemento_arranjos = float(_texto_elemento_arranjos)
            contagem_para_sair_do_loop += 1
            if contagem_para_sair_do_loop > 60:
                logger.critical('Loop infinito no potencia total de modulos')
                raise AssertionError('')

        driver.find_element(by=By.NAME, value='NomFabricanteModulo').send_keys(fabricante_dos_modulos)
        driver.find_element(by=By.NAME, value='NomModeloModulo').send_keys(modelos_dos_modulos)
        driver.find_element(by=By.NAME, value='NomFabricanteInversor').send_keys(fabricante_dos_inversores)
        driver.find_element(by=By.NAME, value='NomModeloInversor').send_keys(modelos_dos_inversores)
        driver.find_element(by=By.NAME, value='DatImplantacaoUsina').send_keys(data_da_conexao)
        driver.find_element(by=By.NAME, value='DatConexao').send_keys(data_da_implantacao)
        driver.find_element(by=By.NAME, value='ENVIAR').click()














