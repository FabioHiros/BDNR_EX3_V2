from useCases.products.createProduct import CreateProductStrategy
from useCases.products.deleteProduct import DeleteProductStrategy
from useCases.products.updateProduct import UpdateProductStrategy
from useCases.products.readProduct import ReadProductStrategy
def productMenu(db):
    while True:
        print("""
                ##### MENU De PRODUTO #####
                    1- Criar Produto
                    2- Ler Produto
                    3- Atualizar Produto
                    4- Deletar Produto
                    
        """)
        option = input("Digite a opção desejada? (V para voltar) ")

        match option:
            case '1':
                strategy = CreateProductStrategy()
                product=strategy.create(db)
            case '4':
                strategy = DeleteProductStrategy()
                result=strategy.delete(db)
                print(f'produto deletado com sucesso!') if result == True else print('Falha ao deletar produto')
            case '3':
                strategy= UpdateProductStrategy()
                strategy.update(db)
            case '2':
                strategy = ReadProductStrategy()
                strategy.read(db)
            case 'v':
                return