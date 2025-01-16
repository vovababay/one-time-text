import os
import uuid
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from pydantic import BaseModel

from utils import create_redis_cache, create_memcached_cache, create_memory_cache

app = FastAPI()

CACHE_BACKEND = os.getenv("CACHE_BACKEND", "memory").lower()

cache_backends = {
    "redis": create_redis_cache,
    "memcached": create_memcached_cache,
    "memory": create_memory_cache,
}

cache = cache_backends.get(CACHE_BACKEND, create_memory_cache)()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class SecretText(BaseModel):
    text: str
    duration: float = 1


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/create")
async def api_create_text(request: Request, secret_text: SecretText):
    text_id = str(uuid.uuid4())
    await cache.set(text_id, secret_text.text, ttl=secret_text.duration * 3600)
    base_url = str(request.base_url)
    access_url = f"{base_url}api/get/{text_id}"
    return JSONResponse({"url": access_url})

@app.get("/api/get/{text_id}")
async def api_get_text(text_id: str):
    print(text_id)
    text = await cache.get(text_id)
    if not text:
        raise HTTPException(status_code=404, detail="Text not found or expired")
    await cache.delete(text_id)
    return JSONResponse({"text": text})

@app.post("/create")
async def create_text(request: Request, text: str = Form(...), duration: int = Form(...)):
    if duration not in [1, 6, 12, 24]:
        raise HTTPException(status_code=400, detail="Invalid duration")
    text_id = str(uuid.uuid4())
    await cache.set(text_id, text, ttl=duration * 3600)
    base_url = str(request.base_url)
    access_url = f"{base_url}pre_get/{text_id}"
    return templates.TemplateResponse("print_url.html", {"request": {}, "text": access_url})

@app.get("/pre_get/{text_id}", response_class=HTMLResponse)
async def get_text(request: Request, text_id: str):
    text = await cache.get(text_id)
    if not text:
        message = 'Ссылка не валидна или срок действия ссылки истек'
        return templates.TemplateResponse("print_url.html", {"request": {}, "text": message})
    base_url = str(request.base_url)
    access_url = f"{base_url}get/{text_id}"
    return templates.TemplateResponse("pre_get.html", {"request": {}, "get_url": access_url})

@app.get("/get/{text_id}", response_class=HTMLResponse)
async def get_text(text_id: str):
    text = await cache.get(text_id)
    if not text:
        message = 'Ссылка не валидна или срок действия ссылки истек'
        return templates.TemplateResponse("print_url.html", {"request": {}, "text": message})
    await cache.delete(text_id)
    return templates.TemplateResponse("text.html", {"request": {}, "text": text})

