"""
    Script principal

    Este script é responsável por iniciar e executar uma automação RPA (Robotic Process Automation), registrando informações relevantes no banco de dados.

    Módulos Importados:
        - Rpa
        - HandleLog
        - DatamartRepository

    Variáveis Globais:
        - datamart (DatamartRepository): Uma instância da classe DatamartRepository para interação com o banco de dados.
        - handle_log (HandleLog): Uma instância da classe HandleLog para lidar com registros de logs no banco de dados.
        - etapa (str): Variável que armazena a etapa principal da automação.
        - subetapa (str): Variável que armazena a subetapa ou fase detalhada da automação.

    Execução:
        - Tenta executar uma automação RPA através da classe Rpa.
        - Registra um log de sucesso no banco de dados se a automação for concluída sem erros.
        - Em caso de exceção, registra um log de erro no banco de dados, incluindo detalhes como a etapa e subetapa em que ocorreu o erro.
"""
# 
from repository.datamart_repository import DatamartRepository
from static.tratamento_excecao import tratamento_excecao
from static.handler_log_processo import HandlerPersonalizado
from static.handler_log_nota import HandlerPersonalizadoNota
from static.registrar_consultar import Registers
from static.find_notes import FindNotes
from static.erros import ErroPrevisto
from etapas.read_excel_file import ReadExcelFile

if __name__ == "__main__":

    # Inicialização de instâncias
    datamart = DatamartRepository()
    excel_reader = ReadExcelFile()
    # excel_reader.atualizar_planilha(caminho_planilha=excel_reader.caminho_do_arquivo)
    excel_reader.inserir_dados_no_datamart()
    
