from useCases.favorites.createFavorite import AddToFavoritesStrategy
from useCases.orders.deleteOrder import DeleteOrderStrategy
from useCases.favorites.updateFavorites import UpdateFavoritesStrategy
from useCases.orders.readOrder import ReadOrderStrategy
def FavoteMenu(db):
    while True:
        print("""
                ##### MENU De Favoritos #####
                    1- Criar Favoritos
                    2- Atualizar Favoritos

                    
        """)
        option = input("Digite a opção desejada? (V para voltar) ")

        match option:
            case '1':
                strategy = AddToFavoritesStrategy()
                product=strategy.create(db)

            case '2':
                strategy= UpdateFavoritesStrategy()
                strategy.update(db)
            case 'v':
                return