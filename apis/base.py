from apis.v1 import route_login
from apis.v1 import route_user
from apis.v1 import route_questions
from apis.v1 import route_subscribe
import send_emails 
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_user.router, prefix="", tags=["users"])
api_router.include_router(route_login.router, prefix="", tags=["login"])
api_router.include_router(route_questions.router, prefix="", tags=["questions"])
api_router.include_router(route_subscribe.router, prefix="", tags=["subscribe"])
api_router.include_router(send_emails.router, prefix="", tags=["email"])