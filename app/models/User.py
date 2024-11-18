from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Prediction(SQLModel, table=True):
    pred_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.user_id")
    input: str
    output: str
    modelVersion: str
    cost: int
    date_time: datetime

class Transaction(SQLModel, table=True):
    transaction_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.user_id")
    description: str
    credits: int
    date_time: datetime

class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    balance: int = 0
    is_admin: int = 0