from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
import stripe
import os

from app.database import get_db
from app.models import Pagamento

router = APIRouter(prefix="/cartao", tags=["Cartão"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class StripePaymentRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Valor do pagamento em reais. Ex: 100.50")
    paymentMethodId: str = Field(..., description="ID do método de pagamento fornecido pelo Stripe.js.")
    description: Optional[str] = "Pagamento via Cartão"
    currency: str = "brl"


@router.post("/pagar")
async def pagar_com_cartao_stripe(payment_data: StripePaymentRequest, db: Session = Depends(get_db)):
    try:
        amount_in_cents = int(payment_data.amount * 100)

        intent = await stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=payment_data.currency,
            payment_method=payment_data.paymentMethodId,
            description=payment_data.description,
            confirm=True,
            metadata={"origem": "API Pagamentos", "valor_original": str(payment_data.amount)}
        )

        if intent.status == "succeeded":
            novo_pagamento = Pagamento(
                carteira_destino=payment_data.paymentMethodId,
                moeda="CARTAO",
                valor=payment_data.amount,
                descricao=payment_data.description
            )
            db.add(novo_pagamento)
            db.commit()
            db.refresh(novo_pagamento)

        return {
            "status": intent.status,
            "mensagem": "Requisição de pagamento enviada ao Stripe.",
            "clientSecret": intent.client_secret,
            "paymentIntentId": intent.id
        }

    except stripe.error.CardError as e:
        raise HTTPException(status_code=400, detail={
            "code": e.code,
            "message": e.user_message or str(e),
            "stripe_error_type": "CardError"
        })
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail={
            "code": e.code,
            "message": str(e),
            "stripe_error_type": "StripeError"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"Erro interno do servidor: {str(e)}"})
