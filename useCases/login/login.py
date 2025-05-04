from redis import Redis
from dbConnection import connect_db
from pymongo.mongo_client import MongoClient
from redisRepository.redisRepo import RedisRepository
from menus.mainMenu import mainMenu
import json
class Login:

    def __init__(self,redis_connection: Redis,mongo) -> None:
        self.__redis_db = RedisRepository(redis_connection)
        self.__mongo_db= mongo
        self.__redis = RedisRepository(redis_connection)

    def createSession(self):
    
        cpf = input('Digite seu cpf: ')
    
        query= {'cpf':cpf}
        user = self.__mongo_db.usuarios.find_one(query)

        if not user:
            print('Usuário não encontrado!')
            return
        
        isLoggedin=self.__redis.getOne(cpf)
        if isLoggedin:

            self.__redis_db.insert(cpf,json.dumps(user.get('favorites')),120)
            mainMenu()
            return

        password = input('Digite sua senha: ')

        isPasswordCorrect= user.get('senha','N/A') == password
        
        if not isPasswordCorrect: 
            print('Senha Incorreta!')
            return

        self.__redis_db.insert(user.get('cpf'),json.dumps(user.get('favorites')),120)

        mainMenu()