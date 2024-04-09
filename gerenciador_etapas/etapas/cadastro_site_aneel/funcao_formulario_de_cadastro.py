# Importando bibliotecas
from re import sub
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import unidecode

# Preencher formulário
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

    elemento = driver.find_element(by=By.NAME, value='MdaSegundoLatitude')
    elemento.clear()

    try:
        latitude_segundo = float(latitude_segundo)
    except:
        raise AssertionError('latitude diferente de float')
    if latitude_segundo > 59.480:
        latitude_segundo = 59.480

    latitude_segundo = str(latitude_segundo)
    split_prov = latitude_segundo.split('.')
    latitude_segundo = '{}.{}'.format(split_prov[0], split_prov[1][:2])

    valor_latitude_segundo_int = int(split_prov[0])
    for numero_por_numero in latitude_segundo:
        elemento.send_keys(numero_por_numero)
        valor_elemento = elemento.get_attribute('value')
        valor_elemento = str(valor_elemento)
        valor_elemento = valor_elemento.replace('.', ',')
        if ',' in valor_elemento:
            split_1 = valor_elemento.split(',')
            valor_elemento_int = int(split_1[0])
            if valor_latitude_segundo_int == valor_elemento_int:
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
    while not valor_latitude_segundo_int == valor_elemento_int:
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
    del elemento

    elemento = driver.find_element(by=By.NAME, value='MdaSegundoLongitude')
    elemento.clear()

    try:
        longitude_segundo = float(longitude_segundo)
    except:
        logger.critical('longitude diferente de float')
        raise AssertionError('')
    if longitude_segundo > 59.480:
        longitude_segundo = 59.480

    longitude_segundo = str(longitude_segundo)
    split_prov = longitude_segundo.split('.')
    longitude_segundo = '{}.{}'.format(split_prov[0], split_prov[1][:2])

    valor_longitude_segundo_int = int(split_prov[0])
    for numero_por_numero in longitude_segundo:
        elemento.send_keys(numero_por_numero)
        valor_elemento = elemento.get_attribute('value')
        valor_elemento = str(valor_elemento)
        valor_elemento = valor_elemento.replace('.', ',')
        if ',' in valor_elemento:
            split_1 = valor_elemento.split(',')
            valor_elemento_int = int(split_1[0])
            if valor_longitude_segundo_int == valor_elemento_int:
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
    while not valor_longitude_segundo_int == valor_elemento_int:
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
    # municipio_da_uc_com_estado = municipio_da_uc_com_estado.replace(' ', '').upper()
    # municipio_da_uc_com_estado = unidecode.unidecode(municipio_da_uc_com_estado)
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
