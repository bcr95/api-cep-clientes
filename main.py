from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

@app.get("/")
def mensagem():
    return {"mensagem": "API funcionando!"}

@app.get("/health")
def status():
    return {"status": "ok"}

@app.get("/ceps/{cep}")
def buscar(cep: str):
    if len(cep) != 8 or not cep.isdigit(): 
        raise HTTPException(status_code=400, detail="CEP inválido")

    resposta = httpx.get(f"https://viacep.com.br/ws/{cep}/json/")
    dados = resposta.json()

    if "erro" in dados:
        raise HTTPException(status_code=404, detail="CEP não encontrado")

    return dados