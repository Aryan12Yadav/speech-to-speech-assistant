from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes.voice import router as voice_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# /audio mount nahi chahiye ab

templates = Jinja2Templates(directory="app/templates")
app.include_router(voice_router, prefix="/api")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

