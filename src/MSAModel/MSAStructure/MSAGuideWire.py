class MSAGuideWire:
    def __init__(self, point_set, length, break_point):
        self.point_set = point_set
        self.length = length
        self.break_point = break_point

    def get_length(self):
        return self.length

    def get_breakpoint(self):
        return self.break_point

    def get_point_set(self):
        return self.point_set

