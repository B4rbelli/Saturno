from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pagamento

router = APIRouter(prefix="/pix", tags=["Pix"])


class PixPayment(BaseModel):
    chave_pix: str
    valor: float
    descricao: Optional[str] = "Pagamento via Pix"


@router.post("/pagar")
def pagar_com_pix(pagamento: PixPayment, db: Session = Depends(get_db)):
    novo_pagamento = Pagamento(
        carteira_destino=pagamento.chave_pix,
        moeda="PIX",
        valor=pagamento.valor,
        descricao=pagamento.descricao
    )
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    return {
        "status": "sucesso",
        "mensagem": f"Pagamento de R$ {pagamento.valor:.2f} via Pix enviado com sucesso!",
        "chave_destino": pagamento.chave_pix,
        "descricao": pagamento.descricao,
        "id_transacao": novo_pagamento.id
    }

