# from menus.mainMenu import mainMenu
# while True:
#     mainMenu()
from dbConnection import connect_db, RedisConnection
from useCases.login.login import Login

redis= RedisConnection().connect()
login = Login(redis,connect_db())

login.createSession()