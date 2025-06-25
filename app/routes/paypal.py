from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pagamento

router = APIRouter(prefix="/paypal", tags=["PayPal"])


class PayPalPayment(BaseModel):
    email: EmailStr
    senha: str  # Observação: não deve ser usada em produção!
    valor: float
    descricao: Optional[str] = "Pagamento via PayPal"


@router.post("/pagar")
def pagar_com_paypal(pagamento: PayPalPayment, db: Session = Depends(get_db)):
    # Simulando bloqueio de conta
    if pagamento.email.endswith("@test.com"):
        raise HTTPException(status_code=403, detail="Conta PayPal bloqueada ou inválida.")

    # Registro no banco de dados
    novo_pagamento = Pagamento(
        carteira_destino=pagamento.email,
        moeda="PAYPAL",
        valor=pagamento.valor,
        descricao=pagamento.descricao
    )
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    return {
        "status": "sucesso",
        "mensagem": f"Pagamento de R$ {pagamento.valor:.2f} via PayPal realizado com sucesso!",
        "email_destino": pagamento.email,
        "descricao": pagamento.descricao,
        "id_transacao": novo_pagamento.id
    }
