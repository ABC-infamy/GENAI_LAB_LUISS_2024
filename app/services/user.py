from models.User import User, Transaction, Prediction
from datetime import datetime

def create_user(new_user, session) -> None:
    user_new = new_user
    session.add(user_new)
    session.commit()

def email_already_registered(email, session):
    our_user = session.query(User).filter(User.email == email).first()
    if our_user:
        return our_user
    return None

#and other balance related services.
def get_balance(id, session):
    our_user = session.query(User).filter(User.user_id == id).first()
    if our_user:
        return our_user.balance
    return None #user does nopt exits.

def modify_balance(id, amount, description_arg, session) -> str:
    our_user = session.query(User).filter(User.user_id == id).first()
    if our_user:
        transaction = Transaction(user_id=id, description=description_arg, credits = amount, date_time=datetime.now())
        add_transaction(transaction, session)
        our_user.balance += amount
        session.commit()
        return "Successfull transation"
    return "User not found"

def get_user_history(id, session) -> None:
    bal = session.query(Transaction).filter(Transaction.user_id == id).all()
    st = (f"User {id} transation history:")
    for el in bal:
        st+=(f"{el.description}, credits : {el.credits}, date and time of the transuaction {el.date_time}\n")
    return st

#Transactions

def add_transaction(transaction, session) -> None:
    session.add(transaction)
    session.commit()

#Model and predictions

def get_predictions_history(id, session) -> None:
    bal = session.query(Prediction).filter(Prediction.user_id == id).all()
    st = ""
    st+=(f"User {id} prediction history:")
    print(f"User {id} prediction history:")
    for el in bal:
        st+= (f"ID: {el.pred_id} input : {el.input}, output : {el.output} model version : {el.modelVersion} cost : {el.cost} date and time of the prediction made {el.date_time}\n")
    return st

def add_prediction(prediction, session) -> None:
    session.add(prediction)
    session.commit()
