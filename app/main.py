from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from app.conn import SocketHandler

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
# )
socket_manager = SocketManager(app=app, socketio_path="", mount_location="")
SocketHandler(socket_manager)


@app.get("/")
def root():
    return JSONResponse({"message": "Hello, world!"})
