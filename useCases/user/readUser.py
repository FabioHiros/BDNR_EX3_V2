from interfaces.read import ReadStrategy

class ReadUserStrategy(ReadStrategy):
    def read(self, db) -> None:
        cpf = input("Digite o cpf do usuário que deseja visualizar (apenas números): ")
        
        if not len(cpf):
            
            print("Usuários existentes: ")
            users = db.usuarios.find().sort("nome")
            print("NOME  CPF")
            for user in users:
                print(f"{user.get('nome', 'N/A')}  {user.get('cpf', 'N/A')}")
        else:
            
            query = {"cpf": cpf}
            user = db.usuarios.find_one(query)
            
            if user:
                print("\nInformações do usuário:")
                print(f"Nome: {user.get('nome', 'N/A')} {user.get('sobrenome', 'N/A')}")
                print(f"CPF: {user.get('cpf', 'N/A')}")
                print(f"Email: {user.get('email', 'N/A')}")
                
                
                addresses = user.get('endereco', [])
                if addresses:
                    print("\nEndereços:")
                    for idx, addr in enumerate(addresses, 1):
                        print(f"  Endereço {idx}:")
                        print(f"    Rua: {addr.get('rua', 'N/A')}, Nº {addr.get('numero', 'N/A')}")
                        print(f"    Bairro: {addr.get('bairro', 'N/A')}")
                        print(f"    Estado: {addr.get('estado', 'N/A')}")
                        print(f"    CEP: {addr.get('cep', 'N/A')}")
                else:
                    print("\nNenhum endereço cadastrado.")
                
               
                favorites = user.get('favorites', [])
                if favorites:
                    print("\nProdutos Favoritos:")
                    print("-"*50)
                    print(f"{'#':<3} {'Produto':<30} {'Preço':<15}")
                    print("-"*50)
                    
                    for idx, fav in enumerate(favorites, 1):
                        name = fav.get("nome", "Produto desconhecido")
                        price = fav.get("valor", 0)
                        print(f"{idx:<3} {name[:30]:<30} R$ {price:<12.2f}")
                    
                    print("-"*50)
                else:
                    print("\nNenhum produto favorito.")
                
               
                orders = user.get('orders', [])
                if orders:
                    print("\nPedidos:")
                    for idx, order in enumerate(orders, 1):
                        order_date = order.get("dataCriacao", "Data desconhecida")
                        if hasattr(order_date, 'strftime'):
                            order_date = order_date.strftime("%d/%m/%Y %H:%M")
                            
                        print(f"  {idx}. ID: {order.get('id')} - R$ {order.get('valor', 0):.2f} - Status: {order.get('status', 'N/A')} - Data: {order_date}")
                else:
                    print("\nNenhum pedido realizado.")
                
                
                if user.get('isSeller', False):
                    print("\nInformações de vendedor:")
                    print(f"Nome da Empresa: {user.get('companyName', 'N/A')}")
                    print(f"CNPJ: {user.get('cnpj', 'N/A')}")
                    print(f"Avaliação: {user.get('rating', 'N/A')}")
                    
                    
                    products = user.get('products', [])
                    if products:
                        print("\nProdutos à venda:")
                        print("-"*50)
                        print(f"{'#':<3} {'Produto':<30} {'Preço':<15} {'Estoque':<10}")
                        print("-"*50)
                        
                        for idx, prod in enumerate(products, 1):
                            name = prod.get("nome", "Produto desconhecido")
                            price = prod.get("valor", 0)
                            stock = prod.get("estoque", 0)
                            print(f"{idx:<3} {name[:30]:<30} R$ {price:<12.2f} {stock:<10}")
                        
                        print("-"*50)
                    else:
                        print("\nNenhum produto à venda.")
                    
                    
                    sold_products = user.get('soldProducts', [])
                    if sold_products:
                        print("\nProdutos Vendidos:")
                        for idx, sold_prod in enumerate(sold_products, 1):
                            name = sold_prod.get("nome", "Produto desconhecido")
                            quantity = sold_prod.get("quantidade", 0)
                            sale_date = sold_prod.get("dataVenda", "Data desconhecida")
                            if hasattr(sale_date, 'strftime'):
                                sale_date = sale_date.strftime("%d/%m/%Y")
                                
                            print(f"  {idx}. {quantity}x {name} - Data: {sale_date}")
                    else:
                        print("\nNenhum produto vendido.")
            else:
                print(f"Nenhum usuário encontrado com o CPF: {cpf}")