import pandas as pd

class Utils:
    """
    Esta classe fornece utilidades diversas para manipulação de DataFrames e arquivos Excel.
    """
    def __init__(self) -> None:
        """
        Inicializa o atributo path com o caminho para o diretório base utilizado na manipulação de arquivos.
        """
        pass  # Não é necessário inicializar nada no construtor

    def rename_dataframe_columns(self, df):
        """
        Renomeia as colunas do dataframe para o formato do banco de dados
        
        Args:
            df (pd.DataFrame): DataFrame cujas colunas serão renomeadas.

        Returns:
            pd.DataFrame: DataFrame com as colunas renomeadas.
        """
        df = df.rename(
            columns={
                'UC': 'uc',
                'SS': 'ss_da_planilha',                                
                'STATUS_SS':'status_ss',
                'SERVICO':'servico',
            },
        )

        return df

    def convert_excel_to_dataframe(self):
        """
        Converte a planilha excel em um dataframe
        
        Returns:
            pd.DataFrame: DataFrame criado a partir do arquivo Excel.
        """
        try:
            from gerenciador_etapas.etapas.read_excel_file import ReadExcelFile
            read_excel_file = ReadExcelFile()
            excel_file_path = read_excel_file.caminho_do_arquivo
            
            df = pd.read_excel(excel_file_path, sheet_name="Base", header=None, na_filter=False)
            
            # Renomeando colunas
            df = self.rename_dataframe_columns(df)
            
            return df
        
        except Exception as e:
            print(f"Erro ao converter o arquivo Excel para DataFrame: {e}")
            return None
