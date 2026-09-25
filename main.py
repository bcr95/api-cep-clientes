from fastapi import FastAPI

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
        return {"erro": "CEP inválido"}
    
    return {"cep": cep}