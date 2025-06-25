from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Pagamento
from app.schemas import PagamentoCreate

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.get("/", response_model=List[PagamentoCreate])
def listar_pagamentos(
    moeda: Optional[str] = Query(None, description="Filtrar por moeda (ex: PIX, BOLETO, PAYPAL, etc.)"),
    valor_min: Optional[float] = Query(None, description="Valor mínimo do pagamento"),
    valor_max: Optional[float] = Query(None, description="Valor máximo do pagamento"),
    db: Session = Depends(get_db)
):
    query = db.query(Pagamento)

    if moeda:
        query = query.filter(Pagamento.moeda.ilike(moeda))
    if valor_min is not None:
        query = query.filter(Pagamento.valor >= valor_min)
    if valor_max is not None:
        query = query.filter(Pagamento.valor <= valor_max)

    return query.order_by(Pagamento.id.desc()).all()
