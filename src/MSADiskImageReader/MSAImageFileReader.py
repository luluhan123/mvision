import threading
import time
import mmap
import numpy as np
import SimpleITK as sitk
import vtk


class ImageFileReader:
    # this class represent all the titleNames and values in the file
    def __init__(self):
        self.fileName = ""
        self.fileType = ""
        self.filePath = ""
        self.rowCount = 0
        self.columnCount = 0
        self.titles = []
        self.values = []
        self.csv_file_parse_thread = threading.Thread(None, self.do_parse_csv_file)

    def set_file_path(self, file_path):
        self.filePath = file_path

    def load(self):
        ret = None
        if self.filePath.__contains__('mhd') or self.filePath.__contains__('mha'):
            ret = self.raw_file_reader_using_simpleitk()
        return ret

    def raw_file_reader(self):
        meta_reader = vtk.vtkMetaImageReader()
        meta_reader.SetFileName(self.filePath)
        meta_reader.Update()

        return meta_reader.GetOutput()

    def raw_file_reader_using_simpleitk(self):
        return sitk.GetArrayFromImage(sitk.ReadImage(self.filePath))

    def do_parse_csv_file(self):
        start = time.time()
        values = list()
        with open(self.filePath, "r+b") as f:
            # memory-mapInput the file, size 0 means whole file
            mapInput = mmap.mmap(f.fileno(), 0)
            # read content via standard file methods
            cpt = 0
            for s in iter(mapInput.readline, ""):
                s = s.translate(None, "\r\n")
                if cpt == 0:
                    title_list = s.split(";")
                    self.set_title_list(title_list)
                    print (title_list)
                else:
                    a_line_of_values = s.split(";")
                    values.append(a_line_of_values)
                cpt += 1

            self.set_values(values)
            self.set_row_count(len(values))
            mapInput.close()
            end = time.time()
            print ("Time for completion",end-start)
