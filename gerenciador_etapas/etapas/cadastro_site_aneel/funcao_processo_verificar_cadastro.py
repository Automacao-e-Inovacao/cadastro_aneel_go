from selenium.webdriver.common.by import By

# Login
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
        if 'ENTRAR' in elemento.accessible_name.upper():
            elemento.click()
            break

# Consultar registros
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
