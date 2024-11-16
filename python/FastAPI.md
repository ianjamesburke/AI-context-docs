# FastAPI Initialization

```python
from fastapi import FastAPI

app = FastAPI()

app = FastAPI(
    debug=False,
    title="FastAPI",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Basic Example
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

 

@app.put("/items/{item_id}")
def replace_item(item_id: str, item: Item):
    return {"message": "Item replaced", "id": item_id}

# WebSocket Example
from fastapi import FastAPI, WebSocket

 

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

# Including Routers
from fastapi import FastAPI
from .users import users_router

 
app.include_router(users_router)

# Middleware Example
import time
from fastapi import FastAPI, Request

 

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception Handling
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

 

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(status_code=418, content={"message": f"Oops! {exc.name} caused an issue."})

# File Uploads
from fastapi import FastAPI, File, UploadFile

 

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# Serving Static Files
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

 
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templating with Jinja2
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

# Testing with TestClient
from fastapi import FastAPI
from fastapi.testclient import TestClient

 

@app.get("/items/")
def read_items():
    return [{"name": "Item1"}]

client = TestClient(app)
response = client.get("/items/")
```

# dependecy injection
```python
from fastapi import FastAPI, Depends

 

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```
# Background Tasks
```python
from fastapi import FastAPI, BackgroundTasks



def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent"}
```

# Security - OAuth2 with Password (and hashing), Bearer with JWT tokens
```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d1b5e5e5e5e5e5...."


