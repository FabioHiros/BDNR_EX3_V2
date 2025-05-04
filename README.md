### Interaçãoes Feitas com o Redis
1- Login : sistema faz um login básico e cria uma sessão no redis, caso o usuário rode o programa<br>
dentro do tempo de expiração de 100 segundos, não será necessário informar a senha novamente<br><br>
2- atualização de produtos: ao atualizar um produto o mesmo é atualizado apenas no redis até que o usuário sincronize os bancos<br>
3- criação de favoritos: os favoritos de um usuário serão adicionados ao redis e para que sejam adicionados ao mongo precisam ser sincronizados<br>
4- sincronização: criação de uma função para sincronizar os dados do redis com o mongodb<br>
### Como Utilizar o programa
<br>
1 - Clone o repositório<br>
2 - crie um ambiente virtual python -m venv venv<br>
3 - inicie o ambiente virtual \venv\Scripts\activate<br>
4 - instale as librarys pip install -r requirements.txt<br>
5 - rode o programa <strong>python main.py</strong><br>

