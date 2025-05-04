from interfaces.create import CreateStrategy
from models.order import Order
from models.address import Address
from bson import ObjectId
import datetime
class CreateOrderStrategy(CreateStrategy):
    def create(self, db) -> Order:
        print("\nCriando novo pedido")
        
        
        buyer_cpf = input("Digite o CPF do comprador: ")
        buyer = db.usuarios.find_one({"cpf": buyer_cpf})
        
        if not buyer:
            print("Comprador não encontrado!")
            return None
            
        buyer_id = str(buyer.get('_id'))
        
        
        delivery_address = self._select_address(buyer)
        if not delivery_address:
            return None
        
        
        selected_products, total_value = self._select_products(db)
        if not selected_products:
            return None
        
        
        order = Order(
            products=selected_products,
            value=total_value,
            address=delivery_address,
            status="Pedido Realizado",
            idBuyer=buyer_id
        )
        
        
        order_dict = {
            "products": [
                {
                    "id": prod.get("id"),
                    "nome": prod.get("nome"),
                    "valor": prod.get("valor"),
                    "quantidade": prod.get("quantidade"),
                    "idVendedor": prod.get("idVendedor")
                } for prod in order.products
            ],
            "valor": order.value,
            "endereco": {
                "rua": order.address.get("rua"),
                "numero": order.address.get("numero"),
                "bairro": order.address.get("bairro"),
                "estado": order.address.get("estado"),
                "cep": order.address.get("cep")
            },
            "status": order.status,
            "idComprador": order.idBuyer,
            "dataCriacao": datetime.datetime.now()
        }
        
        
        result = db.pedidos.insert_one(order_dict)
        order_id = result.inserted_id
        print(f"Pedido criado com ID: {order_id}")
        
        
        order_summary = {
            "id": str(order_id),
            "valor": order.value,
            "status": order.status,
            "dataCriacao": datetime.datetime.now()
        }
        
        if "orders" not in buyer:
            db.usuarios.update_one(
                {"_id": ObjectId(buyer_id)},
                {"$set": {"orders": [order_summary]}}
            )
        else:
            db.usuarios.update_one(
                {"_id": ObjectId(buyer_id)},
                {"$push": {"orders": order_summary}}
            )
        
        
        for product in selected_products:
            product_id = product.get("id")
            quantity = product.get("quantidade")
            
            
            db.produtos.update_one(
                {"_id": ObjectId(product_id)},
                {"$inc": {"estoque": -quantity}}
            )
            
            
            seller_id = product.get("idVendedor")
            db.usuarios.update_one(
                {"_id": ObjectId(seller_id), "products.id": product_id},
                {"$inc": {"products.$.estoque": -quantity}}
            )
            
            
            sold_product = {
                "id": product_id,
                "nome": product.get("nome"),
                "valor": product.get("valor"),
                "quantidade": quantity,
                "dataVenda": datetime.datetime.now()
            }
            
            db.usuarios.update_one(
                {"_id": ObjectId(seller_id)},
                {"$push": {"soldProducts": sold_product}}
            )
        
        print("Pedido realizado com sucesso!")
        return order
    
    def _select_address(self, buyer):
    
        addresses = buyer.get("endereco", [])
        
        if not addresses:
            print("O comprador não possui endereços cadastrados!")
            return None
        
        print("\nSelecione um endereço para entrega:")
        for idx, addr in enumerate(addresses, 1):
            print(f"{idx}. {addr.get('rua')}, {addr.get('numero')}, {addr.get('bairro')}, {addr.get('estado')}, {addr.get('cep')}")
        
        try:
            addr_idx = int(input("Digite o número do endereço: ")) - 1
            if 0 <= addr_idx < len(addresses):
                return addresses[addr_idx]
            else:
                print("Índice de endereço inválido!")
                return None
        except ValueError:
            print("Entrada inválida!")
            return None
    
    def _select_products(self, db):
        
        selected_products = []
        total_value = 0.0
        
        while True:
            
            search_term = input("\nBuscar produto (deixe em branco para parar): ")
            if not search_term:
                if selected_products:
                    break
                else:
                    print("Você precisa selecionar pelo menos um produto!")
                    continue
            
            
            products = list(db.produtos.find(
                {"nome": {"$regex": search_term, "$options": "i"}}
            ))
            
            if not products:
                print("Nenhum produto encontrado com esse termo!")
                continue
            
            
            print("\nProdutos encontrados:")
            for idx, prod in enumerate(products, 1):
                stock = prod.get("estoque", 0)
                if stock > 0:
                    print(f"{idx}. {prod.get('nome')} - R$ {prod.get('valor'):.2f} - Estoque: {stock}")
                else:
                    print(f"{idx}. {prod.get('nome')} - R$ {prod.get('valor'):.2f} - FORA DE ESTOQUE")
            
            
            try:
                prod_idx = int(input("\nDigite o número do produto (0 para voltar): ")) - 1
                if prod_idx == -1:  
                    continue
                    
                if 0 <= prod_idx < len(products):
                    selected_product = products[prod_idx]
                    
                    
                    if selected_product.get("estoque", 0) <= 0:
                        print("Este produto está fora de estoque!")
                        continue
                    
                    
                    max_qty = selected_product.get("estoque", 0)
                    qty = int(input(f"Quantidade (máximo {max_qty}): "))
                    
                    if qty <= 0:
                        print("Quantidade inválida!")
                        continue
                        
                    if qty > max_qty:
                        print(f"Quantidade máxima disponível: {max_qty}")
                        continue
                    
                    
                    product_value = selected_product.get("valor", 0) * qty
                    product_summary = {
                        "id": str(selected_product.get("_id")),
                        "nome": selected_product.get("nome"),
                        "valor": selected_product.get("valor"),
                        "quantidade": qty,
                        "idVendedor": selected_product.get("idVendedor")
                    }
                    
                    selected_products.append(product_summary)
                    total_value += product_value
                    
                    print(f"{qty}x {selected_product.get('nome')} adicionado ao pedido")
                    print(f"Valor total até agora: R$ {total_value:.2f}")
                    
                    
                    add_more = input("\nDeseja adicionar mais produtos? (S/N): ")
                    if add_more.lower() != 's':
                        break
                else:
                    print("Índice de produto inválido!")
            except ValueError:
                print("Entrada inválida!")
        
        print(f"\nResumo do pedido:")
        print(f"Total de produtos: {len(selected_products)}")
        for prod in selected_products:
            print(f"{prod.get('quantidade')}x {prod.get('nome')} - R$ {prod.get('valor') * prod.get('quantidade'):.2f}")
        print(f"Valor total: R$ {total_value:.2f}")
        
        return selected_products, total_value