import os
import time
from ahk import AHK
import win32com.client
from utils.utils import Utils
from repository.datamart_repository import DatamartRepository

class ReadExcelFile:
    """
    Responsável pela leitura da planilha e inclusão dos dados na tabela Fila
    """
    def __init__(self):
        self.caminho_do_arquivo = r'\\55ASPDCARQ01\55Atende\Administrativo\04 - Planejamento e Controle\SENA\automacao\cadastro_aneel_go\base_cadastro_aneel_go.xlsx'
        self.tabela = 'gerar_e_enviar.fila'

    def obter_ultima_modificacao_formatada(self):
        """
        Verifica a última modificação do arquivo e retorna a data formatada.
        """
        if os.path.exists(self.caminho_do_arquivo):
            ultima_modificacao = os.path.getmtime(self.caminho_do_arquivo)
            ultima_modificacao_formatada = time.strftime("%d/%m/%Y %H", time.localtime(ultima_modificacao))
            return ultima_modificacao_formatada
        else:
            return None

    def executar_atualizacao(self, caminho_planilha):
        """
        Executa a atualização do arquivo Excel.
        """
        caminho_autohotkey = os.path.join('venv', 'Autohotkey', 'AutoHotkey.exe')
        ahk = AHK(executable_path=caminho_autohotkey)
        xl = win32com.client.Dispatch("Excel.Application")
        xl.Visible = True
        xl.DisplayAlerts = False
        wbb = xl.Workbooks.Open(caminho_planilha)
        time.sleep(60)
        ahk.run_script('''
        winwait, base_cadastro_aneel_go
        winactivate, base_cadastro_aneel_go
        winwaitactive, base_cadastro_aneel_go
        send, ^b ; Pressiona Control + B
        ''', blocking=True)
        time.sleep(10)
        wbb.Save()
        wbb.Close()
        xl.Quit()

    def inserir_dados_no_datamart(self):
        """
        Lê o arquivo Excel e insere os dados na tabela Fila do datamart.
        """
        try:
            utils = Utils()
            df = utils.convert_excel_to_dataframe()
        except Exception as e:
            raise RuntimeError(f"Erro ao ler e converter arquivo Excel: {e}")

        try:
            datamart = DatamartRepository()
            datamart.save_dataframe_to_table(df)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir dados no datamart: {e}")
