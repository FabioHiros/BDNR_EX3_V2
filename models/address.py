
class Address:
    street: str
    number: str
    neighborhood: str
    state: str
    zipCode: str

    def __init__(self,state,street,number,neighborhood,zipCode):
       self.street = street
       self.state = state
       self.zipCode = zipCode
       self.neighborhood = neighborhood
       self.number = number
