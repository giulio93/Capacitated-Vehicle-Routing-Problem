
class Route:

    def __init__(self,capacity):
        self.capacity = int(capacity),
        self.customers = []
        self.payload = 0
        self.cost = 0,
        self.savings =0

    def addCustomer(self,index, demand , onTop):
        
        if(demand >  self.capacity[0]):
            print("Customer demand too large")
            return -1
        else:    
                tempPayload = int(self.payload + demand)
                if(tempPayload >  self.capacity[0]):
                    print("Route Overloaded")
                    return -1
                else:
                    self.payload = tempPayload
                    if onTop == True :
                        self.customers.insert(0,index)
                        return 1
                    else:
                        self.customers.insert(len(self.customers),index)
                        return 1

        
    
    def checkCustomer(self, index):
        if index not in self.customers:
            print("Customer: " + str(index) +" not present")
            return -1
           
        else:

            i = self.customers.index(index)
            if (0<i<len(self.customers)-1):
                print("Customer: " + str(index) +" interior in the tour")
                return -2

            else: 
                return i #Yeah, it's the starting point or the end point
    
    def getCustomers(self):
        return self.customers

    def getPayload(self):
        return self.payload
     

    def printRoute(self,name):
        textRoute = "Route_"+str(name)+": "
        print("Route:", end =" ")
        for c in  self.customers:
            print(str(c), end="-" )
            textRoute += str(c) + "-"
        print("END")
        textRoute += "END"
        return textRoute
    