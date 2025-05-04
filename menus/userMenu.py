from useCases.user.createUser import CreateUserStrategy
from useCases.user.deleteUser import DeleteUserStrategy
from useCases.user.updateUser import UpdateUserStrategy
from useCases.user.readUser import ReadUserStrategy
def userMenu(db):
    while True:
        print("""
                ##### MENU DO USUÁRIO #####
                    1- Criar Usuário
                    2- Ler Usuário
                    3- Atualizar Usuário
                    4- Deletar Usuário
        """)
        option = input("Digite a opção desejada? (V para voltar) ")

        match option:
            case '1':
                strategy = CreateUserStrategy()
                user=strategy.create(db)
                print(f"Usuário {user.name} criado com sucesso!")
            case '4':
                strategy = DeleteUserStrategy()
                result=strategy.delete(db)
                print(f'usuário deletado com sucesso!') if result == True else print('Falha ao deletar usuário')
            case '3':
                strategy= UpdateUserStrategy()
                strategy.update(db)
            case '2':
                strategy = ReadUserStrategy()
                strategy.read(db)
            case 'v':
                return