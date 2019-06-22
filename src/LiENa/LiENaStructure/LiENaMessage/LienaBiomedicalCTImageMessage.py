from src.LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaBiomedicalCTImageMessage(LienaMessage):
    def __init__(self):
        LienaMessage.__init__(self)

        self.width = 0
        self.height = 0
        self.depth = 0
        self.xSpacing = 0
        self.ySpacing = 0
        self.zSpacing = 0
        self.dataType = 0
        self.MSB = 0
        self.CTImageMessageBody = ""

    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width

    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height

    def set_depth(self,depth):
        self.depth = depth

    def get_depth(self):
        return self.depth

    def set_x_spacing(self,x_spacing):
        self.xSpacing = x_spacing

    def get_x_spacing(self):
        return  self.xSpacing

    def set_y_spacing(self,y_spacing):
        self.ySpacing = y_spacing

    def get_y_spacing(self):
        return self.ySpacing

    def set_z_spacing(self,z_spacing):
        self.zSpacing = z_spacing

    def get_z_spacing(self):
        return self.zSpacing

    def set_message_id(self, data_type):
        self.dataType = data_type

    def get_message_id(self):
        return self.dataType

    def set_msb(self,msb):
        self.MSB = msb

    def get_msb(self):
        return self.MSB

    def set_ct_image_message_body(self, ct_image_message_body):
        self.CTImageMessageBody = ct_image_message_body

    def get_ct_image_message_body(self):
        return self.CTImageMessageBody

