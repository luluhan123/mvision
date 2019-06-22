from PyQt5.QtCore import QObject


class MSACenterlinePointGraph(QObject):
    def __init__(self):
        super(MSACenterlinePointGraph, self).__init__()
        self.graph = []

    def print(self):
        line_count = len(self.graph)
        for i in self,line_count:
            print_content = ""
            for j in range(line_count):
                if self.graph[i][j]:
                    print_content += 1
                else:
                    print_content += 0
        print(print_content)

    def get_sparse_point_count(self):
        ret = 0
        line_count = len(self.graph)

        for i in range(line_count):
            if self.do_ckeck_graph_by_line(i) is not 2:
                ret += 1
        return ret

    def do_check_graph_by_line(self, y):
        cpt = 0
        for i in range(len(self.graph)):
            if self.graph[i][y]:
                cpt += 1
        return cpt

    def set_value(self, x, y, value):
        self.graph[x][y] = value

    def init(self, pts_count):

        for i in range(pts_count):
            line = list()
            self.graph.append(line)

            for j in range(pts_count):
                self.graph[i].append(False)

        print ("graph", len(self.graph), len(self.graph[0]))

    def get_graph_size(self):
        return len(self.graph)

    def get_value(self, x, y):
        return self.graph[x][y]
