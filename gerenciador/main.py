# 
if __name__ == "__main__":
    try:
        import datetime
        import sys
        import os

        caminho_relativo = os.path.dirname(__file__)
        caminho_relativo = os.path.dirname(caminho_relativo)
        sys.path.append(caminho_relativo)

        ordem_das_etapas = ['static', 'verificar_cadastro', 'extracao_cbill', 'extracao_sicap',
                    'extracao_gedis', 'criar_cadastro', 'modificar_cadastro']
        
        for etapa in ordem_das_etapas:
            sys.path.append(os.path.join(caminho_relativo, etapa))

        from static.tratamento_excecao import tratamento_excecao
        import logging
        import psutil

        meu_pid = os.getpid()
        print(meu_pid)
        caminho_relativo_2 = caminho_relativo.lower()

        def obter_informacoes_processos():
            # Obtém a lista de objetos de Processo
            processos = [[p.info, p] for p in psutil.process_iter(['pid', 'name', 'cwd'])]

            # Exibe as informações de cada processo
            for processo in processos:
                if processo[0]['name'] == 'python.exe' or processo[0]['name'] == 'pythonw.exe':
                    processo[0]['cwd'] = processo[0]['cwd'].lower()
                    if caminho_relativo_2 in processo[0]['cwd'] and processo[0]['pid'] != meu_pid:
                        print(processo[0]['cwd'])
                        print(processo[0]['pid'])
                        
                        ## Encerra a ultima execução
                        # processo[1].kill()

        if __name__ == "__main__":
            obter_informacoes_processos()

        from static.handler_log_processo import HandlerPersonalizado
        from static.handler_log_nota import HandlerPersonalizadoNota
        from static.registrar_consultar import Registers
        from static.erros import ErroPrevisto
        from repository.datamart_repository import DatamartRepository
        from gerenciador_etapas.etapas.read_excel_file import ReadExcelFile
        from gerenciador_etapas.main import GerenciadorEtapas

        logger_processo = logging.Logger('')
        
        rpa = 'cadastro_aneel_go'
        
        # Inicialização das instâncias
        inst_register = Registers()
        datamart = DatamartRepository()
        inst_readexcel = ReadExcelFile()
        logger_processo = logging.Logger('')
        inst_handler_personalizado = HandlerPersonalizado(inst_register=inst_register, logger=logger_processo)
        logger_processo.setLevel(logging.DEBUG)
        logger_processo.addHandler(inst_handler_personalizado)
        logger_processo.dicionario = {'rpa': rpa}
        
        logger_nota = logging.Logger('')
        inst_handler_personalizado = HandlerPersonalizadoNota(inst_register=inst_register,
                                                              logger=logger_nota)
        logger_nota.setLevel(logging.DEBUG)
        logger_nota.addHandler(inst_handler_personalizado)
        
        ## Reseta a tabela fila para inserir novos dados
        # inst_register.reset_fila()
        
        ## Executa a atualização da planilha de conexões (Base para tratativa)
        # inst_readexcel.executar_atualizacao(caminho_planilha=inst_readexcel.caminho_do_arquivo)
        
        #Insere os dados da planilha de conexões no datamart
        # inst_register.inserir_dados_no_datamart()

        sql_busca_fila = f'''
            SELECT id, uc, ss_do_parecer FROM cadastro_aneel_go.fila
            where processado = False
            order by id asc
            '''
        lista_de_notas_fila = inst_register.consultar_notas(sql=sql_busca_fila)
        inst_gerenciador_etapas = GerenciadorEtapas(
            inst_register=inst_register,
            logger_nota=logger_nota,
            logger_processo=logger_processo
            )
        
        for nota_fila in lista_de_notas_fila:
            
            #Mandando da tabela fila pra tabela nota               
            inst_gerenciador_etapas.atualizar_fila_processado(id_nota_fila=nota_fila['id'])    

            id_tabela_nota = inst_gerenciador_etapas.migracao_para_tabela_nota(
                uc=nota_fila['uc'], ss_do_parecer=nota_fila['ss_do_parecer']
                                                                                )

            if id_tabela_nota is None:
                continue
            id_etapa, etapa = inst_gerenciador_etapas.definir_etapa(
                id_nota = id_tabela_nota
            )
            
            logger_nota.dicionario = {
                'etapa_fk': id_etapa
            }
            
            try:
                inst_gerenciador_etapas.execucao(
                    id_etapa = id_etapa,
                    etapa = etapa,
                    id_nota = id_tabela_nota
                )
                
            except Exception as excecao:
                if isinstance(excecao, ErroPrevisto):
                    logger_nota.critical(excecao.mensagem, str(type(excecao)), excecao.valor)
                    # Atualizar na tabela nota, a coluna repetir para False, \ 
                    # de acordo com o id da nota que eu tenho, 
                    inst_register.atualizar_registro(
                        dicionario={
                            'repetir': False,
                            'tempo_modificacao': datetime.datetime.now()
                            },
                        tabela='cadastro_aneel_go.nota',
                                                        id_=id_tabela_nota)
                else:
                    string_erro = tratamento_excecao()
                    logger_nota.error(string_erro, str(type(excecao)))
                    print(string_erro)

    except Exception as excecao:
        try:
            string_erro = tratamento_excecao()
        except:
            string_erro = excecao
            
        print(string_erro)
        # logger_processo.critical(msg=string_erro)
