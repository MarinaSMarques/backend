from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///veiculos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Veiculo(Base):
    __tableveiculos__ = "veiculos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(80), unique=True, index=True, nullable=False)
    cor = Column(String(20), nullable=False)
    km = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    ano = Column(Integer, nullable=False)


class VeiculoSchema(BaseModel):
    nome: str
    cor: str
    km: int
    valor: float
    ano: int


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/veiculos/", response_model=List[VeiculoSchema])
async def get_veiculos(db: Session = Depends(get_db)):
    veiculos = db.query(Veiculo).all()
    return veiculos

@app.post("/veiculos/", response_model=VeiculoSchema)
async def create_veiculo(veiculo: VeiculoSchema, db: Session = Depends(get_db)):
    db_veiculo = Veiculo(nome=veiculo.nome, cor=veiculo.cor, km=veiculo.km, valor=veiculo.valor, ano=veiculo.ano)
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo

@app.get("/veiculos/{veiculo_id}", response_model=VeiculoSchema)
async def get_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    db_veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return db_veiculo

@app.put("/veiculos/{veiculo_id}", response_model=VeiculoSchema)
async def update_veiculo(veiculo_id: int, veiculo: VeiculoSchema, db: Session = Depends(get_db)):
    db_veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id)
    db_veiculo.update(veiculo.dict())
    db.commit()
    db_veiculo = db_veiculo.first()
    if db_veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return db_veiculo

@app.delete("/veiculos/{veiculo_id}")
async def delete_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    db_veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id)
    db_veiculo.delete(synchronize_session=False)
    db.commit()
    return {"message": "Veículo deletado"}
