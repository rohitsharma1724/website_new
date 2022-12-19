class Users:

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return f"({self.address}, {self.name})"

    def __init__(self, obj, address):
        #store name of the user
        self.temp=None
        self.name = self.temp
        self.address = address
        # address will store the address of listening and sending address
        self.client = obj
        #contains all the information regarding the users joined

