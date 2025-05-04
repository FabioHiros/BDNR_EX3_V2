from redis import Redis

class RedisRepository:

    def __init__(self,redis_connection: Redis) -> None:
        self.__redis_connection = redis_connection

    def insert(self,key: str,value: any ,ttl:int =None,keepttl:bool=False) -> None:
        self.__redis_connection.set(key,value,ttl,keepttl=keepttl)

    def insertHash(self,key: str,mapping: dict[str,any]) -> None:
        self.__redis_connection.hset(key,mapping= mapping)

    def getOne(self,key:str) -> any :
        return self.__redis_connection.get(key)

    def getHash(self,key:str,field:str) -> any:
        return self.__redis_connection.hget(key,field)
    
    def getAllHash(self,key:str) -> dict[str,any]:
        return self.__redis_connection.hgetall(key)

    def deleteOne(self,keys:list[str]) -> None:
        return self.__redis_connection.delete(*keys)

    def deleteFieldHash(self,key:str,fields:list[str]) -> None:
        self.__redis_connection.hdel(key,*fields)

    def getKeys(self,pattern:str) -> list[str]:
        return self.__redis_connection.keys(pattern)
    