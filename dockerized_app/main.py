from typing import List
from fastapi import FastAPI
from prometheus_client import start_http_server, Counter, generate_latest
from starlette.responses import Response

from app import services
from app.schema import UserIn, BaseResponse, UserListOut

app = FastAPI()

# Define a Counter metric
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')

@app.get("/")
async def index():
    """
    Index route for our application
    """
    return {"message": "Hello from FastAPI ;)"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


@app.post("/users", response_model=BaseResponse)
async def user_create(user: UserIn):
    """
    Add user data to json file
    """
    try:
        services.add_userdata(user.dict())
    except:
        return {"success": False}
    return {"success": True}


@app.get("/users", response_model=UserListOut)
async def get_users():
    """
    Read user data from json file
    """
    return services.read_usersdata()
