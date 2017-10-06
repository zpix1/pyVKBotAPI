class T:

    def __init__(self):
        self.a = 2
        pass

    def d(*args, **kwargs):
        #print("decorator sees {} args: {}".format(len(args), str(args)))
        #print("decorator sees {} kwargs: {}".format(len(kwargs), str(kwargs)))
        # xx = self.a
        func = args[1]
        def new_func(*args,**kwargs):
            print('Wrapped!')
            # print(self.a)
            return func(*args, **kwargs)
        return new_func

testo = T()

@testo.d(time = 3)
def foo():
    print('real foo')