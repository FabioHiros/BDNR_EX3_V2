from interfaces.read import ReadStrategy
from bson import ObjectId

class ReadProductStrategy(ReadStrategy):
    def read(self, db) -> None:
        
        search_option = input("Buscar produtos por: \n1. CPF do vendedor\n2. Nome do produto\n3. Listar todos os produtos\nEscolha uma opção: ")
        
        if search_option == '1':
          
            self._search_by_seller_cpf(db)
        elif search_option == '2':
          
            self._search_by_product_name(db)
        elif search_option == '3':
          
            self._list_all_products(db)
        else:
            print("Opção inválida!")
    
    def _search_by_seller_cpf(self, db):
       
        cpf = input("Digite o CPF do vendedor: ")
        seller = db.usuarios.find_one({"cpf": cpf})
        
        if not seller:
            print("Vendedor não encontrado com este CPF!")
            return
            
        products = seller.get("products", [])
        
        if not products:
            print(f"O vendedor {seller.get('nome')} não possui produtos cadastrados.")
            return
            
        print(f"\nProdutos do vendedor {seller.get('nome')}:")
        for idx, prod in enumerate(products, 1):
            print(f"{idx}. {prod.get('nome')} - R$ {prod.get('valor')} - Estoque: {prod.get('estoque')}")
            
        
        self._show_product_detail_option(db, products, is_seller_products=True)
    
    def _search_by_product_name(self, db):
        
        name = input("Digite o nome do produto (ou parte dele): ")
        if not name:
            print("É necessário informar um nome para busca!")
            return
            
       
        products_cursor = db.produtos.find(
            {"nome": {"$regex": name, "$options": "i"}}
        ).sort("nome")
        
        products_list = list(products_cursor)
        
        if not products_list:
            print(f"Nenhum produto encontrado com o nome '{name}'.")
            return
            
        print(f"\nProdutos encontrados com o nome '{name}' ({len(products_list)}):")
        for idx, prod in enumerate(products_list, 1):
            print(f"{idx}. {prod.get('nome')} - R$ {prod.get('valor')} - Estoque: {prod.get('estoque')}")
            
        
        self._show_product_detail_option(db, products_list, is_seller_products=False)
    
    def _list_all_products(self, db):
       
        products_cursor = db.produtos.find().sort("nome")
        products_list = list(products_cursor)
        
        if not products_list:
            print("Não há produtos cadastrados.")
            return
            
        print("\nTodos os produtos:")
        for idx, prod in enumerate(products_list, 1):
            print(f"{idx}. {prod.get('nome')} - R$ {prod.get('valor')} - Estoque: {prod.get('estoque')}")
            
       
        self._show_product_detail_option(db, products_list, is_seller_products=False)
    
    def _show_product_detail_option(self, db, products, is_seller_products):
        
        detail_option = input("\nDeseja ver detalhes de algum produto? (S/N): ")
        if detail_option.upper() == 'S':
            try:
                prod_idx = int(input("Digite o número do produto: ")) - 1
                if 0 <= prod_idx < len(products):
                    if is_seller_products:
                       
                        product_id = products[prod_idx].get("id")
                    else:
                     
                        product_id = products[prod_idx].get("_id")
                    
                    self._show_product_details(db, product_id)
                else:
                    print("Número de produto inválido!")
            except ValueError:
                print("Entrada inválida!")
    
    def _show_product_details(self, db, product_id):
    
        if isinstance(product_id, str):
            try:
                product_id = ObjectId(product_id)
            except:
                print("ID de produto inválido!")
                return
                
        
        product = db.produtos.find_one({"_id": product_id})
        
        if not product:
            print("Produto não encontrado!")
            return
            
       
        print("\nDetalhes do produto:")
        print(f"Nome: {product.get('nome')}")
        print(f"Descrição: {product.get('descricao')}")
        print(f"Marca: {product.get('marca')}")
        print(f"Valor: R$ {product.get('valor'):.2f}")
        print(f"Estoque: {product.get('estoque')}")
        print(f"Avaliação: {product.get('avaliacao', 0.0)}")
        
      
        seller_id = product.get("idVendedor")
        if seller_id:
   
            if isinstance(seller_id, str):
                try:
                    seller_id = ObjectId(seller_id)
                except:
                    seller_id = None
                    
            if seller_id:
                seller = db.usuarios.find_one({"_id": seller_id})
                if seller:
                    print(f"Vendedor: {seller.get('nome')} {seller.get('sobrenome')}")
                    print(f"Contato: {seller.get('email')}")