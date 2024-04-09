# %% [markdown]
# Importando bibliotecas

# %%
from selenium.webdriver.common.by import By


# %% [markdown]
# Formulário técnico cadastro ANEEL

# %%
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
