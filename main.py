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
        dados = consultar_cep(cep)
        return dados
    except CEPNaoEncontrado:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
        
    except ProblemaDeComunicacao as erro:
        if erro.tipo == "timeout":
            raise HTTPException(status_code=504, detail="Tempo excedido")
        elif erro.tipo == "conexao":
            raise HTTPException(status_code=503, detail="Falha na conexão")
        elif erro.tipo == "resposta_http":
            raise HTTPException(status_code=502, detail="Resposta inválida do servidor")

    
class CEPNaoEncontrado(Exception):
    pass

class ProblemaDeComunicacao(Exception):
    def __init__(self, tipo):
        self.tipo = tipo
        
def consultar_cep(cep):
    
    try:
        resposta = httpx.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5.0)
        resposta.raise_for_status()

        dados = resposta.json()
    except httpx.TimeoutException:
        raise ProblemaDeComunicacao("timeout")
    except httpx.RequestError:
        raise ProblemaDeComunicacao("conexao")
    except httpx.HTTPStatusError:
        raise ProblemaDeComunicacao("resposta_http")

    if "erro" in dados:
            raise CEPNaoEncontrado("CEP não encontrado")

    return dados