class A:
    def __init__(self, e):
        self.e = e


class A1(A):
    def __init__(self):
        super(A, self).__init__()