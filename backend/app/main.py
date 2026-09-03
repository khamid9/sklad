from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import admin, auth, catalog, operations

app = FastAPI(title='Мой Склад API', version='1.0.0', description='REST API для простого управления складом')
app.add_middleware(CORSMiddleware, allow_origins=[origin.strip() for origin in settings.cors_origins.split(',')], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(operations.router)
app.include_router(admin.router)
@app.get('/health', tags=['Служебное'])
def health(): return {'status': 'ok'}
