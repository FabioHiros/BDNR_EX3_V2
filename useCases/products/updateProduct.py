from interfaces.update import UpdateStrategy
from models.product import Product
from bson import ObjectId
import json
from redisRepository.redisRepo import RedisRepository
from dbConnection import RedisConnection
class UpdateProductStrategy(UpdateStrategy):
    def __init__(self):
        self.redis_db= RedisRepository(RedisConnection().connect())


    def update(self, db):
        print("\nAtualizando produto")
        
      
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
            produto_idx = int(input("\nDigite o número do produto que deseja atualizar: ")) - 1
            if produto_idx < 0 or produto_idx >= len(seller.get("products")):
                print("Índice de produto inválido!")
                return False
        except ValueError:
            print("Entrada inválida!")
            return False
        
        
        produto_resumo = seller.get("products")[produto_idx]
        produto_id = produto_resumo.get("id")
        
       
        try:
            if isinstance(produto_id, str):
                produto_obj_id = ObjectId(produto_id)
            else:
                produto_obj_id = produto_id
                
            produto = db.produtos.find_one({"_id": produto_obj_id})
            id =type(str( produto['_id']))
            print(id)
            if not produto:
                print("Produto não encontrado na coleção de produtos!")
                return False
        except Exception as e:
            print(f"Erro ao buscar produto: {e}")
            return False
        
 
        print("\nDados atuais do produto:")
        print(f"Nome: {produto.get('nome')}")
        print(f"Descrição: {produto.get('descricao')}")
        print(f"Marca: {produto.get('marca')}")
        print(f"Valor: R$ {produto.get('valor'):.2f}")
        print(f"Estoque: {produto.get('estoque')}")
        
      
        print("\nDeixe em branco para manter o valor atual")
        
        novo_nome = input("Novo nome: ")
        if len(novo_nome):
            produto["nome"] = novo_nome
            
        nova_descricao = input("Nova descrição: ")
        if len(nova_descricao):
            produto["descricao"] = nova_descricao
            
        nova_marca = input("Nova marca: ")
        if len(nova_marca):
            produto["marca"] = nova_marca
        
        novo_valor_str = input("Novo valor (R$): ")
        if len(novo_valor_str):
            try:
                produto["valor"] = float(novo_valor_str)
            except ValueError:
                print("Valor inválido, mantendo valor atual")
        
        novo_estoque_str = input("Novo estoque: ")
        if len(novo_estoque_str):
            try:
                produto["estoque"] = int(novo_estoque_str)
            except ValueError:
                print("Estoque inválido, mantendo valor atual")
        

        del produto['_id']
        self.redis_db.insert(f'product:{str(produto_obj_id)}',json.dumps(produto))

        # db.produtos.update_one({"_id": produto_obj_id}, {"$set": produto})
        
       
        # db.usuarios.update_one(
        #     {"_id": seller.get("_id"), "products.id": produto_id},
        #     {
        #         "$set": {
        #             "products.$.nome": produto.get("nome"),
        #             "products.$.valor": produto.get("valor"),
        #             "products.$.estoque": produto.get("estoque")
        #         }
        #     }
        # )
        
        print("Produto atualizado com sucesso! \npara concretizar as alterações sincronize com o mongo")
        