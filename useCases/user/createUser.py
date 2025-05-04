from interfaces.create import CreateStrategy
from models.user import User
from models.address import Address

class CreateUserStrategy(CreateStrategy):
    def create(self, db) -> User:
        print("\nCriando novo usuário")
        name = input("Nome: ")
        lastName = input("Sobrenome: ")
        email = input("Email: ")
        cpf = input("CPF: ")
        password = input("Senha: ")
        
       
        address_list = []
        key = 's'
        while key.lower() != 'n':
            print("\nAdicionando endereço:")
            street = input("Rua: ")
            number = input("Número: ")
            neighborhood = input("Bairro: ")
            state = input("Estado: ")
            zipCode = input("CEP: ")
            
            address = Address(state, street, number, neighborhood, zipCode)
            address_list.append(address)
            
            key = input("Adicionar outro endereço? (S/N): ")
        
       
        is_seller_input = input("\nDeseja se cadastrar como vendedor? (S/N): ")
        is_seller = is_seller_input.upper() == 'S'
        
        
        user = User(
            name=name, 
            lastName=lastName, 
            email=email, 
            cpf=cpf, 
            password=password, 
            address=address_list,
            isSeller=is_seller,
            favorites=[],
            orders=[]
        )
        
       
        if is_seller:
            print("\nInformações de vendedor:")
            company_name = input("Nome da Empresa: ")
            cnpj = input("CNPJ: ")
            
          
            user.companyName = company_name
            user.cnpj = cnpj
            user.rating = 0.0
            user.products = []
            user.soldProducts = []
        
      
        user_dict = {
            "nome": user.name,
            "sobrenome": user.lastName,
            "email": user.email,
            "cpf": user.cpf,
            "senha": user.password,
            "endereco": [
                {
                    "rua": addr.street,
                    "numero": addr.number,
                    "bairro": addr.neighborhood,
                    "estado": addr.state,
                    "cep": addr.zipCode
                } for addr in user.address
            ],
            "isSeller": user.isSeller,
            "favorites": [],
            "orders": []
        }
        

        if user.isSeller:
            user_dict["companyName"] = user.companyName
            user_dict["cnpj"] = user.cnpj
            user_dict["rating"] = user.rating
            user_dict["products"] = []
            user_dict["soldProducts"] = []
        
       
        result = db.usuarios.insert_one(user_dict)
        print(f"Usuário criado com ID: {result.inserted_id}")
        return user