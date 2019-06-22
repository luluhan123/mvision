import threading
import time
import os
import mmap
import numpy as np
from vtk.util import numpy_support as nps
import vtk
import math


class XRayImage:
    # this class represent all the titleNames and values in the file
    def __init__(self):
        self.fileName = ""
        self.filePath = ""
        self.fileType = ""
        self.filePath = ""
        self.displayed = False
        self.saved = False

        self.xRayImageWidth = 0
        self.xRayImageHeight = 0

        self.imageInString = None
        self.imageInVTK = None
        self.filteredValues = None
        self.localFilteredValues = None
        self.traceredPoint = None
        self.actor = None
        self.keyPoints = list()
        self.ridgePoint = list()
        self.img = None
        self.groundTruthCount = 0
        self.groundTruth = list()
        self.guidewireTip = []

    def remove_guidewire_point(self, pt):
        offset = 0
        print(pt, "to be removed")
        newOffset = math.sqrt((self.guidewireTip[-1][0] - pt[0]) ** 2 + (self.guidewireTip[-1][1] - pt[1]) ** 2)

        if newOffset > 5:
            self.guidewireTip.pop(-1)

        if len(self.guidewireTip) > 1:
            for i in range(len(self.guidewireTip)):
                # print(self.guidewireTip[i])
                offset = math.sqrt((self.guidewireTip[i][0] - pt[0]) ** 2 + (self.guidewireTip[i][1] - pt[1]) ** 2)
                if offset < 1.0:
                    self.guidewireTip.pop(i)
        pass

    def set_guidewire_point(self, pt):
        self.guidewireTip.append(pt)

    def clear_guidewire_point(self):
        self.guidewireTip.clear()

    def get_guidewire_tip(self):
        return self.guidewireTip

    def print_guidewire_tip(self):
        print (" -----------------  ")
        for pt in self.guidewireTip:
            print(pt[0], ';', pt[1])
        print(" -----------------  ")

    def create_groud_truth_sequence(self):
        self.groundTruth.append(list())

    def ground_truth_existed(self, index):
        if len(self.groundTruth) > index:
            return True

    def set_ground_truth_point(self, index, pos):
        self.groundTruth[index].append(pos)

    def remove_point_in_ground_truth(self, pos):
        if pos in self.groundTruth:
            self.groundTruth.pop(self.groundTruth.index(pos))

    def find_ground_truth_existed(self):
        temp = self.filePath.split('.')
        values = list()

        file_name = temp[0] + '.csv'
        if os.path.exists(file_name):
            with open(temp[0] + '.csv', "r+b") as f:
                # memory-mapInput the file, size 0 means whole file
                mapInput = mmap.mmap(f.fileno(), 0)
                # read content via standard file methods
                cpt = 0
                for s in iter(mapInput.readline, ""):
                    s = s.translate(None, "\r\n")
                    a_line_of_values = s.split(";")
                    self.groundTruth.append((int(a_line_of_values[0]), int(a_line_of_values[1])))
                    cpt += 1
                mapInput.close()

    def get_tv_optimise_points(self):
        pts = list()
        temp = self.filePath.split('.')
        file_name = temp[0] + '_ridge_normalisetv.txt'

        if os.path.exists(file_name):
            with open(file_name, "r+b") as f:
                if os.stat(file_name).st_size != 0:
                    mapInput = mmap.mmap(f.fileno(), 0)
                    for s in iter(mapInput.readline, ""):
                        s = s.translate(None, "\r\n")
                        a_line_of_values = s.split(" ")
                        pts.append((int((float(a_line_of_values[0]) + 2)*192.0/4), int((float(a_line_of_values[1]) + 2)*192.0/4)))
                    mapInput.close()
        return pts

    def save_ridge_points(self):
        temp = self.filePath.split('.')
        f = open(temp[0] + '_ridge.csv', 'w')

        for l in self.ridgePoint:
            if l[0] < 5 or l[0] > 507:
                continue

            if l[1] < 5 or l[1] > 507:
                continue

            f.write(str(l[0]) + ' ' + str(l[1]) + '\n')

        f.close()

    def renew_image(self):

        temp = self.filePath.split('.')
        file_name = temp[0] + '_ridge.raw'
        mhd_name = temp[0] + '_ridge.mhd'

        #pts = self.ridgePoint

        for y in range(512):
            for x in range(512):
                if (x, 511 - y) not in self.ridgePoint:
                    self.imageInVTK.SetScalarComponentFromFloat(x, 511 - y, 0, 0, float(0))

        writer = vtk.vtkMetaImageWriter()
        writer.SetInputData(self.imageInVTK)
        writer.SetCompression(False)
        writer.SetFileName(mhd_name)
        writer.SetRAWFileName(file_name)
        writer.Write()

    def get_rig_points(self):
        pts = list()
        temp = self.filePath.split('.')
        file_name = temp[0] + '_ridge.txt'

        with open(file_name, "r+b") as f:
            if os.stat(file_name).st_size != 0:
                mapInput = mmap.mmap(f.fileno(), 0)
                for s in iter(mapInput.readline, ""):
                    s = s.translate(None, "\r\n")
                    a_line_of_values = s.split(" ")
                    pts.append((int(a_line_of_values[0]), int(a_line_of_values[1])))
                mapInput.close()
        return pts

    def save_ground_truth(self):
        temp = self.filePath.split('.')
        f = open(temp[0]+'.csv', 'w')
        for l in self.groundTruth:
            f.write(str(l[0]) + ';' + str(l[1]) + '\n')
        f.close()

    def get_ground_truth(self):
        return self.groundTruth

    def save(self,path):
        open(path, "wb").write(self.imageInString)

    def set_state_saved(self):
        self.saved = True

    def get_saved_state(self):
        return self.saved

    def set_state_displayed(self):
        self.displayed = True

    def get_displayed_state(self):
        return self.displayed

    def set_image_width(self, width):
        self.xRayImageWidth = width

    def set_image_height(self, height):
        self.xRayImageHeight = height

    def get_image_width(self):
        return self.xRayImageWidth

    def get_image_height(self):
        return self.xRayImageHeight

    def get_filename(self):
        return self.filePath

    def set_filename(self, filename):
        self.filePath = filename

    def get_file_type(self):
        return self.fileType

    def set_file_type(self, file_type):
        self.fileType = file_type

    def get_values(self):
        return self.imageInVTK

    def set_local_filtered_values(self, local_filtered_value):
        self.localFilteredValues = local_filtered_value

    def get_local_filtered_values(self):
        return self.localFilteredValues

    def set_filtered_values(self, filtered_value):
        self.filteredValues = filtered_value

    def get_filtered_values(self):
        return self.filteredValues

    def set_tracered_point(self,tracered_point):
        self.traceredPoint = tracered_point

    def get_tracered_point(self):
        return self.traceredPoint

    def set_rig_points(self, point):
        self.ridgePoint = point

        pts_reduced = list()

        for l in self.ridgePoint:
            if l[0] < 5 or l[0] > 507:
                continue

            if l[1] < 5 or l[1] > 507:
                continue

            pts_reduced.append(l)

        self.ridgePoint = pts_reduced

        for y in xrange(512):
            for x in xrange(512):
                if not self.pts_existed((x, y)):
                    self.imageInVTK.SetScalarComponentFromFloat(x, y, 0, 0, float(0))

        temp = self.filePath.split('.')
        file_name = temp[0] + '_ridge.raw'
        mhd_name = temp[0] + '_ridge.mhd'

        writer = vtk.vtkMetaImageWriter()
        writer.SetInputData(self.imageInVTK)
        writer.SetCompression(False)
        writer.SetFileName(mhd_name)
        writer.SetRAWFileName(file_name)
        writer.Write()

    def save_enhanced_image(self,vtk_img):
        temp = self.filePath.split('.')
        file_name = temp[0] + '_ridge.raw'
        mhd_name = temp[0] + '_ridge.mhd'

        writer = vtk.vtkMetaImageWriter()
        writer.SetInputData(vtk_img)
        writer.SetCompression(False)
        writer.SetFileName(mhd_name)
        writer.SetRAWFileName(file_name)
        writer.Write()

        self.imageInVTK = vtk_img

    def pts_existed(self, pts):
        for p in self.ridgePoint:
            if (p[0] == pts[0]) and (p[1] == pts[1]):
                return True
                break
        return False

    def set_key_points(self, point):
        self.keyPoints.append(point)

    def get_key_points(self):
        return self.keyPoints

    def set_image_to_numpy(self, input):
        dim = input.GetDimensions()
        flat_v = nps.vtk_to_numpy(input.GetPointData().GetScalars())
        img = flat_v.reshape(dim[0], dim[1], dim[2])
        self.img = img[:, :, 0]

    def do_decode(self, input):
        self.imageInString = input
        image_data = vtk.vtkImageData()
        image_data.SetDimensions(self.xRayImageWidth, self.xRayImageHeight, 1)
        image_data.AllocateScalars(vtk.VTK_UNSIGNED_SHORT, 1)

        for y in range(self.xRayImageHeight):
            for x in range(self.xRayImageWidth):
                image_data.SetScalarComponentFromFloat(x, self.xRayImageHeight - 1 - y, 0, 0, float(int(ord(input[y * self.xRayImageHeight + x]))))
        self.imageInVTK = image_data

    def raw_file_reader(self, path):
        f = open(path, 'r+b')
        v = f.read()

        image_data = vtk.vtkImageData()
        image_data.SetDimensions(self.xRayImageWidth, self.xRayImageHeight, 1)
        image_data.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)

        for y in range(self.xRayImageHeight):
            for x in range(self.xRayImageWidth):
                image_data.SetScalarComponentFromFloat(x, self.xRayImageHeight - 1 - y, 0, 0, float(int(ord(v[y * self.xRayImageHeight + x]))))
        self.imageInVTK = image_data

    def get_file_name(self):
        return self.fileName

    def raw_file_reader_by_vtk(self, path, filename, file_size):
        self.filePath = path
        self.fileName = self.filePath.split('/')[-1]
        # print self.fileName
        image_reader = vtk.vtkImageReader()
        image_reader.SetFileName(path)
        image_reader.SetNumberOfScalarComponents(1)
        image_reader.SetDataExtent(0, self.xRayImageWidth - 1, 0, self.xRayImageHeight - 1, 0, 0)

        if file_size == 262144:
            image_reader.SetDataScalarTypeToUnsignedChar()
        elif file_size == 262144*2:
            image_reader.SetDataScalarTypeToShort()
        elif file_size == 1048576:
            image_reader.SetDataByteOrderToLittleEndian()
            image_reader.SetDataScalarTypeToInt()
        elif file_size == 32768:
            image_reader.SetDataScalarTypeToShort()
        else:
            image_reader.SetDataScalarTypeToUnsignedShort()
        image_reader.Update()
        self.imageInVTK = image_reader.GetOutput()

        icon_folder_path = (path.split(filename)[0] + "icon/"+filename).split('.')[0] + '.png'
        if not os.path.exists(icon_folder_path):
            writer = vtk.vtkPNGWriter()
            writer.SetFileName(icon_folder_path)
            writer.SetInputData(self.imageInVTK)
            writer.Write()

    def numpy_to_vtk(img, spacing=[1.0, 1.0, 1.0]):

        importer = vtk.vtkImageImport()

        img_data = img.astype('uint8')
        img_string = img_data.tostring()  # type short
        dim = img.shape

        importer.CopyImportVoidPointer(img_string, len(img_string))
        importer.SetDataScalarType(vtk.VTK_UNSIGNED_CHAR)
        importer.SetNumberOfScalarComponents(1)

        extent = importer.GetDataExtent()
        importer.SetDataExtent(extent[0], extent[0] + dim[2] - 1,
                               extent[2], extent[2] + dim[1] - 1,
                               extent[4], extent[4] + dim[0] - 1)
        importer.SetWholeExtent(extent[0], extent[0] + dim[2] - 1,
                                extent[2], extent[2] + dim[1] - 1,
                                extent[4], extent[4] + dim[0] - 1)

        importer.SetDataSpacing(spacing[0], spacing[1], spacing[2])
        importer.SetDataOrigin(0, 0, 0)

        return importer
