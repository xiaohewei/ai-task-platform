from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
  return ["hello,world"]

@app.get("/goodbye")
async def goodbye():
  return ["goodbye"]
