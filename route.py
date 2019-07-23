
class Route:

    def __init__(self,capacity):
        self.capacity = capacity,
        self.customer = []
        self.weight = 0,
        self.cost = 0,
        self.savings =0

    def addCustomer(self,index, demand , onTop):

        if(demand >  self.capacity):
            print("Customer demand too large")
            return -1
        else:    
                self.weight += demand
                if(self.weight >  self.capacity):
                    print("Route Overloaded")
                    return -1
                else:
                    if onTop == True :
                        self.customer.insert(0,index)
                        return 1
                    else:
                        self.customer.insert(len(self.customer),index)
                        return 1

        
    
    def checkCustomer(self, index):
        if index not in self.customer:
            print("Customer: " + str(index) +" not present")
            return -1
           
        else:

            i = self.customer.index(index)
            if (0<i<len(self.customer)-1):
                print("Customer: " + str(index) +" interior in the tour")
                return -2

            else: 
                return i #Yeah, it's the starting point or the end point
    
    def printRoute(self):
        print("Depot ")
        for c in  self.customer:
            print(" - " + c )
        print("Depot")