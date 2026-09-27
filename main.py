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

    try:
        resposta = httpx.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5.0)
        resposta.raise_for_status()

        dados = resposta.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Tempo excedido")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Falha na conexão")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="Erro na resposta do serviço de CEP")

    if "erro" in dados:
        raise HTTPException(status_code=404, detail="CEP não encontrado")

    return dados