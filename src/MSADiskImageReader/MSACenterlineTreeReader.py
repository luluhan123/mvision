from PyQt5.QtCore import QObject, QFile, QIODevice
from vtk import vtkMath
from MSAModel.MSAStructure.MSACenterlineTree import MSACenterlineTree
from MSAModel.MSAStructure.MSACenterlineBranch import MSACenterlineBranch
from MSAModel.MSAStructure.MSACenterlinePoint import MSACenterlinePoint


class MSACenterlineTreeReader(QObject):

    def __init__(self):
        super(MSACenterlineTreeReader, self).__init__()

    def do_read_center_line_tree(self, path):
        file = open(path)
        ret = MSACenterlineTree()
        all_string = str(file.read())
        all_string += "["

        branch_text_segments = all_string.split("Branch Set")

        pts_count = 0
        for branch_index in range(1, len(branch_text_segments)):
            branch = MSACenterlineBranch()
            branch.set_index(branch_index)

            temp = branch_text_segments[branch_index]

            temp1 = temp.split("Dmin\n")
            temp2 = temp1[1]
            temp3 = temp2.split("[")

            coordinate_text = temp3[0]
            coordinates = coordinate_text.split("\n")

            for pts_cpt in range(len(coordinates)):
                if coordinates[pts_cpt] is not "":
                    test_v = self.enlever_null_string(coordinates[pts_cpt].split(" "))

                    pts = MSACenterlinePoint()

                    pts.set_abscissa(float(test_v[0]))
                    pts.set_ordinate(float(test_v[1]))
                    pts.set_isometric(float(test_v[2]))

                    if ret.is_point_existed(pts):
                        pts.set_id(ret.get_index_by_points(pts))
                        branch.append(pts)
                    else:
                        pts.set_id(pts_count)
                        branch.append(pts)
                        pts_count += 1
            ret.append(branch)

        ret.init_total_centerline_point_graph(pts_count)
        ret.do_fill_total_graph()

        sparse_point_count = ret.set_sparse_point()
        ret.init_sparse_centerline_point_graph(sparse_point_count)
        ret.do_fill_sparse_graph()

        return ret

    def enlever_null_string(self, str_list):
        ret = list()
        for i in range(len(str_list)):
            if str_list[i] is not "":
                ret.append(str_list[i])
        return ret














