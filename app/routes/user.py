from typing import List
from models import Model
from fastapi import HTTPException, Depends, status, APIRouter
from services import user
from database.database import get_session
from models.User import Prediction, Transaction, User
from pydantic import BaseModel
from datetime import datetime
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from services.logging.logging import get_logger

logger = get_logger(logger_name=__name__)

user_route = APIRouter(tags=['User'])

class RegisterInfo(BaseModel):
    email: str
    username: str
    password: str

@user_route.post('/register')
async def register(data: RegisterInfo, session = Depends(get_session)):
	if user.email_already_registered(data.email, session):
		logger.warning("User exists")
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

	user.create_user(User(username = data.username, email = data.email, password = HashPassword().create_hash(data.password), balance = 0, is_admin = 0), session)
	return {"message": "User successfully registered!"}

@user_route.post('/login')
async def login(data: RegisterInfo, session = Depends(get_session)):
	temp_user = user.email_already_registered(data.email, session)
	if temp_user is None:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not found, register")

	if HashPassword().verify_password(data.password, temp_user.password):
		token = create_access_token({"email":temp_user.email,"username":temp_user.username,"user_id":temp_user.user_id,"is_admin":temp_user.is_admin,"exp":datetime.now()})
		return {"access_token": token , "token_type":"Bearer"}
	logger.warning("Wrong password")
	raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")



@user_route.get('/balance/{user_id}')
async def balance_check(id: int, session=Depends(get_session)):
	bal = user.get_balance(id, session)
	if bal is None:
		logger.warning("User not found")
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not found")
	else:
		return bal

class Baldata(BaseModel):
	user_id:int
	amount:int
	description_arg:str

@user_route.post('/balance')
async def balance_change(data: Baldata, session=Depends(get_session)):
	bal = user.modify_balance(data.user_id, data.amount, data.description_arg, session)
	if bal == "User not found":
		logger.warning("User not found")
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return "Balance was changed successfully"


class PredData(BaseModel):
	user_id:int
	amount:int
	description_arg:str
	version:str
	data2:str

@user_route.post('/predict')
async def make_prediction(data: PredData, session=Depends(get_session)):
	#(user.get_balance(data.user_id, session) >= 5)
	if (user.get_balance(data.user_id, session) >= 5): #if user has money
		test_model = Model.Model(data.version)
		if (test_model.validate(data.data2)): #if model works
			user.modify_balance(id = data.user_id , amount = -5 , description_arg = "User payed for model use", session = get_session()) #datetime added in other place
			user.add_prediction(Prediction(user_id = data.user_id, input = data.data2, output = test_model.predict(data.data2), modelVersion = test_model.get_version(), cost = 5, date_time = datetime.now()), session = get_session())
			return "Prediction is made"
		logger.warning("Invalid input, failed model validation!")
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")
	logger.warning("Insufficient funds, balance MONEY")
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds, balance MONEY")

@user_route.get('/predictions/{user_id}')
async def get_predictions_history(id: int, session=Depends(get_session)):
	bal = user.get_balance(id = id, session =session)
	if bal == "User not found":
		logger.warning("User not found")
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	return user.get_predictions_history(id = id, session =session)

@user_route.get('/transactions/{user_id}')
async def get_predictions_history(id: int, session=Depends(get_session)):
	bal = user.get_balance(id = id, session =session)
	if bal == "User not found":
		logger.warning("User not found")
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	return user.get_user_history(id = id, session =session)

