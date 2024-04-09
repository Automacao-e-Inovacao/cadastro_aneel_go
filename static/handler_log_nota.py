import logging
import time
import datetime


class HandlerPersonalizadoNota(logging.StreamHandler):

    def __init__(self, inst_register, logger):
        super().__init__()
        self.tabela_log = 'cadastro_aneel.log_nota'
        self.inst_register = inst_register
        self.logger = logger

    def emit(self, record: logging.LogRecord) -> None:
        if record:
            dicionario_log = self.logger.dicionario
            titulo_do_erro = record.msg.split(':|:')
            if len(titulo_do_erro) > 1:
                if titulo_do_erro[1] != '':
                    descricao_do_erro = titulo_do_erro[1]

                else:
                    descricao_do_erro = None
            else:
                descricao_do_erro = None
            titulo_do_erro = titulo_do_erro[0]

            dicionario_logger = {
                'carimbo_tempo': datetime.datetime.now(),
                'etapa_fk': dicionario_log['etapa_fk'],
                'arquivo': record.filename,
                'funcao': record.funcName,
                'linha': record.lineno,
                'level': record.levelname,
                'titulo_do_erro': titulo_do_erro,
                'descricao_do_erro': descricao_do_erro
            }
            self.inst_register.registro_sucesso(dicionario_logger, tabela=self.tabela_log)
