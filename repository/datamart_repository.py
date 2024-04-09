from datetime import datetime
import pandas as pd
import sys
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import psycopg2

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from models.models import Base, Nota, Fila, Etapa, LogNota

class DatamartRepository:
    """
        Utiliza o SQLAlchemy
    """
    def __init__(self):
        """
            Configura a conexão com o banco de dados PostgreSQL e cria a tabela se não existir.
        """
        self.database_user = 5512983
        self.database_pass = "meuprimeiroacesso"
        self.database_host = "10.6.2.211"
        self.database_name = "datamart"
        self.schema_name = "cadastro_aneel_go"

        # Configurando a conexão com o banco de dados
        self.engine = sqlalchemy.create_engine(f"postgresql://{self.database_user}:{self.database_pass}@{self.database_host}/{self.database_name}")

        # Cria uma sessão
        session = sessionmaker(bind=self.engine)
        self.session = session()

        # Cria tabela no banco de dados
        Base.metadata.create_all(self.engine)

    def save_dataframe_to_table(self, dataframe):
        """
        Salva um DataFrame em uma tabela PostgreSQL no banco de dados.

        Args:
            dataframe (pd.DataFrame): DataFrame a ser salvo.

        Returns:
            None
        """
        # Converter o DataFrame para uma lista de dicionários
        data_to_insert = dataframe.iloc[1:].to_dict(orient='records')

        # Modificar a estrutura de cada dicionário na lista conforme necessário
        for row in data_to_insert:
            modified_row = {
                'uc': row[0],
                'ss_do_parecer': row[1],
                'status_ss': row[2],
                'servico': row[3],
                'created_at': row[4],
                'updated_at': row[5]
            }

            # # Aqui você pode imprimir o dicionário modificado para verificar sua estrutura antes de inseri-lo
            # print(modified_row)

            # Inserir o dicionário modificado na tabela do banco de dados
            self.session.bulk_insert_mappings(Fila, [modified_row])

        # Confirmar a transação
        self.session.commit()


    def save_etapas_to_table(self, data):
        """
        Salva dados na tabela Etapa do banco de dados.

        Args:
            data (dict or list of dicts): Dados a serem inseridos na tabela Etapa.

        Returns:
            None
        """
        if isinstance(data, dict):
            data = [data]  # Se for apenas um dicionário, transforma em uma lista de dicionários

        # Adiciona as colunas 'created_at' e 'updated_at' aos dados
        for item in data:
            item['created_at'] = datetime.now()

        # Insere os dados no banco
        self.session.bulk_insert_mappings(Etapa, data)
        self.session.commit()

    def save_lognota_to_table(self, data):
        """
        Salva dados na tabela LogNota do banco de dados.

        Args:
            data (dict or list of dicts): Dados a serem inseridos na tabela LogNota.

        Returns:
            None
        """
        if isinstance(data, dict):
            data = [data]  # Se for apenas um dicionário, transforma em uma lista de dicionários

        # Adiciona as colunas 'created_at' e 'updated_at' aos dados
        for item in data:
            item['created_at'] = datetime.now()
            item['updated_at'] = datetime.now()

        # Insere os dados no banco
        self.session.bulk_insert_mappings(LogNota, data)
        self.session.commit()
