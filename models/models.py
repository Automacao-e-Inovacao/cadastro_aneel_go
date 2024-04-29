from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Time, DateTime, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Nota(Base):
    """
    Modelo da tabela 'nota' do schema 'cadastro_aneel_go'.
    """
    __tablename__ = "nota"
    __table_args__ = {'schema': 'cadastro_aneel_go'}

    id = Column(Integer, primary_key=True)
    uc = Column(VARCHAR, nullable=False)
    ss_da_planilha = Column(VARCHAR, nullable=False)
    ss_do_parecer = Column(VARCHAR, nullable=False)
    tempo_criacao = Column(DateTime)
    tempo_modificacao = Column(DateTime)
    repetir = Column(Boolean, default=True)
    concluido = Column(Boolean, default=False)
    num_cadastro_gd = Column(String)
    nome_cliente = Column(String)
    classe_consumo = Column(String)
    gru_tar	= Column(String)
    modalidade = Column(String)
    data_solicitacao_conexao_gd = Column(DateTime)
    data_aprov_p_conexao = Column(DateTime)
    tipo_fonte = Column(String)
    endereco = Column(String)
    numero = Column(Integer, nullable=False)
    bairro = Column(String)
    municipio = Column(String, nullable=False)
    cep = Column(Integer)
    cpf = Column(Integer)
    cnpj = Column(Integer)
    quantidade_modulos = Column(Integer, nullable=False)
    fabricante_modulos = Column(String, nullable=False)
    area_arranjos = Column(Float, nullable=False)
    qtde_inversores = Column(Integer, nullable=False)
    fab_inversor = Column(String)
    pot_modulos_kwp = Column(Float, nullable=False)
    pot_inversor_kw = Column(Integer, nullable=False)
    grau_latitude = Column(String, nullable=False)
    grau_longitude = Column(String, nullable=False)
    instalacao = Column(Integer, nullable=False)
    conta_contrato = Column(Integer, nullable=False)
    num_solicitacao_atc_protocolo = Column(Integer, nullable=False)
    unid_leitura = Column(String, nullable=False)
    qtd_gd = Column(Integer)
    email = Column(String, nullable=False)
    tel_movel = Column(String, nullable=False)
    tel_fixo = Column(String, nullable=False)
    conta_contrato_beneficiarias = Column(String, nullable=False)
    etapa_de_leitura_beneficiarias = Column(String, nullable=False)
    modelo_modulo = Column(String, nullable=False)
    modelo_inversor = Column(String, nullable=False)
    empresa = Column(String, nullable=False)
    concluido = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Nota(id={self.id}, nota={self.nota}, tempo_criacao={self.tempo_criacao}, tempo_modificacao={self.tempo_modificacao}, num_cadastro_gd={self.num_cadastro_gd}, nome_cliente={self.nome_cliente}, classe_consumo={self.classe_consumo}, gru_tar={self.gru_tar}, modalidade={self.modalidade}, data_solicitacao_conexao_gd={self.data_solicitacao_conexao_gd}, data_aprov_p_conexao={self.data_aprov_p_conexao}, tipo_fonte={self.tipo_fonte}, endereco={self.endereco}, numero={self.numero}, bairro={self.bairro}, municipio={self.municipio}, cep={self.cep}, cpf={self.cpf}, cnpj={self.cnpj}, quantidade_modulos={self.quantidade_modulos}, fabricante_modulos={self.fabricante_modulos}, area_arranjos={self.area_arranjos}, qtde_inversores={self.qtde_inversores}, fab_inversor={self.fab_inversor}, pot_modulos_kwp={self.pot_modulos_kwp}, pot_inversor_kw={self.pot_inversor_kw}, grau_latitude={self.grau_latitude}, grau_longitude={self.grau_longitude}, instalacao={self.instalacao}, conta_contrato={self.conta_contrato}, num_solicitacao_atc_protocolo={self.num_solicitacao_atc_protocolo}, unid_leitura={self.unid_leitura}, qtd_gd={self.qtd_gd}, email={self.email}, tel_movel={self.tel_movel}, tel_fixo={self.tel_fixo}, conta_contrato_beneficiarias={self.conta_contrato_beneficiarias}, etapa_de_leitura_beneficiarias={self.etapa_de_leitura_beneficiarias}, modelo_modulo={self.modelo_modulo}, modelo_inversor={self.modelo_inversor}, empresa={self.empresa}, concluido={self.concluido})>"
        
class Fila(Base):
    """
    Modelo da tabela 'nota' do schema 'cadastro_aneel_go'.
    """
    __tablename__ = "fila"
    __table_args__ = {'schema': 'cadastro_aneel_go'}

    id = Column(Integer, primary_key=True)
    uc = Column(VARCHAR, nullable=False)
    ss_da_planilha = Column(VARCHAR, nullable=False)
    servico = Column(VARCHAR, nullable=False)
    status_ss = Column(String, nullable=False)
    created_at = Column(DateTime)
    processado = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Fila(id={self.id}, nota={self.nota}, created_at={self.created_at}, processado={self.processado}, empresa={self.empresa})>"

class Etapa(Base):
    """
    Modelo da tabela 'etapa' do schema 'cadastro_aneel_go'.
    """
    __tablename__ = "etapa"
    __table_args__ = {'schema': 'cadastro_aneel_go'}

    id = Column(Integer, primary_key=True)
    nota_fk = Column(Integer, ForeignKey('cadastro_aneel_go.nota.id'))
    repetir = Column(Boolean, nullable=False, default=True)
    concluido = Column(Boolean, nullable=False, default=False)
    etapa = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    nota = relationship("Nota", back_populates="etapas")

    def __repr__(self):
        return f"<Etapa(id={self.id}, nota_fk={self.nota_fk}, ...)>"

class LogNota(Base):
    """
    Modelo da tabela 'log_nota' do schema 'cadastro_aneel_go'.
    """
    __tablename__ = "log_nota"
    __table_args__ = {'schema': 'cadastro_aneel_go'}

    id = Column(Integer, primary_key=True)
    etapa_fk = Column(Integer, ForeignKey('cadastro_aneel_go.etapa.id'))
    arquivo = Column(String, nullable=False)
    funcao = Column(String, nullable=False)
    linha = Column(String, nullable=False)
    level = Column(String, nullable=False)
    titulo_do_erro = Column(String, nullable=False)
    descricao_do_erro = Column(String)
    created_at = Column(DateTime)

    etapa = relationship("Etapa", back_populates="logs")

    def __repr__(self):
        return f"<LogNota(id={self.id}, etapa_fk={self.etapa_fk}, arquivo={self.arquivo}, funcao={self.funcao}, linha={self.linha}, level={self.level}, titulo_do_erro={self.titulo_do_erro}, descricao_do_erro={self.descricao_do_erro}, created_at={self.created_at})>"

Nota.etapas = relationship("Etapa", order_by=Etapa.id, back_populates="nota")
Etapa.logs = relationship("LogNota", order_by=LogNota.id, back_populates="etapa")
