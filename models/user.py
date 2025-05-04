from models.address import Address
from models.product import Product
from models.order import Order

class User:
    name: str
    lastName: str
    email: str
    cpf: str
    password: str
    address: list[Address]
    isSeller: bool
    favorites: list[Product]
    orders: list[Order]
    
    companyName: str = None
    cnpj: str = None
   
    products: list[Product] = None
    soldProducts: list[Product] = None

    def __init__(self, name="", lastName="", email="", cpf="", password="", orders=None, favorites=None, address=None, isSeller=False, companyName=None, cnpj=None, products=None, soldProducts=None):
        self.name = name
        self.lastName = lastName
        self.email = email
        self.cpf = cpf
        self.password = password
        self.address = address or []
        self.isSeller = isSeller
        self.favorites = favorites or []
        self.orders = orders or []
        
        
        if isSeller:
            self.companyName = companyName
            self.cnpj = cnpj
            self.products = products or []
            self.soldProducts = soldProducts or []