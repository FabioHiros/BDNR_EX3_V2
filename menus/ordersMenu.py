from useCases.orders.createOrder import CreateOrderStrategy
from useCases.orders.deleteOrder import DeleteOrderStrategy
from useCases.orders.updateOrder import UpdateOrderStrategy
from useCases.orders.readOrder import ReadOrderStrategy
def OrderMenu(db):
    while True:
        print("""
                ##### MENU De Compra #####
                    1- Criar Compra
                    2- Ler Compra
                    3- Atualizar Compra
                    4- Deletar Compra
                    
        """)
        option = input("Digite a opção desejada? (V para voltar) ")

        match option:
            case '1':
                strategy = CreateOrderStrategy()
                product=strategy.create(db)
            case '4':
                strategy = DeleteOrderStrategy()
                strategy.delete(db)
                
            case '3':
                strategy= UpdateOrderStrategy()
                strategy.update(db)
            case '2':
                strategy = ReadOrderStrategy()
                strategy.read(db)
            case 'v':
                return