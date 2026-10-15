

class A:
    mobile = 'Redmi'

class B:
    mobile = 'One plus'
    acres = 25

    def house_function(self):
            print("B does house function")

class C:
    def house_function(self):
        print("C does house function")

class D(A, B, C):
    pass

obj = D()
obj.house_function()