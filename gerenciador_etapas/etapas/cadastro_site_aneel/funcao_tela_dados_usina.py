# %% [markdown]
# Importando bibliotecas

# %%
from selenium.webdriver.common.by import By


# %%
def tel_dados_usina(driver):
    driver.find_element(by=By.NAME, value='ENVIAR').click()
