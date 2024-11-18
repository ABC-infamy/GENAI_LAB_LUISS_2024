import requests
import pytest
from contextlib import nullcontext as does_not_raise
#When testing TestUser do not forget to clear the databse before testing (restart api.py), otherwise you would not be able to aderquately check TestUser
class TestUser: 
  #Testing registering user and Testing registering user, but data is incorrect, as we are trying to register a new user with data oif already regisntered one.
  @pytest.mark.parametrize(
      "x,y,z,expectation,expected_status",
      [
        ("user@gmail.com","example_user","12345",does_not_raise(),200),
        ("user@gmail.com","example_user","123457",pytest.raises(requests.exceptions.HTTPError),409),
        ("user@gmail.com","example_user_2","123457",pytest.raises(requests.exceptions.HTTPError),409),
      ]
  )
  
  def test_register(self,x,y,z,expectation,expected_status):
    url = 'http://0.0.0.0:8080/user/register/'
    payload = {"email":x,"username":y,"password":z}
    response = requests.post(url, json=payload)
    with expectation:
        if response.status_code != 200:
            assert response.status_code == expected_status
            response.raise_for_status()
        else:
            assert response.status_code == 200

  #Testing login, 1.Login as existing user 2.Login as non existing user 3.Login as existing user, wrong password
  @pytest.mark.parametrize(
      "x,y,z,expectation,expected_status",
      [
        ("user@gmail.com","example_user","12345",does_not_raise(),200),
        ("userx@gmail.com","example_userx","12345",pytest.raises(requests.exceptions.HTTPError),409),
        ("user@gmail.com","example_user_2","123457",pytest.raises(requests.exceptions.HTTPError),403),
      ]
  )
  def test_login(self,x,y,z,expectation,expected_status):
    url = 'http://0.0.0.0:8080/user/login/'
    payload = {"email":x,"username":y,"password":z}
    response = requests.post(url, json=payload)
    with expectation:
        if response.status_code != 200:
            assert response.status_code == expected_status
            response.raise_for_status()
        else:
            assert response.status_code == 200

#run register test before it, so there are users in the database to begin with.
class TestBalance:
  #testing view balance 1.valid_id 2.invalid id
  @pytest.mark.parametrize(
      "x,expectation,expected_status",
      [
        ("1",does_not_raise(),200),
        ("100",pytest.raises(requests.exceptions.HTTPError),409)
      ]
  )
  def test_view_balance(self,x,expectation,expected_status):
    url = f'http://0.0.0.0:8080/user/balance/{x}?id={x}'
    response = requests.get(url)
    with expectation:
        if response.status_code != 200:
            assert response.status_code == expected_status
            response.raise_for_status()
        else:
            assert response.status_code == 200

  #1.Tesing valid add balance, 2.Test non existing user id 3.Testing transaction
  @pytest.mark.parametrize(
      "x,y,z,expectation,expected_status",
      [
        ("1","105","test add money",does_not_raise(),200),
        ("100","10","test add money",pytest.raises(requests.exceptions.HTTPError),404),
        ("1","-100","test remove money",does_not_raise(),200),
      ]
  )
  def test_change_balance(self,x,y,z,expectation,expected_status):
    url = 'http://0.0.0.0:8080/user/balance/'
    payload = {"user_id":x,"amount":y,"description_arg":z}
    response = requests.post(url, json=payload)
    with expectation:
        if response.status_code != 200:
            assert response.status_code == expected_status
            response.raise_for_status()
        else:
            assert response.status_code == 200

class TestModel:
  #testing view predoction history 1.valid_id 2.invalid id
  @pytest.mark.parametrize(
      "x,expectation,expected_status",
      [
        ("1",does_not_raise(),200),
        ("100d",pytest.raises(requests.exceptions.HTTPError),422)
      ]
  )
  def test_prediction_viewin(self,x,expectation,expected_status):
    url = f'http://0.0.0.0:8080/user/predictions/{x}?id={x}'
    response = requests.get(url)
    with expectation:
        if response.status_code != 200:
            assert response.status_code == expected_status
            response.raise_for_status()
        else:
            assert response.status_code == 200
  
  #1.Valid user, Valid prediction. 2.Invalid User 3.Invalid prediction data
  @pytest.mark.parametrize(
      "x,y,z,a,b,expectation,expected_status",
      [
        ("1","5","testing making prediction","4.3|3.2|1.4|0.1","1",does_not_raise(),200),
        ("100d","5","testing making prediction","4.3|3.2|1.4|0.1","1",pytest.raises(requests.exceptions.HTTPError),422),
        ("1","5","testing making prediction","meme","1",pytest.raises(requests.exceptions.HTTPError),400)
      ]
  )
  def test_prediction_making(self,x,y,z,a,b,expectation, expected_status):
    url = 'http://0.0.0.0:8080/user/predict/'
    payload = {"user_id":x,"amount":y,"description_arg":z, "data2":a,"version":b}
    response = requests.post(url, json=payload)
    with expectation:
        if response.status_code != 200:
            assert response.status_code == expected_status
            response.raise_for_status()
        else:
            assert response.status_code == 200