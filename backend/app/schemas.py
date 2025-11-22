from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

from .validators import sanitize_document, is_valid_cpf, is_valid_cnpj


class UsuarioBase(BaseModel):
    nome: str
    cpf_cnpj: str
    apartamento: Optional[str] = None
    bloco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None

    @validator("cpf_cnpj")
    def validar_cpf_cnpj(cls, v: str) -> str:
        doc = sanitize_document(v)
        if len(doc) == 11:
            if not is_valid_cpf(doc):
                raise ValueError("CPF inválido")
        elif len(doc) == 14:
            if not is_valid_cnpj(doc):
                raise ValueError("CNPJ inválido")
        else:
            raise ValueError("CPF/CNPJ deve ter 11 (CPF) ou 14 (CNPJ) dígitos")
        return doc  # salva sempre só os dígitos


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioRead(UsuarioBase):
    id: int

    class Config:
        orm_mode = True


###############################################
# ENCOMENDAS
###############################################

class EncomendaBase(BaseModel):
    cpf_cnpj: str
    codigo_ocr_detectado: Optional[str] = None
    nome_detectado: Optional[str] = None

class EncomendaCreate(EncomendaBase):
    pass

class EncomendaRead(BaseModel):
    id: int
    usuario_id: int
    status: str
    data_recebimento: datetime
    codigo_ocr_detectado: Optional[str]
    nome_detectado: Optional[str]
    data_retirada: Optional[datetime] = None

    class Config:
        orm_mode = True

class EncomendaList(BaseModel):
    id: int
    usuario_id: int
    data_recebimento: datetime
    status: str
    nome_detectado: Optional[str] = None
    codigo_ocr_detectado: Optional[str] = None

    class Config:
        orm_mode = True
