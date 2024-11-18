from fastapi import FastAPI
from database.database import init_db
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api_analytics.fastapi import Analytics
from routes.user import user_route
from dotenv import load_dotenv
import os

load_dotenv()
secret_api =os.getenv('SECRET_API')

app = FastAPI()

app.include_router(user_route, prefix='/user')

app.add_middleware(Analytics, api_key = secret_api)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8080, reload=True)
