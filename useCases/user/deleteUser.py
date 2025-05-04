from interfaces.delete import DeleteStrategy
from bson import ObjectId

class DeleteUserStrategy(DeleteStrategy):
    def delete(self, db) -> bool:
        cpf = input("Digite o cpf do usuário que deseja deletar (apenas números): ")
        
        
        user = db.usuarios.find_one({"cpf": cpf})
        
        if not user:
            print(f"Nenhum usuário encontrado com o CPF {cpf}")
            return False
            
        
        products = user.get("products", [])
        if products:
            print(f"Esse usuário possui {len(products)} produtos cadastrados.")
            confirm = input("Deletar o usuário e todos os seus produtos? (S/N): ")
            
            if confirm.upper() != 'S':
                print("Operação cancelada.")
                return False
                
            
            for product in products:
                product_id = product.get("id")
                try:
                    if isinstance(product_id, str):
                        product_obj_id = ObjectId(product_id)
                    else:
                        product_obj_id = product_id
                        
                    db.produtos.delete_one({"_id": product_obj_id})
                    
                  
                    db.usuarios.update_many(
                        {"favorites.id": product_id},
                        {"$pull": {"favorites": {"id": product_id}}}
                    )
                except Exception as e:
                    print(f"Erro ao deletar produto {product.get('nome')}: {e}")
            
            print(f"Todos os produtos do usuário foram deletados.")
        
      
        result = db.usuarios.delete_one({"cpf": cpf})
        
        if result.deleted_count > 0:
            print(f"Usuário com CPF {cpf} deletado com sucesso")
            return True
        else:
            print(f"Erro ao deletar usuário com CPF {cpf}")
            return False