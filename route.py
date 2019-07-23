
class Route:

    def __init__(self,capacity):
        self.capacity = capacity,
        self.customer = []
        self.weight = 0,
        self.cost = 0,
        self.savings =0

    def addCustomer(self,index, demand , onTop):

        if onTop == True :
            self.customer.insert(0,index)
        else:
             self.customer.insert(index)

        if(demand >  self.capacity):
            print("Customer demand too large")
        else:    
              self.weight += demand

        if(self.weight >  self.capacity):
            print("Route Overloaded")
    
    def checkCustomer(self, index):
        if index not in self.customer:
            return -1
        else:
            return self.customer.index(index)