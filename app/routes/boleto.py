from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import random

from app.database import get_db
from app.models import Pagamento

router = APIRouter(prefix="/boleto", tags=["Boleto"])


class BoletoPayment(BaseModel):
    nome: str
    cpf: str
    valor: float
    descricao: Optional[str] = "Pagamento via Boleto"


def gerar_linha_digitavel() -> str:
    return " ".join(["".join(str(random.randint(0, 9)) for _ in range(5)) for _ in range(5)])


@router.post("/gerar")
def gerar_boleto(pagamento: BoletoPayment, db: Session = Depends(get_db)):
    linha_digitavel = gerar_linha_digitavel()

    novo_pagamento = Pagamento(
        carteira_destino=pagamento.cpf,  # Armazenando CPF no campo carteira_destino
        moeda="BOLETO",
        valor=pagamento.valor,
        descricao=pagamento.descricao
    )
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    return {
        "status": "gerado",
        "mensagem": f"Boleto gerado para {pagamento.nome}",
        "linha_digitavel": linha_digitavel,
        "valor": f"R$ {pagamento.valor:.2f}",
        "descricao": pagamento.descricao,
        "id_transacao": novo_pagamento.id
    }
