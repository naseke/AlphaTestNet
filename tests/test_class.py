class test:

    def __init__(self):
        self.version = 0.001
        self.text = "coucou"
        self.welcome()

    def welcome(self):
        print('welcome')

    def trt(self):
        obj = test()
        print(self.version)


class test2(test):



    def welcome(self):
        print('tutu')

    def trt(self):
        obj = test2()
        print(self.version, self.text)

toto = test2()
toto.trt()