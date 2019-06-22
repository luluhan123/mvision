import vtk


class MSA3DImageReaderInterface:
    """
        l'interface pour charger tous les types de image medicale
    """

    def __init__(self):
        self.file_path = str('')
        self.img = None

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_output(self):
        return self.img

    def load_mhd_image(self):
        meta_reader = vtk.vtkMetaImageReader()
        meta_reader.SetFileName(self.file_path)
        meta_reader.Update()
        self.img = meta_reader.GetOutput()

    def load(self):
        if self.file_path.__contains__("mhd") or self.file_path.__contains__("mha"):
            self.load_mhd_image()
