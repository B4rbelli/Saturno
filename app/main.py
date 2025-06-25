from fastapi import FastAPI
from app.routes import pix, cartao, paypal, cripto, boleto, pagamentos
from app.database import Base, engine

app = FastAPI(title="Sistema de Pagamento")


@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API de Pagamento"}


# Rotas de métodos de pagamento
app.include_router(pix.router)
app.include_router(cartao.router)
app.include_router(paypal.router)
app.include_router(cripto.router)
app.include_router(boleto.router)

# Nova rota de listagem de pagamentos
app.include_router(pagamentos.router)


# Criação automática das tabelas
def criar_tabelas():
    Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup_event():
    criar_tabelas()
