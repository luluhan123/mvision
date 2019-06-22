from PyQt5.QtCore import QObject


class AcquisitionPoint(QObject):
    def __init__(self):
        super(AcquisitionPoint, self).__init__()

        self.gsv = None
        self.coordinates = []

    def set_abscissa(self, abs):
        self.coordinates[0] = abs

    def set_ordinate(self, ord):
        self.coordinates[1] = ord

    def set_is_ometric(self, iso):
        self.coordinates[2] = iso

    def get_abscissa(self):
        return self.coordinates[0]

    def get_ordinates(self):
        return self.coordinates[1]

    def get_is_ometric(self):
        return self.coordinates[2]

    def get_gray_scale_value(self):
        return self.gsv
