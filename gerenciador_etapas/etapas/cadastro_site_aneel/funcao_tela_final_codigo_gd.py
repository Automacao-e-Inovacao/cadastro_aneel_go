# %% [markdown]
# Importando bibliotecas

# %%
from selenium.webdriver.common.by import By


# %%
def tela_para_obtencao_codigo_gd(driver, empresa_abreviado):
    codigo_da_pagina = driver.page_source
    indice_da_procura_string = codigo_da_pagina.find(f'GD.{empresa_abreviado}.')
    codigo_registro_gd = codigo_da_pagina[indice_da_procura_string:indice_da_procura_string + 17]
    driver.find_element(by=By.NAME, value='inicio').click()
    return codigo_registro_gd
