from interfaces.delete import DeleteStrategy
from bson import ObjectId

class DeleteProductStrategy(DeleteStrategy):
    def delete(self, db) -> bool:
        print("\nDeletando produto")
        
      
        cpf_vendedor = input("Digite o CPF do vendedor: ")
        seller = db.usuarios.find_one({"cpf": cpf_vendedor})
        
        if not seller:
            print("Vendedor não encontrado!")
            return False
        
      
        if not seller.get("products") or len(seller.get("products")) == 0:
            print("Este vendedor não possui produtos cadastrados!")
            return False
        
     
        print("\nProdutos do vendedor:")
        for idx, prod in enumerate(seller.get("products"), 1):
            print(f"{idx}. {prod.get('nome')} - R$ {prod.get('valor')} - Estoque: {prod.get('estoque')}")
        
      
        try:
            produto_idx = int(input("\nDigite o número do produto que deseja deletar: ")) - 1
            if produto_idx < 0 or produto_idx >= len(seller.get("products")):
                print("Índice de produto inválido!")
                return False
        except ValueError:
            print("Entrada inválida!")
            return False
        
       
        produto_resumo = seller.get("products")[produto_idx]
        produto_id = produto_resumo.get("id")
        
     
        confirm = input(f"Tem certeza que deseja deletar o produto '{produto_resumo.get('nome')}'? (S/N): ")
        if confirm.upper() != 'S':
            print("Operação cancelada.")
            return False
        
       
        try:
            if isinstance(produto_id, str):
                produto_obj_id = ObjectId(produto_id)
            else:
                produto_obj_id = produto_id
                
           
            result = db.produtos.delete_one({"_id": produto_obj_id})
            
            if result.deleted_count == 0:
                print("Produto não encontrado na coleção de produtos!")
                
            
         
            db.usuarios.update_one(
                {"_id": seller.get("_id")},
                {"$pull": {"products": {"id": produto_id}}}
            )
            
            
            db.usuarios.update_many(
                {"favorites.id": produto_id},
                {"$pull": {"favorites": {"id": produto_id}}}
            )
            
            print("Produto deletado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao deletar produto: {e}")
            return False