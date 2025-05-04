from interfaces.update import UpdateStrategy
from bson import ObjectId

class UpdateFavoritesStrategy(UpdateStrategy):
    def update(self, db) -> bool:
        print("\nGerenciar favoritos")
        
        
        user_cpf = input("Digite o CPF do usuário: ")
        user = db.usuarios.find_one({"cpf": user_cpf})
        
        if not user:
            print("Usuário não encontrado!")
            return False
        
        
        favorites = user.get("favorites", [])
        if not favorites:
            print("O usuário não possui favoritos!")
            option = input("Deseja adicionar um produto aos favoritos? (S/N): ")
            if option.lower() == 's':
                
                from useCases.favorites.createFavorite import AddToFavoritesStrategy
                create_strategy = AddToFavoritesStrategy()
                return create_strategy.create(db)
            return False
        
        
        print("\nFavoritos atuais:")
        for idx, fav in enumerate(favorites, 1):
            print(f"{idx}. {fav.get('nome')} - R$ {fav.get('valor'):.2f}")
        
        
        print("\nO que deseja fazer?")
        print("1. Remover um item dos favoritos")
        print("2. Adicionar novo favorito")
        print("V. Voltar")
        
        option = input("Escolha uma opção: ")
        
        if option == "1":
            return self._remove_favorite(db, user, favorites)
        elif option == "2":
            from useCases.favorites.createFavorite import AddToFavoritesStrategy
            create_strategy = AddToFavoritesStrategy()
            return create_strategy.create(db)
        else:
            print("Operação cancelada.")
            return False
    
    def _remove_favorite(self, db, user, favorites):
        
        try:
            fav_idx = int(input("\nDigite o número do item a ser removido: ")) - 1
            if 0 <= fav_idx < len(favorites):
                removed_item = favorites[fav_idx]
                
                
                db.usuarios.update_one(
                    {"_id": user.get("_id")},
                    {"$pull": {"favorites": {"id": removed_item.get("id")}}}
                )
                
                print(f"Item '{removed_item.get('nome')}' removido dos favoritos!")
                return True
            else:
                print("Índice inválido!")
                return False
        except ValueError:
            print("Entrada inválida!")
            return False
    
    
        return updates_made