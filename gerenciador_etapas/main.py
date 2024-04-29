import os
import sys
import datetime

caminho_relativo = os.path.dirname(__file__)
caminho_relativo_2 = os.path.dirname(caminho_relativo)
caminho_relativo = os.path.join(caminho_relativo, 'etapas')
sys.path.append(caminho_relativo)
ordem_das_etapas = ['verificar_cadastro', 'extracao_cbill', 'extracao_sicap',
                    'extracao_gedis', 'criar_cadastro', 'modificar_cadastro']
for etapa in ordem_das_etapas:
    sys.path.append(os.path.join(caminho_relativo, etapa))
    
ordem_das_etapas_2 = ['static']
for etapa in ordem_das_etapas_2:
    sys.path.append(os.path.join(caminho_relativo_2, etapa))
    
from static.registrar_consultar import Registers
from gerenciador_etapas.etapas.cadastro_site_aneel.main import CadastroSiteAneel
from gerenciador_etapas.etapas.cadastro_site_aneel.static_site_aneel import StaticSiteAneel
from gerenciador_etapas.etapas.extract_data_sicap.main import ExtracoesDadosSicap
from gerenciador_etapas.etapas.extract_data_cbill.main import ExtracoesDadosCbill
from gerenciador_etapas.etapas.extract_data_gedis.main import ExtracoesDadosGedis


class GerenciadorEtapas:
    def __init__(self, inst_register:Registers, logger_nota, logger_processo, static_site_aneel: StaticSiteAneel) -> None:
        self.tabela = 'cadastro_aneel_go.nota'
        self.logger_nota = logger_nota
        self.logger_processo = logger_processo
        self.inst_register = inst_register
        self.static_site_aneel = static_site_aneel
        self.tabela_etapa = 'cadastro_aneel_go.etapa'
        self.inst_cadastro_site_aneel = CadastroSiteAneel(logger_nota= self.logger_nota,
                                                          inst_register=self.inst_register,
                                                          inst_static_site_aneel=self.static_site_aneel
                                                          )
        self.inst_static_cbill = ExtracoesDadosCbill(logger_nota=self.logger_nota,
                                                     inst_register=self.inst_register,
                                                     )
        self.inst_static_gedis = ExtracoesDadosGedis(logger_nota=self.logger_nota,
                                                     inst_register=self.inst_register,
                                                     )
        self.inst_static_sicap = ExtracoesDadosSicap(logger_nota=self.logger_nota,
                                                     inst_register=self.inst_register,
                                                     )
        
    def atualizar_fila_processado(self, id_nota_fila):
        dicionario = {
            'processado': True
            }
        self.inst_register.atualizar_registro(
            dicionario = dicionario,
            tabela = 'cadastro_aneel_go.fila',
            id_ = id_nota_fila
        )
           
    def migracao_para_tabela_nota(self, uc, ss_da_planilha) -> int | None:
        """
        Migra dados para a tabela 'nota' no banco de dados.

        Args:
            uc (str): O valor do campo 'uc' a ser inserido na tabela.
            ss_do_parecer (str): O valor do campo 'ss_do_parecer' a ser inserido na tabela.

        Returns:
            int | None: O ID do registro inserido ou None, dependendo da operação realizada.
        """
        # Cria uma consulta SQL para verificar se já existem registros com os mesmos valores de 'uc' e 'ss_do_parecer'
        sql_consulta_nota = f'''
        SELECT * FROM cadastro_aneel_go.nota
        WHERE uc = '{uc}' 
        AND ss_da_planilha = '{ss_da_planilha}
        '
        '''
        # Executa a consulta SQL
        lista_notas = self.inst_register.consultar_notas(
            sql=sql_consulta_nota
        )

        # Verifica se não há notas correspondentes na consulta
        if len(lista_notas) == 0: 
            # Se não houver, cria um dicionário de inserção com os valores de 'uc' e 'ss_do_parecer'
            dicionario_insercao = {
                'uc': uc
                ,'ss_da_planilha': ss_da_planilha
            }
            # Insere os dados na tabela 'nota' e obtém o ID do registro inserido
            id_nota = self.inst_register.registro_sucesso(
                dicionario=dicionario_insercao,
                tabela='cadastro_aneel_go.nota'
            )
        else:
            # Se houver notas correspondentes
            dicionario_nota = lista_notas[0]
            # Verifica se a nota correspondente pode ser repetida (indicada pelo valor da coluna 'repetir')
            if dicionario_nota['repetir']:
                # Se puder ser repetida, retorna o ID da nota existente
                id_nota = dicionario_nota['id']
            else:
                # Se não puder ser repetida, retorna None indicando que nenhum novo registro foi inserido
                return None
        
        # Retorna o ID do registro inserido ou None, dependendo da operação realizada
        return id_nota

    def definir_etapa(self, id_nota) -> tuple:
        sql_consulta_etapa = f'''
        select * from cadastro_aneel_go.etapa
        where nota_fk = {id_nota}
        '''
        lista_etapas = self.inst_register.consultar_notas(
            sql=sql_consulta_etapa
        )
        if len(lista_etapas) == 0: 
            etapa = 'Verificar Cadastro Site ANEEL'
            
            dicionario_etapa = {
                'nota_fk': id_nota,
                'etapa': etapa
            }
            id_etapa = self.inst_register.registro_sucesso(
                dicionario=dicionario_etapa,
                tabela='cadastro_aneel_go.etapa'
            )
            return id_etapa, etapa
        else:
            for dicionario_etapa_repeticao in lista_etapas:
                if not dicionario_etapa_repeticao['concluido']:
                    break
            else:
                return
            
            id_etapa = dicionario_etapa_repeticao['id']
            etapa = dicionario_etapa_repeticao['etapa']
            
            return id_etapa, etapa
    
    def execucao(self, id_etapa, etapa, id_nota):
        if etapa == 'Verificar Cadastro Site ANEEL': 
            self.inst_cadastro_site_aneel.verificar_cadastro()
            self.inst_register.atualizar_registro(dicionario={
                                                    'concluido': True
                                                    ,'update_at': datetime.datetime.now()},
                                                  tabela=self.tabela_etapa, id_=id_etapa)
            etapa = 'Extrair dados CBILL'
            etapa_fk = self.inst_register.registro_sucesso(dicionario={'etapa': etapa, 'nota_fk': id_nota},
                                                           tabela=self.tabela_etapa)
            id_etapa = etapa_fk

        if etapa == 'Extrair dados CBILL':
            # self.inst_extracaoeqtlinfo.extracao(id_nota=id_nota)
            self.inst_register.atualizar_registro(dicionario={
                                                            'concluido': True
                                                            ,'update_at': datetime.datetime.now()},
                                                  tabela=self.tabela_etapa, id_=id_etapa)
            etapa = 'Extrair dados SICAP'
            etapa_fk = self.inst_register.registro_sucesso(dicionario={'etapa': etapa, 'nota_fk': id_nota},
                                                           tabela=self.tabela_etapa)
            id_etapa = etapa_fk

        if etapa == 'Extrair dados SICAP':
            # self.inst_gerar_carta.criarcarta(id_nota=id_nota)
            self.inst_register.atualizar_registro(dicionario={
                                                            'concluido': True
                                                            ,'update_at': datetime.datetime.now()},
                                                  tabela=self.tabela_etapa, id_=id_etapa)
            etapa = 'Extrair dados GEDIS'
            etapa_fk = self.inst_register.registro_sucesso(dicionario={'etapa': etapa, 'nota_fk': id_nota},
                                                           tabela=self.tabela_etapa)
            id_etapa = etapa_fk

        if etapa == 'Extrair dados GEDIS':
            # self.inst_conclusaocrm.conclusao_crm(id_nota=id_nota)
            self.inst_register.atualizar_registro(dicionario={
                                                            'concluido': True
                                                            ,'update_at': datetime.datetime.now()},
                                                  tabela=self.tabela_etapa, id_=id_etapa)
            etapa = 'Criar cadastro Site Aneel'
            etapa_fk = self.inst_register.registro_sucesso(dicionario={'etapa': etapa, 'nota_fk': id_nota},
                                                           tabela=self.tabela_etapa)
            id_etapa = etapa_fk

        if etapa == 'Criar cadastro Site Aneel':
            # self.inst_concluir_nota.conclusao(id_nota=id_nota)
            self.inst_register.atualizar_registro(dicionario={
                                                    'concluido': True
                                                    # ,'update_at': datetime.datetime.now()
                                                    },
                                                  tabela=self.tabela_etapa, id_=id_etapa)
            self.inst_register.atualizar_registro(
                dicionario= {
                    'tempo_modificacao': datetime.datetime.now(),
                    'concluido': True,
                    'repetir': False
                },
                tabela='cadastro_aneel_go.nota',
                id_=id_nota
                                                  )
