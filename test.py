from dbConnection import RedisConnection


redis= RedisConnection().connect()
# print(redis)

from redisRepository.redisRepo import RedisRepository
from useCases.login.login import Login
redisRepo = RedisRepository(redis)

# redisRepo.insert('teste','asdas')
# redisRepo.insert('teste','fabio1')

# redis.hset('test',items=['1',3])

# print(redis.get("teste"))
# redisRepo.insertHash('lolo',{'um':123,'2':'trovão'})
# redisRepo.insertHash('lolo',{'dois':1234})
# redisRepo.deleteFieldHash('lolo',['um'])
# print(redisRepo.getAllHash("lolo"))

# redisRepo.deleteOne(['teste'])

# print(redis.keys('product:*'))
from dbConnection import connect_db
login = Login(redis,connect_db())

login.createSession()

from useCases.sync.sync import Synchronize

a=Synchronize()
a.sync()