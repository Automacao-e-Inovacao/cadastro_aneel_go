from static.postgresql import ConexaoPostgresql
from psycopg2.extensions import AsIs


class Registers:
    usuario_datamart = '5512983'
    senha_datamart = 'meuprimeiroacesso'
    nome_do_banco_de_dados_postgresql = 'datamart'
    ip_conexao_postgresql = '10.6.2.211'

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