from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Time, DateTime, ForeignKey, VARCHAR, Double
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
    uc = Column(VARCHAR, nullable=False, unique=True)
    ss_da_planilha = Column(VARCHAR, nullable=False)
    ss_do_parecer = Column(VARCHAR)
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
    numero = Column(Integer)
    bairro = Column(String)
    municipio = Column(String)
    cep = Column(VARCHAR)
    cpf = Column(VARCHAR)
    cnpj = Column(VARCHAR)
    quantidade_modulos = Column(Integer)
    fabricante_modulos = Column(String)
    area_arranjos = Column(Double)
    qtde_inversores = Column(Integer)
    fab_inversor = Column(String)
    pot_modulos_kwp = Column(Float)
    pot_inversores_kwp = Column(VARCHAR)
    grau_latitude = Column(String)
    grau_longitude = Column(String)
    instalacao = Column(VARCHAR)
    conta_contrato = Column(Integer)
    num_solicitacao_atc_protocolo = Column(Integer)
    unid_leitura = Column(String)
    qtd_gd = Column(Integer)
    email = Column(String)
    tel_movel = Column(String)
    tel_fixo = Column(String)
    conta_contrato_beneficiarias = Column(String)
    etapa_de_leitura_beneficiarias = Column(String)
    modelo_modulo = Column(String)
    modelo_inversor = Column(String)
    empresa = Column(String)
    concluido = Column(Boolean)

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
