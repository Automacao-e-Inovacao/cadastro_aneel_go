from static.postgresql import ConexaoPostgresql
from psycopg2.extensions import AsIs
from unidecode import unidecode
import pandas as pd

class Registers:
    usuario_datamart = "5507011"
    senha_datamart = "meuprimeiroacesso"
    nome_do_banco_de_dados_postgresql = "datamart"
    ip_conexao_postgresql = "10.6.2.211"

    def __init__(self) -> None:                    
        self.conexao = ConexaoPostgresql(self.__class__.ip_conexao_postgresql,
                                         self.__class__.nome_do_banco_de_dados_postgresql,
                                         self.__class__.usuario_datamart, self.__class__.senha_datamart)

    def registro_sucesso(self, dicionario: dict, tabela: str) -> int:
        sql_insert = f'insert into {tabela} (%s) values %s'

        colunas_string = dicionario.keys()
        colunas_string = ','.join(colunas_string)
        
        return self.conexao.manipular(sql_insert, (AsIs(colunas_string), tuple(dicionario.values())))

    def atualizar_registro(self, dicionario: dict, tabela: str, id_: int, outro_filtro = None) -> None:
        
        string_set = dicionario.keys()
        lista = ['{}={}'.format(coluna, '%s') for coluna in string_set]
        string_set = ','.join(lista)
        
        if outro_filtro == None:
            sql_update = " update {} set {} where id = {} "
            sql_1 = sql_update.format(tabela, string_set, id_)
        else:
            sql_update = " update {} set {} {} "
            sql_1 = sql_update.format(tabela, string_set, outro_filtro)


        self.conexao.manipular(sql_1, tuple(dicionario.values()))

    def consultar_notas(self, sql: str) -> list:
        lista = self.conexao.consultar(sql)
        return lista
    
    def reset_fila(self):
        sql_reset_fila = f'''
        TRUNCATE TABLE cadastro_aneel_go.fila RESTART IDENTITY
        '''
        
        self.conexao.query(sql=sql_reset_fila)
    
    def query(self, sql: str) -> list:
        self.conexao.query(sql)

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
                'NUMERO_SS': 'ss_da_planilha',                                
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
            
            # Lendo o arquivo Excel
            dataframe = pd.read_csv(excel_file_path, sep=',', header=None, na_filter=False, encoding='latin1')
            
            dataframe = dataframe.applymap(lambda x: unidecode(str(x)) if isinstance(x, str) else x)
            
            # Renomeando as colunas do DataFrame
            dataframe = self.rename_dataframe_columns(dataframe)

            # Convertendo o DataFrame para uma lista de dicionários
            data = dataframe.iloc[1:].to_dict(orient='records')
            
            return data
            
        except Exception as e:
            print(f"Erro ao converter o arquivo Excel para DataFrame: {e}")
            return None

    def inserir_dados_no_datamart(self):
        """
        Lê o arquivo Excel e insere os dados na tabela Fila do datamart.
        """
        try:
            # Convertendo o arquivo Excel para DataFrame
            data_to_insert = self.convert_excel_to_dataframe()
            
            # Iterando sobre os dados a serem inseridos
            for row in data_to_insert:
                # Criando um dicionário com os dados da linha
                data = {
                    'uc': str(row[0]),
                    'ss_da_planilha': str(row[1]),
                    'status_ss': str(row[2]),
                    'servico': str(row[3]),
                    'created_at': str(row[4]),
                }
                
                # Convertendo todos os valores do dicionário para strings
                data_str = {str(key): str(value) for key, value in data.items()}
                
                # Inserindo os dados na tabela 'cadastro_aneel_go.fila'
                self.registro_sucesso(data_str, tabela='cadastro_aneel_go.fila')
                
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir dados no datamart: {e}")

