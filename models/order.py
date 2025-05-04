from models.product import Product
from models.address import Address

class Order:
    products: list[Product]
    value: float
    address: Address
    status: str
    idBuyer: str
    
    def __init__(self, products=None, value=0.0, address=None, status="Pending", idBuyer=""):
        self.products = products or []
        self.value = value
        self.address = address
        self.status = status
        self.idBuyer = idBuyer