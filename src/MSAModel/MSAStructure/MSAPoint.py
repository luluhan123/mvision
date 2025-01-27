class MSAPoint:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

        self.v = [0.0, 0.0]

        self.weight = 0

    def set_curvature(self, a, b):
        self.v[0] = a
        self.v[1] = b

    def set_lle_weight(self, w):
        self.weight = w

    def get_weight(self):
        return self.weight

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

