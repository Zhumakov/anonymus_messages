from contextlib import asynccontextmanager

from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    debug=True,
    title="Anonym messages",
    description="Сайт для анонимных для отправки анонимных сообщений",
    lifespan=lifespan,
)


@app.get(
    "/",
    description="Основная страница с описанием и приглашением для регистрации",
)
def main_page(request: Request):
    return {"content": "Это главная страница"}
