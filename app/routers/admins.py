# from typing import List
# from fastapi import HTTPException, Request, Response, APIRouter

# from app.auth import check_admin_key
# from app.db import SessionDep


# router = APIRouter(prefix="/admin", tags=["Admin"])


# @router.post("/")
# async def auth_admin(db: SessionDep, request: Request):
#     admin_key = request.body.admin_key
#     user_id = request.cookies.get("user_id")
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Не авторизован")

#     if not check_admin_key(admin_key):
#         raise HTTPException(status_code=403, detail="Не админ")
    
    
#     return {'message': 'Вы стали админом'}