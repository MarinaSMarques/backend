from pydantic import BaseModel

class VeiculoBase(BaseModel):
    nome: str
    cor: str
    km: float
    valor: float
    ano: int

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoUpdate(VeiculoBase):
    id: int

class Veiculo(VeiculoBase):
    id: int

    class Config:
        orm_mode = True
