from menus.userMenu import userMenu
from dbConnection import connect_db
from menus.productMenu import productMenu
from menus.ordersMenu import OrderMenu
from menus.favoriteMenu import FavoteMenu
from useCases.sync.sync import Synchronize
def mainMenu():
    db = connect_db()
    x = Synchronize()
    while (True):
        print("""
                ##### Menu Principal #####
                    1- CRUD Usuário
                    2- CRUD Compras
                    3- CRUD Produto
                    4- CRUD Favoritos
                    5- Sincronizar com Mongodb
            """)
        option = input('Digite a  opção desejada (S para sair):  ')

        match option:
            case '1':
                userMenu(db)
            case '3':
                productMenu(db)
            case '2':
                OrderMenu(db)
            case '4':
                FavoteMenu(db)
            case '5':
                x.sync()
            case 's':
                return

