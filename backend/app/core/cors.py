# app/config/cors.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "https://vvs-volvo-application-frontend.onrender.com",
        "http://localhost:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"], 
        allow_headers=["*"],  
    )
