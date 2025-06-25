from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import re

router = APIRouter(prefix="/cripto", tags=["Criptomoeda"])

MOEDAS_ACEITAS = {"BTC", "ETH", "XRP", "BNB", "SOL"}

class CriptoPayment(BaseModel):
    carteira_destino: str = Field(..., description="Endereço da carteira de destino")
    moeda: str = Field(..., description="Moeda: BTC, ETH, XRP, BNB ou SOL")
    valor: float
    descricao: Optional[str] = "Pagamento via Cripto"

def validar_btc(address: str) -> bool:
    # Bitcoin pode começar com 1, 3, ou bc1 (Bech32)
    if address.startswith('1') or address.startswith('3'):
        return bool(re.fullmatch(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}', address))
    elif address.startswith('bc1'):
        return bool(re.fullmatch(r'bc1[ac-hj-np-z02-9]{11,71}', address))
    return False

def validar_eth(address: str) -> bool:
    # Ethereum normalmente começa com 0x seguido de 40 hex chars
    return bool(re.fullmatch(r'0x[a-fA-F0-9]{40}', address))

def validar_xrp(address: str) -> bool:
    # Endereço Ripple geralmente começa com 'r' e tem 25-35 chars alfanum
    return bool(re.fullmatch(r'r[1-9A-HJ-NP-Za-km-z]{25,35}', address))

def validar_bnb(address: str) -> bool:
    # Binance Chain (BNB) usa endereços BEP2 que começam com "bnb" seguido de 39 chars alfanum minúsculos
    return bool(re.fullmatch(r'bnb1[0-9a-z]{38}', address))

def validar_sol(address: str) -> bool:
    # Solana address é uma string base58 com 32 ou 44 chars (simplificado)
    # Base58 = [1-9A-HJ-NP-Za-km-z], tamanho variável, geralmente 32 chars para chave pública
    return bool(re.fullmatch(r'[1-9A-HJ-NP-Za-km-z]{32,44}', address))

@router.post("/pagar")
def pagar_com_cripto(pagamento: CriptoPayment):
    moeda = pagamento.moeda.upper()

    if moeda not in MOEDAS_ACEITAS:
        raise HTTPException(
            status_code=400,
            detail=f"Moeda '{moeda}' não é aceita. Use: {', '.join(MOEDAS_ACEITAS)}."
        )

    # Validação detalhada da carteira
    if moeda == "BTC" and not validar_btc(pagamento.carteira_destino):
        raise HTTPException(status_code=400, detail="Carteira inválida para Bitcoin.")
    elif moeda == "ETH" and not validar_eth(pagamento.carteira_destino):
        raise HTTPException(status_code=400, detail="Carteira inválida para Ethereum.")
    elif moeda == "XRP" and not validar_xrp(pagamento.carteira_destino):
        raise HTTPException(status_code=400, detail="Carteira inválida para Ripple (XRP).")
    elif moeda == "BNB" and not validar_bnb(pagamento.carteira_destino):
        raise HTTPException(status_code=400, detail="Carteira inválida para Binance Coin (BNB).")
    elif moeda == "SOL" and not validar_sol(pagamento.carteira_destino):
        raise HTTPException(status_code=400, detail="Carteira inválida para Solana (SOL).")

    return {
        "status": "sucesso",
        "moeda": moeda,
        "mensagem": f"Transferência de {pagamento.valor:.4f} {moeda} enviada com sucesso!",
        "carteira": pagamento.carteira_destino,
        "descricao": pagamento.descricao
    }
