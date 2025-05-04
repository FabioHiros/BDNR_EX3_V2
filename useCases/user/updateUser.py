from interfaces.update import UpdateStrategy

class UpdateUserStrategy(UpdateStrategy):
    def update(self, db) -> bool:
        cpf = input('Digite o cpf do usuário (apenas números): ')
        query = {"cpf": cpf}
        user = db.usuarios.find_one(query)
        
        if not user:
            print("Usuário não encontrado!")
            return False

        print("Dados do usuário: ", user)
        
        print("CASO NÃO QUEIRA ALTERAR UM CAMPO APENAS DEIXE EM BRANCO!")
        
        nome = input("Mudar Nome: ")
        if len(nome):
            user["nome"] = nome

        sobrenome = input("Mudar Sobrenome: ")
        if len(sobrenome):
            user["sobrenome"] = sobrenome

        novo_cpf = input("Mudar CPF: ")
        if len(novo_cpf):
            user["cpf"] = novo_cpf

        senha = input("Mudar senha: ")
        if len(senha):
            user["senha"] = senha
        
        address_option = input("Deseja gerenciar endereços? (S/N): ")
        if address_option.lower() == 's':
            self._manage_addresses(user)

        
        is_seller = user.get("isSeller", False)
        
        if is_seller:
            
            seller_option = input("Deseja atualizar informações de vendedor? (S/N): ")
            if seller_option.lower() == 's':
                self._update_seller_info(user)
        else:
            
            become_seller = input("Deseja se tornar um vendedor? (S/N): ")
            if become_seller.lower() == 's':
                self._add_seller_info(user)
        
        
        newvalues = {"$set": user}
        result = db.usuarios.update_one(query, newvalues)
        
        if result.modified_count > 0:
            print("Usuário atualizado com sucesso!")
            return True
        else:
            print("Nenhuma alteração foi feita.")
            return False

    def _add_seller_info(self, user):
        
        print("\nAdicionando informações de vendedor:")
        company_name = input("Nome da Empresa: ")
        cnpj = input("CNPJ: ")
        
        user["isSeller"] = True
        user["companyName"] = company_name
        user["cnpj"] = cnpj
    
        user["products"] = []
        user["soldProducts"] = []
        
        print("Usuário agora é um vendedor!")

    def _update_seller_info(self, user):
        """Helper method to update seller information"""
        print("\nInformações atuais de vendedor:")
        print(f"Nome da Empresa: {user.get('companyName', 'N/A')}")
        print(f"CNPJ: {user.get('cnpj', 'N/A')}")
        print(f"Avaliação: {user.get('rating', 0.0)}")
        
        print("\nAtualize as informações (deixe em branco para manter):")
        company_name = input("Nome da Empresa: ")
        if len(company_name):
            user["companyName"] = company_name
            
        cnpj = input("CNPJ: ")
        if len(cnpj):
            user["cnpj"] = cnpj

    def _manage_addresses(self, user):
        """Helper method to manage user addresses"""
        # Display current addresses
        addresses = user.get("endereco", [])
        if addresses:
            print("\nEndereços atuais:")
            for idx, addr in enumerate(addresses, 1):
                print(f"{idx}. {addr.get('rua')}, {addr.get('numero')}, {addr.get('bairro')}, {addr.get('estado')}, {addr.get('cep')}")
        else:
            print("\nNenhum endereço cadastrado.")
        
        # Address management options
        print("\nOpções:")
        print("1. Adicionar novo endereço")
        print("2. Atualizar endereço existente")
        print("3. Remover endereço")
        print("4. Voltar")
        
        option = input("Escolha uma opção: ")
        
        if option == '1':
            # Add new address
            new_address = self._get_address_input()
            if "endereco" not in user:
                user["endereco"] = []
            user["endereco"].append(new_address)
            print("Endereço adicionado com sucesso.")
            
        elif option == '2' and addresses:
            # Update existing address
            idx = int(input("Digite o número do endereço a ser atualizado: ")) - 1
            if 0 <= idx < len(addresses):
                updated_address = self._get_address_input()
                user["endereco"][idx] = updated_address
                print("Endereço atualizado com sucesso.")
            else:
                print("Índice de endereço inválido.")
                
        elif option == '3' and addresses:
            # Remove address
            idx = int(input("Digite o número do endereço a ser removido: ")) - 1
            if 0 <= idx < len(addresses):
                del user["endereco"][idx]
                print("Endereço removido com sucesso.")
            else:
                print("Índice de endereço inválido.")
                
        elif option == '4':
            # Return to main menu
            return
        else:
            print("Opção inválida ou não há endereços para gerenciar.")
    
    def _get_address_input(self):
        """Helper method to get address input from the user"""
        street = input("Rua: ")
        number = input("Número: ")
        neighborhood = input("Bairro: ")
        state = input("Estado: ")
        zipCode = input("CEP: ")
        
        return {
            "rua": street,
            "numero": number,
            "bairro": neighborhood,
            "estado": state,
            "cep": zipCode
        }