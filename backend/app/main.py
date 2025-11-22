from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from .database import SessionLocal, engine, Base
from . import models
from . import schemas

# cria todas as tabelas no banco, se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Entrega Ágil API")


# dependência de sessão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "API Entrega Ágil funcionando"}


@app.get("/teste-db")
def testar_conexao(db: Session = Depends(get_db)):
    novo = models.LogOCR(texto_extraido="Teste", confianca="1.0")
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"id": novo.id, "texto": novo.texto_extraido}


@app.post("/usuarios", response_model=schemas.UsuarioRead, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # verifica se já existe usuário com o mesmo CPF/CNPJ
    existente = db.query(models.Usuario).filter(
        models.Usuario.cpf_cnpj == usuario.cpf_cnpj
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe usuário cadastrado com este CPF/CNPJ.",
        )

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        cpf_cnpj=usuario.cpf_cnpj,
        apartamento=usuario.apartamento,
        bloco=usuario.bloco,
        telefone=usuario.telefone,
        email=usuario.email,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post("/encomendas", response_model=schemas.EncomendaRead, status_code=status.HTTP_201_CREATED)
def criar_encomenda(encomenda: schemas.EncomendaCreate, db: Session = Depends(get_db)):

    # Sanitizar CPF/CNPJ
    cpf = encomenda.cpf_cnpj.replace(".", "").replace("-", "").replace("/", "")

    # Verificar se usuário existe
    usuario = db.query(models.Usuario).filter(
        models.Usuario.cpf_cnpj == cpf
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado para este CPF/CNPJ."
        )

    # Criar encomenda
    nova = models.Encomenda(
        usuario_id=usuario.id,
        codigo_ocr_detectado=encomenda.codigo_ocr_detectado,
        nome_detectado=encomenda.nome_detectado,
        status="PENDENTE",
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova

@app.get("/encomendas/pendentes", response_model=list[schemas.EncomendaList])
def listar_encomendas_pendentes(db: Session = Depends(get_db)):
    pendentes = (
        db.query(models.Encomenda)
        .filter(models.Encomenda.status == "PENDENTE")
        .order_by(models.Encomenda.data_recebimento.desc())
        .all()
    )
    return pendentes



@app.patch("/encomendas/{encomenda_id}/retirar", response_model=schemas.EncomendaRead)
def retirar_encomenda(encomenda_id: int, db: Session = Depends(get_db)):
    encomenda = db.query(models.Encomenda).filter(
        models.Encomenda.id == encomenda_id
    ).first()

    if not encomenda:
        raise HTTPException(
            status_code=404,
            detail="Encomenda não encontrada."
        )

    if encomenda.status == "RETIRADA":
        raise HTTPException(
            status_code=400,
            detail="Esta encomenda já foi marcada como retirada."
        )

    encomenda.status = "RETIRADA"
    encomenda.data_retirada = datetime.now()

    db.commit()
    db.refresh(encomenda)

    return encomenda

