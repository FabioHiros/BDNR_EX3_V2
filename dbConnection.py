from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from redis import Redis
uri = "mongodb+srv://fabiomatsumura:123456789Fatec@mercadolivre.as8bk7j.mongodb.net/?retryWrites=true&w=majority&appName=mercadolivre"

def connect_db():
   
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.mercadolivre
    return db

class RedisConnection:
    def __init__(self) -> None:
        self.__host = 'redis-10928.c17.us-east-1-4.ec2.redns.redis-cloud.com'
        self.__port = 10928
        self.__password='hq1yaTfwEHfYetZ31Uz3vMlytXS2rF5J'
        self.__username='default'

    def connect(self) -> Redis:
        self.__connection = Redis(
            host= self.__host,
            port= self.__port,
            password= self.__password,
            username= self.__username,
            decode_responses = True
        )
        return self.__connection


