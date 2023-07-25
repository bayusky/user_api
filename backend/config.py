from dotenv import load_dotenv
import os
import redis
import pymongo

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    MONGO_CLIENT = pymongo.MongoClient(os.environ["MONGO_URI"])
    DB = MONGO_CLIENT['Users']
    
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")

class MailerConfig:
    SMTP_RELAY = os.environ["SMTP_RELAY"]
    SMTP_USER = os.environ["SMTP_USER"]
    SMTP_PORT = os.environ["SMTP_PORT"]
    SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
    #SMTP_ENCRYPTION = os.environ["SMTP_ENCRYPTION"]
    