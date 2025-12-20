from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import *
import uvicorn
from datetime import datetime

app = FastAPI(
    title="API Learning",
    description="API description",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=True
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
    )
# Handle browser favicon request
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/images/favicon.ico")

class User(BaseModel):
    name: str = Field(alias='username',description='Enter user name')
    age: int = Field(default=18)
    tel: Optional[int]= None

class APIResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates success or failure"
        )
    message: str = Field(
        ...,
        description="Human readable message"
        )
    data: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Send data if clint Request"
        )
    errors: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Validation or business errors"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response time (UTC)"
    )
class GreetResponse(APIResponse):
    pass


@app.post("/greet", response_model=GreetResponse)
def greet(user: User):
    return {"success":True,"message":f"Namaste {user.name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)
