import requests
import streamlit as st
from auth.jwt_handler import verify_access_token
from datetime import datetime, timedelta
import extra_streamlit_components as stx
import streamlit.components.v1 as components
import pandas as pd

API_URL = "http://app:8080"

def get_cookie_manager():
    return stx.CookieManager()
cookie_manager = get_cookie_manager()

def set_token(token):
    st.session_state.token = token
    st.session_state.token_expiry = datetime.now() + timedelta(minutes=20)
    cookie_manager.set("token", token, expires_at=st.session_state.token_expiry)
def get_token():
    return st.session_state.token
def remove_token():
    st.session_state.token = None
    st.session_state.token_expiry = None

# Login page
def login_page():
    add_custom_css()
    st.markdown('<h1 class="main-title">Log in into user area</h1>', unsafe_allow_html=True)
    email = st.text_input("Email", key="login_email")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Log in")
    back1_button = st.button("Back to menu")

    if login_button:
        url = f'{API_URL}/user/login/'
        payload = {"email": email, "username": username, "password": password}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            res = response.json()
            token = res.get("access_token")
            user_id = res.get("user_id")
            set_token(token)
            st.session_state.admin = verify_access_token(token)["is_admin"]
            st.session_state.logged = True
            st.session_state.username = verify_access_token(token)["username"]
            st.session_state.user_id = verify_access_token(token)["user_id"]
            st.session_state.current_page = "dashboard"
            st.rerun()
        else:
            st.error("Error logging in")

    if back1_button:
        st.session_state.current_page = "menu"
        st.rerun()

#Register page
def register_page():
    add_custom_css()
    st.markdown('<h1 class="main-title">Register</h1>', unsafe_allow_html=True)
    username = st.text_input("Name", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    reg_button = st.button("Register")
    back1_button = st.button("Back to menu")

    if reg_button:
        url = f'{API_URL}/user/register/'
        payload = {"email": email, "username": username, "password": password}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            st.success("Registered successfully")
            st.session_state.current_page = "login"
            st.rerun()
        else:
            st.error("Registration error :(")

    if back1_button:
        st.session_state.current_page = "menu"
        st.rerun()

#Dashboard
def dashboard_page():
    add_custom_css()

    if (st.session_state.username == ""):
        return

    st.markdown('<h1 class="main-title">Personal account</h1>', unsafe_allow_html=True)

    st.markdown('<p class="welcome-text">Welcome. You have successfully logged into your account. Here you can acquire credits, or spend them on generating a plan. We offer a web service for users and an API service for mass requests. Here you can also view the history of your transactions and predictions. There is moderation present on the website, they will prevent fraud and are able to view all users accounts. The reccomendations for users are saved in our database</p>', unsafe_allow_html=True)

    url = f'http://app:8080/user/balance/{st.session_state.user_id}?id={st.session_state.user_id}'
    response = requests.get(url)

    if response.status_code == 200:
        balance = response.json()
        st.write(f"Your balance: {balance} credits")
    else:
        st.write("Balance error, could not retrieve data")

    st.subheader("Add credits")
    amount = st.number_input("Add x credits") #We do not use html for input windows, due to the security risks.

    if st.button("Add credits"):
        if (amount <= 0):
            st.error("You must only deposit positive amounts")
            return
        url = 'http://app:8080/user/balance/'
        payload = {
          "user_id": st.session_state.user_id,
          "amount": amount,
           "description_arg": "User deposited credits"
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            st.success("Balance updated successfullys")
            st.rerun()
        else:
            st.error("Error. The credits were not added, sorry.")

    st.subheader("Reccomendations")
    input_data = st.file_uploader("Add file with user data", type=["csv"])
    model_ver = st.text_input("Select model to use")
    if (model_ver != "1"):
        st.error(f"This model version does not exist. Use v1 for now")

    if st.button("Make predictions and reccomendations"):
        url = 'http://app:8080/user/predict/'
        df = pd.read_csv(input_data)
        payload = {
            "user_id": st.session_state.user_id,
            "amount": "5",
            "description_arg": "prediction",
            "data2": df.to_json(orient="split"),
            "version":model_ver
        }
        response = requests.post(url, json=payload)
        if  response.status_code == 200:
            result = response.json()
            st.success("prediction complete")
            st.write(f"Result: {result}")
        else:
            damn_it_why_error = f"Error {response.status_code}: {response.reason}"
            st.error(f"Unknown error :(\n{damn_it_why_error}")

    st.subheader("View generated reccomendations")
    if st.button("View"):
        url = f'http://app:8080/user/predictions/{st.session_state.user_id}?id={st.session_state.user_id}'
        response = requests.get(url)
        if response.status_code == 200:
            history = response.json()
            st.write(history)
        else:
            st.error("Error fetching history")

    st.subheader("Transaction history")
    if st.button("View transactions"):
        url = f'http://app:8080/user/transactions/{st.session_state.user_id}?id={st.session_state.user_id}'
        response = requests.get(url)
        if response.status_code == 200:
            history = response.json()
            st.write(history)
        else:
            st.error("Error fetching history")
    
    if (st.session_state.admin == 1):
        st.subheader("Secret admin page")
        st.subheader("View transactions of other users ;)")
        user_id_search = st.text_input("Enter User ID")
        if (st.button("View by id")):
            url = f'http://app:8080/user/transactions/{user_id_search}?id={user_id_search}'
            response = requests.get(url)
            if response.status_code == 200:
                history = response.json()
                st.write(history)
            else:
                st.error("Error")

        st.subheader("Modify user's balance :O")
        user_id_balance = st.text_input("ID")  
        user_add_amount = st.text_input("Credits")
        if (st.button("Append user balance")):
            if (int(user_add_amount) <= 0):
                st.error("Add > 0")
                return
            url = 'http://app:8080/user/balance/'
            payload = {
            "user_id": user_id_balance,
            "amount": user_add_amount,
            "description_arg": "success"
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.success("success")
                st.rerun()
            else:
                st.error("Error we could not update your balance")


def add_custom_css():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #6DD5FA 0%, #2986cc 100%);
                font-family: 'Arial', sans-serif;
            }
            /* Main style */
            .main-title {
                font-size: 3rem;
                color: white;
                text-align: center;
                font-weight: bold;
            }
            /* Style for general text */
            .welcome-text {
                font-size: 1.5rem;
                color: white;
                text-align: center;
            }
            /* Buttons */
            .stButton > button {
                border: none;
                color: white;
                background-color: #5e9d60;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                transition: background-color 0.3s ease, transform 0.3s ease;
            }
            /* Button selection effectss */
            .stButton > button:hover {
                background-color: #45a049;
                transform: translateY(-3px);
            }
            /* Website intro images, hosted on igmur */
            .backkground-container {
                width: 100%;
                overflow: hidden;
                position: relative;
            }

            .backkground {
                display: flex;  
                flex-wrap: nowrap;  
                justify-content: start;
            }

            .backkground img {
                width: 20%; 
                transition: all 0.5s ease;
                opacity: 0.5;
                transform: scale(0.8); 
            }

            .backkground img.center {
                opacity: 1;
                transform: scale(1);
            }
        </style>
    """, unsafe_allow_html=True)

def add_custom_css2():
    #Background 2 TBD
    pass

# Main page
def main_page():
    add_custom_css()

    st.markdown('<h1 class="main-title">Main menu</h1>', unsafe_allow_html=True)

    st.markdown('<p class="welcome-text">Dear gamer, welcome to our ML servince which aims to help you detect and fight gaming addiction. Our model based on your data will try to understand whether you need help fighting with the addiction, or not. If so we will try to determine what exactly should your steps be.</p>', unsafe_allow_html=True)

    if not st.session_state.logged:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Log in"):
                st.session_state.current_page = "login"
                st.rerun()
        with col2:
            if st.button("Register"):
                st.session_state.current_page = "register"
                st.rerun()

    #images hosted on imgur
    carousel_html = """
    <div class="backkground-container">
        <div class="backkground">
            <img src="https://imgur.com/uhDuFnn.png" alt="img1">
            <img src="https://imgur.com/hciCKd5.png" alt="img2">
            <img src="https://imgur.com/Y37ktNP.png" alt="img3">
            <img src="https://imgur.com/NY6VqDe.png" alt="img4">
            <img src="https://imgur.com/uhDuFnn.png" alt="img5">
        </div>
    </div>

    <script>
      const backside = document.querySelector('.backkground');
      const images = document.querySelectorAll('.backkground img');

      const totalImages = images.length;
      let index = 0;
      const speed = 2000;

      function moveImages() {
        index = (index + 2) % totalImages;

        images.forEach((image, i) => {
          const center_position = (i - index + totalImages) % totalImages; 
          if (center_position === 0) {
            image.classList.add('center');
            image.style.opacity = '0.99'; 
            image.style.transform = 'scale(0.9)'; 
          } else {
            image.classList.remove('center');
            image.style.opacity = '0.49'; 
            image.style.transform = 'scale(0.7)';
          }
        }
        );

        if (index === totalImages - 1) {

          setTimeout(() => {
            backside.style.transition = 'none';

            backside.style.transform = 'translateX(0)';

            setTimeout(() => { backside.style.transition = 'transform 0.5s ease'; });}, speed);

        }
      }

      moveImages();
      setInterval(moveImages, speed);

    </script>
    """

    # Render the HTML
    components.html(carousel_html, height=350)


def initialize_session_state():
    if 'logged' not in st.session_state:
        st.session_state.logged = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "menu"
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'token' not in st.session_state:
        st.session_state.token = None
        st.session_state.token_expiry = None
    if 'admin' not in st.session_state:
        st.session_state.admin = 0

def main():
    initialize_session_state()

    token = get_token()

    if token:
        try:
            decoded_token = verify_access_token(token)
            if decoded_token:
                st.session_state.logged = True
                st.session_state.username = verify_access_token(token)["email"]
                st.session_state.user_id = verify_access_token(token)["user_id"]
                st.sidebar.write("Guide")
                st.sidebar.write(f"You are logged in as {st.session_state.username}!")

                st.sidebar.write("Working with balance")
                st.sidebar.write("To place money on you balance just enter the needed sum into the respective window and press add credits. This will give your credits which are the currency on this website, using them you can request the personal analysis of you profile to be done.")

                st.sidebar.write("Working with the model")
                st.sidebar.write("To use the model you must have >=5 credits on your balance.")
                st.sidebar.write("First our machine learniong model will access your profile and assign you to one of many categories, then we will generate a personal text of a reccomendation.")
                st.sidebar.write("For the service to work you will neeed to provide us all the data about your steam account.")
                
                st.sidebar.write("View results")
                st.sidebar.write("Allows to view all reccomendations")

                st.sidebar.write("View transactions")
                st.sidebar.write("See the history of your spendings and deposits.")
            else:
                print("Bad token")
                raise ValueError("Invalid token")

        except Exception as e:
            #print("auth error")
            st.error(f"Error logging in: {e}")
            remove_token()
            st.session_state.logged = False
    else:
        st.session_state.logged = False

    if st.session_state.logged:
        pages = {
            "menu": main_page,
            "dashboard": dashboard_page,
        }
        logout_button = st.button("Log out")
        if logout_button:
            remove_token()
            st.session_state.logged = False
            st.session_state.username = ""
            st.session_state.user_id = None
            st.session_state.current_page = "menu"
            st.rerun()
    else:
        pages = {"menu": main_page, "login": login_page, "register": register_page}

    if st.session_state.current_page in pages:
        pages[st.session_state.current_page]()


if __name__ == "__main__":
    main()
