from PyQt5.QtCore import QObject
from vtk import vtkMath


class MSACenterlinePoint(QObject):
    def __init__(self):
        super(MSACenterlinePoint, self).__init__()
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0

        self.x_diff = 0.0
        self.y_diff = 0.0
        self.z_diff = 0.0

        self.sparse_id = 0

        self.vector = []
        # self.vector[0] = 0.0
        # self.vector[1] = 0.0
        # self.vector[2] = 0.0

        self.cos_theta = 0.0
        self.cos_sigma = 0.0
        self.constant_k = 0.0

        self.radius = 0.0

        self.acquisition_radius = 40
        self.acquisition_frequence = 40

        self.id = 0
        self.acquisition_points = list()

        self.acquisition_vector = []

    def get_abscissa(self):
        return self.pos_x

    def get_ordinate(self):
        return self.pos_y

    def get_isometric(self):
        return self.pos_z

    def set_abscissa(self, pos_x):
        self.pos_x = pos_x

    def set_ordinate(self, pos_y):
        self.pos_y = pos_y

    def set_isometric(self, pos_z):
        self.pos_z = pos_z

    def set_vectors(self, vec_x, vec_y, vec_z):
        self.vector[0] = vec_x
        self.vector[1] = vec_y
        self.vector[2] = vec_z

    def get_vector(self):
        return self.vector

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def print_acquisition_points(self):
        for cpt in range(len(self.acquisition_points)):
            print("here need to add")

    def append_acquisition_points(self, acq_point):
        return self.acquisition_points.append(acq_point)

    def get_acquisition_point_at(self, index):
        return self.acquisition_points[index]

    def print_point(self):
        print(self.pos_x, self.pos_y, self.pos_z)

    def normalize(self):
        vtkMath.Normalize(self.vector)

    def update(self):
        self.vector[0] = self.x_diff
        self.vector[1] = self.y_diff
        self.vector[2] = self.z_diff
        self.normalize()

    def normalize_uvw(self):
        vtkMath.Normalize(self.acquisition_vector)

    def set_cos_sigma(self, cos_sigma):
        self.cos_sigma = cos_sigma
        self.set_cos_theta()

    def set_cos_theta(self, cos_theta):
        self.cos_theta = cos_theta

    def set_acquisition_k(self, constant_k):
        self.constant_k = constant_k

    def get_acquisition_k(self):
        return self.constant_k

    def set_acguisition_vector(self,u):
        self.acquisition_vector[0] = u

    def set_acquisition_vector(self, v):
        self.acquisition_vector[1] = v

    def set_acquisition_vector(self, w):
        self.acquisition_vector[2] = w

    def set_acquisition_radius(self,r):
        self.acquisition_radius = r

    def set_acquisition_frequence(self, frequence):
        self.acquisition_frequence = frequence

    def get_acquisition_vector_u(self):
        return self.acquisition_vector[0]

    def get_acquisition_vector_v(self):
        return self.acquisition_vector[1]

    def get_acquisition_vector_w(self):
        return self.acquisition_vector[2]

    def get_acquisition_radius(self):
        return self.acquisition_radius

    def get_acquisition_frequence(self):
        return self.acquisition_frequence

    def set_x_diff(self, x_diff):
        self.x_diff = x_diff

    def set_y_diff(self, y_diff):
        self.y_diff = y_diff

    def set_z_diff(self, z_diff):
        self.z_diff = z_diff

    def set_radius(self, radius):
        self.radius = radius

    def get_vector_x(self):
        return self.vector[0]

    def get_vector_y(self):
        return self.vector[1]

    def get_vector_z(self):
        return self.vector[2]

    def get_x_diff(self):
        return self.vector[0]

    def get_y_diff(self):
        return self.vector[1]

    def get_z_diff(self):
        return self.vector[2]

    def get_radiu(self):
        return self.radius

    def get_cos_sigma(self):
        return self.cos_sigma

    def get_cos_theta(self):
        return self.cos_theta

    def set_sparse_id(self, id):

        self.sparse_id = id

    def get_sparse_id(self):
        return self.sparse_id














