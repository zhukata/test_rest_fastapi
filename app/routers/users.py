from fastapi import HTTPException, Request, Response, APIRouter

from dependencies import SessionDep
from schemas import UserCreate, UserLogin, UserResponse
from repository import UserRepo


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
async def login(db: SessionDep, user: UserLogin, response: Response):
    """Авторизация через email/password"""
    check_user = await UserRepo.authenticate_user(db, user)
    if check_user is None:
        raise HTTPException(status_code=401,
                            detail='Неверная почта или пароль')

    response.set_cookie(key="user_id_from_cookie", value=str(check_user.id), expires=300, httponly=True)
    return {"message": "Успешный вход"}




@router.get("/me", response_model=UserResponse)
async def get_user(request: Request, db: SessionDep):
    user_id = request.cookies.get("user_id_from_cookie")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")

    db_user = await UserRepo.get_user_by_id(db, int(user_id))
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return UserResponse.model_validate(db_user)
