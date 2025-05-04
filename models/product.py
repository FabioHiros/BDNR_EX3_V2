class Product:
    name: str
    idSeller: str
    description: str
    brand: str
    price: float
    stock: int
    rating: float

    def __init__(self, name="", idSeller="", description="", brand="", price=0.0, stock=0, rating=0.0):
        self.name = name
        self.idSeller = idSeller
        self.description = description
        self.brand = brand
        self.price = price
        self.stock = stock
        self.rating = rating