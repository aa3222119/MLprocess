class Foo:  # 定义类Foo   实例化时Foo(*arg)中*arg会传入类的__init__方法
    counter1 = 0

    def __init__(self, name):
        self.name1 = name
        self.counter2 = 0
        self.count()

    def count(self):
        Foo.counter1 += 1
        self.counter2 += 1

    def display(self):
        print("my name is %s :\n  " % self.name1 + "counter1=%d" % self.counter1, ",counter2=%d" % self.counter2)


class Smart(Foo):

    def __init__(self, name):
        super(Smart, self).__init__(name)     # 继承父类Foo的变量和方法
        self.counter2 *= 2

    def count(self):
        Smart.counter1 += 1
        self.counter2 += 1

Foo('TOM').display()  # Class().method 指调用实例Class()下的method方法
tony = Smart('antony')
tony.display()
