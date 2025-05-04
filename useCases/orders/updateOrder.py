from interfaces.update import UpdateStrategy
from bson import ObjectId
import datetime

class UpdateOrderStrategy(UpdateStrategy):
    def update(self, db) -> bool:
        print("\nAtualizando pedido")
        
       
        buyer_cpf = input("Digite o CPF do comprador: ")
        buyer = db.usuarios.find_one({"cpf": buyer_cpf})
        
        if not buyer:
            print("Comprador não encontrado!")
            return False
            
   
        orders_list = buyer.get("orders", [])
        if not orders_list:
            print("Este comprador não possui pedidos!")
            return False
            
        print("\nPedidos do comprador:")
        for idx, order_summary in enumerate(orders_list, 1):
            order_date = order_summary.get("dataCriacao", "Data desconhecida")
            if isinstance(order_date, datetime.datetime):
                order_date = order_date.strftime("%d/%m/%Y %H:%M")
            print(f"{idx}. ID: {order_summary.get('id')} - Valor: R$ {order_summary.get('valor'):.2f} - Status: {order_summary.get('status')} - Data: {order_date}")
        
      
        try:
            order_idx = int(input("\nDigite o número do pedido a ser atualizado: ")) - 1
            if not (0 <= order_idx < len(orders_list)):
                print("Índice de pedido inválido!")
                return False
                
            order_id = orders_list[order_idx].get("id")
            
         
            order = db.pedidos.find_one({"_id": ObjectId(order_id)})
            if not order:
                print("Pedido não encontrado no banco de dados!")
                return False
                
            
            current_status = order.get("status")
            if current_status != "Pedido Realizado":
                print(f"Pedidos com status '{current_status}' não podem ser atualizados!")
                print("Apenas pedidos com status 'Pedido Realizado' podem ser modificados.")
                return False
                
         
            print("\nDetalhes do pedido:")
            print(f"ID: {order_id}")
            print(f"Status: {current_status}")
            print(f"Valor total: R$ {order.get('valor'):.2f}")
            print("\nProdutos:")
            for idx, prod in enumerate(order.get("products", []), 1):
                print(f"{idx}. {prod.get('quantidade')}x {prod.get('nome')} - R$ {prod.get('valor') * prod.get('quantidade'):.2f}")
            
           
            print("\nO que deseja atualizar?")
            print("1. Endereço de entrega")
            print("2. Adicionar produtos")
            print("3. Remover produtos")
            print("4. Cancelar pedido")
            print("5. Voltar")
            
            option = input("Escolha uma opção: ")
            
            if option == "1":
                
                delivery_address = self._select_address(buyer)
                if delivery_address:
                    db.pedidos.update_one(
                        {"_id": ObjectId(order_id)},
                        {"$set": {"endereco": delivery_address}}
                    )
                    print("Endereço de entrega atualizado com sucesso!")
                    return True
                    
            elif option == "2":
                
                new_products, additional_value = self._select_products(db)
                if new_products:
                    
                    for product in new_products:
                        db.pedidos.update_one(
                            {"_id": ObjectId(order_id)},
                            {"$push": {"products": product}}
                        )
                        
                        
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
                    
                    
                    new_total = order.get("valor", 0) + additional_value
                    db.pedidos.update_one(
                        {"_id": ObjectId(order_id)},
                        {"$set": {"valor": new_total}}
                    )
                    
                    
                    db.usuarios.update_one(
                        {"_id": ObjectId(buyer.get("_id")), "orders.id": order_id},
                        {"$set": {"orders.$.valor": new_total}}
                    )
                    
                    print("Produtos adicionados ao pedido com sucesso!")
                    print(f"Novo valor total: R$ {new_total:.2f}")
                    return True
                    
            elif option == "3":
                
                current_products = order.get("products", [])
                if not current_products:
                    print("O pedido não possui produtos para remover!")
                    return False
                    
                print("\nProdutos no pedido:")
                for idx, prod in enumerate(current_products, 1):
                    print(f"{idx}. {prod.get('quantidade')}x {prod.get('nome')} - R$ {prod.get('valor') * prod.get('quantidade'):.2f}")
                
                try:
                    prod_idx = int(input("\nDigite o número do produto a remover: ")) - 1
                    if not (0 <= prod_idx < len(current_products)):
                        print("Índice de produto inválido!")
                        return False
                        
                    product_to_remove = current_products[prod_idx]
                    product_id = product_to_remove.get("id")
                    quantity = product_to_remove.get("quantidade")
                    product_value = product_to_remove.get("valor") * quantity
                    
                    
                    db.pedidos.update_one(
                        {"_id": ObjectId(order_id)},
                        {"$pull": {"products": {"id": product_id}}}
                    )
                    
                    
                    new_total = order.get("valor", 0) - product_value
                    db.pedidos.update_one(
                        {"_id": ObjectId(order_id)},
                        {"$set": {"valor": new_total}}
                    )
                    
                    
                    db.usuarios.update_one(
                        {"_id": ObjectId(buyer.get("_id")), "orders.id": order_id},
                        {"$set": {"orders.$.valor": new_total}}
                    )
                    
                    
                    db.produtos.update_one(
                        {"_id": ObjectId(product_id)},
                        {"$inc": {"estoque": quantity}}
                    )
                    
                    
                    seller_id = product_to_remove.get("idVendedor")
                    db.usuarios.update_one(
                        {"_id": ObjectId(seller_id), "products.id": product_id},
                        {"$inc": {"products.$.estoque": quantity}}
                    )
                    
                    print(f"Produto '{product_to_remove.get('nome')}' removido do pedido!")
                    print(f"Novo valor total: R$ {new_total:.2f}")
                    return True
                    
                except ValueError:
                    print("Entrada inválida!")
                    return False
                    
            elif option == "4":
                
                confirm = input("Tem certeza que deseja cancelar o pedido? (S/N): ")
                if confirm.lower() == "s":
                    
                    db.pedidos.update_one(
                        {"_id": ObjectId(order_id)},
                        {"$set": {"status": "Cancelado"}}
                    )
                    
                   
                    db.usuarios.update_one(
                        {"_id": ObjectId(buyer.get("_id")), "orders.id": order_id},
                        {"$set": {"orders.$.status": "Cancelado"}}
                    )
                    
                    
                    for product in order.get("products", []):
                        product_id = product.get("id")
                        quantity = product.get("quantidade")
                        
                        
                        db.produtos.update_one(
                            {"_id": ObjectId(product_id)},
                            {"$inc": {"estoque": quantity}}
                        )
                        
                        
                        seller_id = product.get("idVendedor")
                        db.usuarios.update_one(
                            {"_id": ObjectId(seller_id), "products.id": product_id},
                            {"$inc": {"products.$.estoque": quantity}}
                        )
                        
                        
                        db.usuarios.update_one(
                            {"_id": ObjectId(seller_id)},
                            {"$pull": {"soldProducts": {"id": product_id}}}
                        )
                    
                    print("Pedido cancelado com sucesso!")
                    return True
                else:
                    print("Operação cancelada.")
                    return False
                    
            elif option == "5":
                print("Operação cancelada.")
                return False
                
            else:
                print("Opção inválida!")
                return False
                
        except ValueError:
            print("Entrada inválida!")
            return False
            
    def _select_address(self, buyer):
        """Helper method to select a delivery address"""
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
        """Helper method to select products for the order"""
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
        
        return selected_products, total_value