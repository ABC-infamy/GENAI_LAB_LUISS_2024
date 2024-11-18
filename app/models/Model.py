import joblib
import os
import pandas as pd
import numpy as np
import sklearn
from openai import OpenAI
from dotenv import load_dotenv
import google.generativeai as genai
import json

class Model:
    def __init__(self, version):
        self.version = version
        self.model_path = os.path.join(os.getcwd(),"models","model_v"+self.version+".joblib")

    def transform(self,user_data):
        return True

    def validate(self,user_data):
        return True
        """if (transform(user_data)):
                                    return True TBD
                                else:
                                    return False"""

    def predict(self,user_data):
        loaded_model = joblib.load(self.model_path)
        user_data = pd.read_json(user_data, orient="split")
        if (self.version == "1"):
            prediction = loaded_model.predict(user_data)
            y_pred = prediction
            y_pred = y_pred[0] #propensity to addiction.

            """
            IMPORTANT
            (-inf,0] - No addiction risks detected by our model
            (0,10) - Neglibible addiction risks
            [10,25) - Minor addiction risks
            [25,100) - Some addiction risks
            [100,1000) - Strong addiction risks
            [1000,inf] - Catastrophic addiction
            """

            try:
                with open("config.json", "r") as f:
                    config = json.load(f)

                #api_key = config["openai_api_key"]

                #openai.api_key = os.getenv('CHAT_GPT_API_KEY')

                addiction_level = ""

                if (y_pred <= 0):
                    addiction_level = "No Addiction"
                elif 0 < y_pred < 10:
                    addiction_level = "Small Addiction"
                elif 10 <= y_pred < 25:
                    addiction_level = "Moderate Addiction"
                elif 25 <= y_pred < 100:
                    addiction_level = "Strong Addiction"
                elif 100 <= y_pred < 1000:
                    addiction_level = "Very Strong Addiction"
                else:
                    addiction_level = "Catastrophic Addiction"

                prompt = f"The User has a {addiction_level} to video games. Please generate an advise to help the user reduce video game schedule. If the addiction level is small just talk about small things like reducing gaming hours. If addiction is medium refer to hobies and physical activity options. If strong advice on how to seek therapy and how to ask for help. Be polite and detailed."

                """
                client = OpenAI(api_key = api_key)
                
                #I wanted to use chat GPT api first, but since I do not have paid version I had to resort to diffrent api.

                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"{prompt}",
                        }
                    ],
                    model="gpt-3.5-turbo",
                )

                return response.choices[0].text.strip()
                """
                with open('config.json') as f:
                    config = json.load(f)

                api_key = config.get("API_KEY_2")
                genai.configure(api_key=api_key)

                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                return response.text

            except Exception as e:
                #print(e)
                if y_pred <= 0:
                    return "GEN AI Model is not avaliable, but based on Linear Regression ML model you have a Noaddiction to video games. No reccomendations. For a clearer picture and better reccomendations retry again later when connection with GENAI model would resume. Sorry for the incovenience."
                elif 0 < y_pred < 10:
                    return "GEN AI Model is not avaliable, but based on Linear Regression ML model you have a Neglignle addiction to video games. Everything is fine, no need to change the schedule. Just do not play more. For a clearer picture and better reccomendations retry again later when connection with GENAI model would resume. Sorry for the incovenience."
                elif 10 <= y_pred < 25:
                    return f"{e},GEN AI Model is not avaliable, but based on Linear Regression ML model you have a Small addiction to video games. You might have a small addication, try reducing gaming times, nothing critical though. For a clearer picture and better reccomendations retry again later when connection with GENAI model would resume. Sorry for the incovenience."
                elif 25 <= y_pred < 100:
                    return "GEN AI Model is not avaliable, but based on Linear Regression ML model you have a Moderate addiction to video games. You have an addiction, which you should defenetely put under controll. Impose a harsh gaming time schedule on yourself and do not go beyond the threthold. No more then 2 hours per day. For a clearer picture and better reccomendations retry again later when connection with GENAI model would resume. Sorry for the incovenience."
                elif 100 <= y_pred < 1000:
                    return "GEN AI Model is not avaliable, but based on Linear Regression ML model you have a Strong addiction to video games. You have a very strong addiction. You should gradually reduce gaming times and reduce shop spendings. For a clearer picture and better reccomendations retry again later when connection with GENAI model would resume. Sorry for the incovenience."
                else:
                    return "GEN AI Model is not avaliable, but based on Linear Regression ML model you have a Catastrophic addiction to video games. It is so bad, that our model would not be able to help you :(. Better call a Doctor or Relatives and seek some serious help, since you alone would most likely fail to overcome it. For a clearer picture and better reccomendations retry again later when connection with GENAI model would resume. Sorry for the incovenience."
                return f"Model not avaliable."

        else:
            pass
    
    def __str__(self):
        return f"version = {self.version}"

    def get_version(self):
        return self.version