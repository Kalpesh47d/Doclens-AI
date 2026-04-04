from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# print(API_KEY)

# import os
# print(os.getenv("HF_HOME"))