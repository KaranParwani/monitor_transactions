from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.monitoring_routes import transaction_router
from config import HOST, PORT

app = FastAPI()

app.include_router(transaction_router, prefix='/monitor')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)