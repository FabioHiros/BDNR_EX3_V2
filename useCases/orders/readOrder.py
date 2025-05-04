from interfaces.read import ReadStrategy
from bson import ObjectId
import datetime

class ReadOrderStrategy(ReadStrategy):
    def read(self, db) -> None:
        print("\nConsulta de Pedidos")
        print("1. Buscar pedidos por CPF do cliente")
        print("2. Listar todos os pedidos")
        
        option = input("Escolha uma opção: ")
        
        if option == "1":
            self._read_by_cpf(db)
        elif option == "2":
            self._read_all_orders(db)
        else:
            print("Opção inválida!")
    
    def _read_by_cpf(self, db):
        
        cpf = input("Digite o CPF do cliente: ")
        user = db.usuarios.find_one({"cpf": cpf})
        
        if not user:
            print(f"Nenhum usuário encontrado com o CPF: {cpf}")
            return
        
        orders = user.get("orders", [])
        if not orders:
            print(f"O usuário {user.get('nome')} não possui pedidos.")
            return
        
        print(f"\nPedidos do cliente {user.get('nome')} {user.get('sobrenome')}:")
        for idx, order_summary in enumerate(orders, 1):
            order_date = order_summary.get("dataCriacao", "Data desconhecida")
            if isinstance(order_date, datetime.datetime):
                order_date = order_date.strftime("%d/%m/%Y %H:%M")
            
            print(f"{idx}. ID: {order_summary.get('id')} - R$ {order_summary.get('valor'):.2f} - Status: {order_summary.get('status')} - Data: {order_date}")
        
        
        detail_option = input("\nDeseja ver detalhes de algum pedido? (S/N): ")
        if detail_option.upper() == 'S':
            try:
                order_idx = int(input("Digite o número do pedido: ")) - 1
                if 0 <= order_idx < len(orders):
                    order_id = orders[order_idx].get("id")
                    self._show_order_details(db, order_id)
                else:
                    print("Número de pedido inválido!")
            except ValueError:
                print("Entrada inválida!")
    
    def _read_all_orders(self, db):
       
        
        orders_cursor = db.pedidos.find().sort("dataCriacao", -1)
        orders_list = list(orders_cursor)
        
        if not orders_list:
            print("Não há pedidos no sistema.")
            return
        
        print(f"\nTodos os pedidos ({len(orders_list)}):")
        for idx, order in enumerate(orders_list, 1):
            order_id = str(order.get("_id"))
            order_date = order.get("dataCriacao", "Data desconhecida")
            if isinstance(order_date, datetime.datetime):
                order_date = order_date.strftime("%d/%m/%Y %H:%M")
            
            buyer_id = order.get("idComprador")
            buyer_name = "Cliente desconhecido"
            
            
            if buyer_id:
                try:
                    buyer = db.usuarios.find_one({"_id": ObjectId(buyer_id)})
                    if buyer:
                        buyer_name = f"{buyer.get('nome')} {buyer.get('sobrenome')}"
                except:
                    pass
            
            print(f"{idx}. ID: {order_id} - Cliente: {buyer_name} - R$ {order.get('valor'):.2f} - Status: {order.get('status')} - Data: {order_date}")
        
        
        detail_option = input("\nDeseja ver detalhes de algum pedido? (S/N): ")
        if detail_option.upper() == 'S':
            try:
                order_idx = int(input("Digite o número do pedido: ")) - 1
                if 0 <= order_idx < len(orders_list):
                    order_id = str(orders_list[order_idx].get("_id"))
                    self._show_order_details(db, order_id)
                else:
                    print("Número de pedido inválido!")
            except ValueError:
                print("Entrada inválida!")
    
    def _show_order_details(self, db, order_id):
        """Show detailed information about a specific order"""
        try:
            order = db.pedidos.find_one({"_id": ObjectId(order_id)})
            if not order:
                print("Pedido não encontrado!")
                return
            
            
            buyer_id = order.get("idComprador")
            buyer_name = "Cliente desconhecido"
            buyer_email = "Email desconhecido"
            
            if buyer_id:
                try:
                    buyer = db.usuarios.find_one({"_id": ObjectId(buyer_id)})
                    if buyer:
                        buyer_name = f"{buyer.get('nome')} {buyer.get('sobrenome')}"
                        buyer_email = buyer.get('email', 'Email desconhecido')
                except:
                    pass
            
            
            order_date = order.get("dataCriacao", "Data desconhecida")
            if isinstance(order_date, datetime.datetime):
                order_date = order_date.strftime("%d/%m/%Y %H:%M")
            
            
            print("\n" + "="*50)
            print(f"DETALHES DO PEDIDO (ID: {order_id})")
            print("="*50)
            print(f"Data: {order_date}")
            print(f"Status: {order.get('status')}")
            print(f"Cliente: {buyer_name}")
            print(f"Contato: {buyer_email}")
            
            
            address = order.get("endereco", {})
            print(f"\nENDEREÇO DE ENTREGA:")
            print(f"Rua: {address.get('rua', 'N/A')}, {address.get('numero', 'N/A')}")
            print(f"Bairro: {address.get('bairro', 'N/A')}")
            print(f"Cidade/Estado: {address.get('cidade', 'N/A')}/{address.get('estado', 'N/A')}")
            print(f"CEP: {address.get('cep', 'N/A')}")
            
           
            products = order.get("products", [])
            print(f"\nPRODUTOS ({len(products)}):")
            print("-"*50)
            print(f"{'Qtd':<5} {'Produto':<30} {'Valor Unit.':<15} {'Subtotal':<15}")
            print("-"*50)
            
            for product in products:
                qty = product.get("quantidade", 0)
                name = product.get("nome", "Produto desconhecido")
                price = product.get("valor", 0)
                subtotal = qty * price
                
                print(f"{qty:<5} {name[:30]:<30} R$ {price:<12.2f} R$ {subtotal:<12.2f}")
            
            print("-"*50)
            print(f"{'TOTAL':<50} R$ {order.get('valor', 0):.2f}")
            print("="*50)
            
        except Exception as e:
            print(f"Erro ao mostrar detalhes do pedido: {e}")