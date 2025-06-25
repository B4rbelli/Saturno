from pydantic import BaseModel
from typing import Optional

class PagamentoCreate(BaseModel):
    id: int
    moeda: str
    valor: float
    descricao: Optional[str]
    carteira_destino: Optional[str]  # se usar Pix/Paypal/etc.

    model_config = {
        "from_attributes": True
    }
