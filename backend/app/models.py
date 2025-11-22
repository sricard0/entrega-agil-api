from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

#########################################
# TABELA DE USUÁRIOS
#########################################

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String, nullable=False, unique=True, index=True)
    apartamento = Column(String, nullable=True)
    bloco = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    encomendas = relationship("Encomenda", back_populates="usuario")


#########################################
# TABELA DE ENCOMENDAS
#########################################

class Encomenda(Base):
    __tablename__ = "encomendas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    
    codigo_ocr_detectado = Column(String, nullable=True)
    nome_detectado = Column(String, nullable=True)
    imagem_original = Column(String, nullable=True)

    data_recebimento = Column(DateTime, default=datetime.now)
    data_retirada = Column(DateTime, nullable=True)

    status = Column(String, default="PENDENTE")  # PENDENTE | RETIRADA

    usuario = relationship("Usuario", back_populates="encomendas")
    notificacoes = relationship("Notificacao", back_populates="encomenda")


#########################################
# TABELA DE NOTIFICAÇÕES
#########################################

class Notificacao(Base):
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True, index=True)
    encomenda_id = Column(Integer, ForeignKey("encomendas.id"))

    tipo = Column(String, nullable=False)  # whatsapp | email
    data_envio = Column(DateTime, default=datetime.now)
    status_envio = Column(String, default="ENVIADO")  # ok | erro

    encomenda = relationship("Encomenda", back_populates="notificacoes")


#########################################
# TABELA DE LOGS DE OCR
#########################################

class LogOCR(Base):
    __tablename__ = "logs_ocr"

    id = Column(Integer, primary_key=True, index=True)
    texto_extraido = Column(Text, nullable=False)
    confianca = Column(String, nullable=True)
    caminho_imagem = Column(String, nullable=True)
    data = Column(DateTime, default=datetime.now)

