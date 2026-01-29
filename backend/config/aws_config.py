from dotenv import load_dotenv
load_dotenv()
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")