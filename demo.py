

class Iphone18Pro:

    colors = ('Purple', 'Black', 'White', 'Blue')
    cameras = 3
    sim = 1
    buttons = 4
    storage = (256, 512, 1024)
    imei = 12929893

    # how to create a class method
    def display(self):
        print(f'''phone common specs are cameras:{self.cameras}, 
            sim: {self.sim}
            storage options: {self.storage}''')

phone1 = Iphone18Pro()
print(phone1.imei)

# how to use class method

phone1.display()