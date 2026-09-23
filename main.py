from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def mensagem():
    return {"mensagem": "API funcionando!"}