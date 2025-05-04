from interfaces.create import CreateStrategy
from models.product import Product

class CreateProductStrategy(CreateStrategy):
    def create(self, db) -> Product:
        print("\nCriando novo produto")
        
       
        cpf = input("CPF do vendedor: ")
        seller = db.usuarios.find_one({"cpf": cpf})
        
        if not seller:
            print("Vendedor não encontrado com este CPF.")
            return None
            
       
        if not seller.get("isSeller", False):
            print("Este usuário não está registrado como vendedor.")
            print("Apenas vendedores podem criar produtos.")
            return None
            
        idSeller = str(seller.get('_id'))
        
       
        name = input("Nome do produto: ")
        description = input("Descrição: ")
        brand = input("Marca: ")
        
       
        price = self._get_float_input("Valor (R$): ")
        stock = self._get_int_input("Quantidade em estoque: ")
        rating = 0.0 
        

        product = Product(name, idSeller, description, brand, price, stock, rating)
        
        product_dict = {
            "nome": product.name,
            "idVendedor": product.idSeller,
            "descricao": product.description,
            "marca": product.brand,
            "valor": product.price,
            "estoque": product.stock,
            "avaliacao": product.rating
        }
        
 
        result = db.produtos.insert_one(product_dict)
        product_id = result.inserted_id
        print(f"Produto criado com ID: {product_id}")

      
        product_summary = {
            "id": str(product_id),
            "nome": product.name,
            "valor": product.price,
            "estoque": product.stock
        }
        
     
        if "products" not in seller:
            
            db.usuarios.update_one(
                {"_id": seller.get("_id")},
                {"$set": {"products": [product_summary]}}
            )
        else:
           
            db.usuarios.update_one(
                {"_id": seller.get("_id")},
                {"$push": {"products": product_summary}}
            )
            
        print(f"Produto adicionado à lista de produtos do vendedor")
        return product
    
    def _get_float_input(self, prompt):
       
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Por favor, digite um valor numérico válido.")
    
    def _get_int_input(self, prompt):
        
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Por favor, digite um número inteiro válido.")