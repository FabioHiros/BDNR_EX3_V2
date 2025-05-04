from interfaces.delete import DeleteStrategy
from bson import ObjectId
import datetime

class DeleteOrderStrategy(DeleteStrategy):
    def delete(self, db) -> bool:
        print("\nCancelar/Deletar Pedido")
        
        
        buyer_cpf = input("Digite o CPF do cliente: ")
        buyer = db.usuarios.find_one({"cpf": buyer_cpf})
        
        if not buyer:
            print("Cliente não encontrado!")
            return False
            
        
        orders_list = buyer.get("orders", [])
        if not orders_list:
            print("Este cliente não possui pedidos!")
            return False
            
        print(f"\nPedidos do cliente {buyer.get('nome')} {buyer.get('sobrenome')}:")
        for idx, order_summary in enumerate(orders_list, 1):
            order_date = order_summary.get("dataCriacao", "Data desconhecida")
            if isinstance(order_date, datetime.datetime):
                order_date = order_date.strftime("%d/%m/%Y %H:%M")
            print(f"{idx}. ID: {order_summary.get('id')} - R$ {order_summary.get('valor'):.2f} - Status: {order_summary.get('status')} - Data: {order_date}")
        
        
        try:
            order_idx = int(input("\nDigite o número do pedido a ser cancelado/deletado: ")) - 1
            if not (0 <= order_idx < len(orders_list)):
                print("Índice de pedido inválido!")
                return False
                
            order_id = orders_list[order_idx].get("id")
            
           
            order = db.pedidos.find_one({"_id": ObjectId(order_id)})
            if not order:
                print("Pedido não encontrado no banco de dados!")
                return False
                
            
            current_status = order.get("status")
            
            
            if current_status == "Pedido Realizado":
                print("\nOpções:")
                print("1. Cancelar pedido (restaurar estoque)")
                print("2. Excluir permanentemente")
                print("3. Voltar")
                
                option = input("Escolha uma opção: ")
                
                if option == "1":
                    return self._cancel_order(db, order, order_id, buyer)
                elif option == "2":
                    return self._delete_order(db, order, order_id, buyer)
                else:
                    print("Operação cancelada.")
                    return False
                    
            elif current_status == "Cancelado":
                print("\nEste pedido já está cancelado.")
                confirm = input("Deseja excluir permanentemente? (S/N): ")
                if confirm.lower() == "s":
                    return self._delete_order(db, order, order_id, buyer)
                else:
                    print("Operação cancelada.")
                    return False
                    
            else:
                print(f"\nPedidos com status '{current_status}' não podem ser cancelados.")
                print("Deseja excluir permanentemente este pedido?")
                print("ATENÇÃO: Esta ação não restaurará o estoque dos produtos.")
                confirm = input("Confirmar exclusão permanente? (S/N): ")
                
                if confirm.lower() == "s":
                    return self._delete_order(db, order, order_id, buyer)
                else:
                    print("Operação cancelada.")
                    return False
                
        except ValueError:
            print("Entrada inválida!")
            return False
    
    def _cancel_order(self, db, order, order_id, buyer):
        
        print("\nCancelando pedido...")
        
       
        db.pedidos.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": "Cancelado"}}
        )
        
        
        db.usuarios.update_one(
            {"_id": buyer.get("_id"), "orders.id": order_id},
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
    
    def _delete_order(self, db, order, order_id, buyer):
        """Helper method to permanently delete an order"""
        print("\nExcluindo pedido permanentemente...")
        
        
        if order.get("status") != "Cancelado":
            confirm = input("Esta ação é irreversível. Confirmar exclusão? (S/N): ")
            if confirm.lower() != "s":
                print("Operação cancelada.")
                return False
        
        
        db.pedidos.delete_one({"_id": ObjectId(order_id)})
        
        
        db.usuarios.update_one(
            {"_id": buyer.get("_id")},
            {"$pull": {"orders": {"id": order_id}}}
        )
        
        print("Pedido excluído permanentemente!")
        return True