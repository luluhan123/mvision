from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from src.MSAModel.MSAImage.XRayImage import XRayImage
import threading
import os, shutil
import getpass
import sys
import scipy
from vtk.util import numpy_support as nps
from src.MSADiskImageReader.MSAImageFileReader import ImageFileReader


class MSAModel(QObject):
    # signals
    imageSequenceLoaded = pyqtSignal()
    volumeImageLoaded = pyqtSignal()

    def __init__(self, processing_factory, workspace_path=None):
        super(MSAModel, self).__init__()
        self.processing_factory = processing_factory
        self.workspace_path = workspace_path
        path = os.path.dirname(os.path.realpath(__file__))
        temp = path.split("src")
        self.meta_file_path = temp[0] + "dat/msfr.txt"
        self.files = dict()

        self.target_image_width = 512
        self.target_image_height = 512

        self.current_sequence_folder = None
        self.current_sequence_icon_folder = None

        # models
        self.files_count = 0
        self.current_sequence = None

        self.framesLock = threading.Lock()
        self.frames = list()  # x ray fluoroscope sequence
        self.ready = False

        self.opacity_sequence = []
        self.color_sequence = []

        self.inputMessageCache = None
        self.outputMessageCache = None

        #  for windows and color level
        self.global_window_level = 0
        self.global_color_level = 0

        if workspace_path is not None:
            self.find_image_existed()

        self.volumeImageFilePath = None

    # threading.Thread(None, self.do_parse_target_folder).start()

    def centerline_extraction(self, input):
        return self.processing_factory.centerline_extraction(input)

    def set_message_cache(self, input_message, output_message):
        self.inputMessageCache = input_message
        self.outputMessageCache = output_message

    def read_volume_image_by_path(self):
        reader = ImageFileReader()
        reader.set_file_path(self.volumeImageFilePath)
        img_numpy = reader.load()

        folder = self.workspace_path + 'sequence' + str(len(self.files.keys())) + '/'
        os.mkdir(folder)
        os.mkdir(folder + 'icon')
        os.mkdir(folder + 'volume')

        filepath = str(self.volumeImageFilePath)
        temp = filepath.split('/')
        filename = temp[-1]
        print (filename)
        self.save_vtk_image_locally(filepath, folder + 'volume/volume.mha')
        self.save_volume_data_to_local_folder(img_numpy, folder)
        self.find_image_existed()
        self.volumeImageLoaded.emit()

    def do_read_volume_image_by_path(self, filepath):
        self.volumeImageFilePath = filepath
        threading.Thread(None, self.read_volume_image_by_path).start()

    def reinitialiser_base_de_donnee(self):
        self.target_image_width = 512
        self.target_image_height = 512
        self.current_sequence_folder = None
        self.current_sequence_icon_folder = None
        self.files_count = 0
        self.current_sequence = None

        self.frames = list()  # x ray fluoroscope sequence
        self.ready = False

    def find_image_existed(self):
        self.files.clear()
        for folder_name in os.listdir(self.workspace_path):
            if folder_name.__contains__('sequence'):
                self.files[folder_name] = list()
                for filename in os.listdir(self.workspace_path + '/' + folder_name + '/'):
                    if filename.__contains__('navi') and filename.__contains__('.raw'):
                        self.files[folder_name].append(filename)
                self.files[folder_name].sort()

    def check_system_meta_file(self):
        return os.path.isfile(self.meta_file_path)

    def set_global_workspace_by_meta_file(self):
        meta_data = open(self.meta_file_path, 'rb')
        temp = meta_data.read()
        meta_data.close()
        temp = temp.decode()
        temp = temp.replace('\r','').replace('\n','').replace('\t','')
        self.workspace_path = temp
        print ("set_global_workspace_by_meta_file", self.workspace_path)
        self.find_image_existed()

    def set_global_workspace(self, workspace):
        self.workspace_path = workspace

        if self.workspace_path is not None:
            self.find_image_existed()
            self.save_meta_data()

    def save_meta_data(self):
        meta_data = open(self.meta_file_path, 'w')
        meta_data.write(self.workspace_path + '\n')
        meta_data.close()

    def is_global_workspace_configured(self):
        if self.workspace_path is None:
            return False
        else:
            return True

    def get_current_sequence_count(self):
        return len(self.frames)

    def get_part_image_by_size_by_vtk(self, img, center, box_w, box_h, w, h):
        return self.processing_factory.get_part_image_by_size_by_vtk(img, center, box_w, box_h, w, h)

    def set_global_image_size(self, w, h):
        self.target_image_width = w
        self.target_image_height = h

    def get_current_sequence_folder(self):
        ret = None

        if self.current_sequence is not None:
            ret = self.workspace_path + self.current_sequence

        return ret

    @staticmethod
    def save_vtk_image_locally(srcfile, dstfile):
        shutil.move(srcfile, dstfile)

    @staticmethod
    def convert_image_to_numpy(self, input):
        dim = input.GetDimensions()
        flat_v = nps.vtk_to_numpy(input.GetPointData().GetScalars())
        img = flat_v.reshape(dim[0], dim[1], dim[2])
        return img

    def save_volume_data_to_local_folder(self, img, target_path):
        for i in range(0, img.shape[0]):
            slice = img[i, :, :]  # .astype(np.uint16)
            scipy.misc.imsave(target_path + 'icon/' + ''.join(["navi" + str(i).rjust(8, '0')]) + '.png', slice)
            bts = slice.tobytes()
            file = open(target_path + ''.join(["navi" + str(i).rjust(8, '0')]) + '.raw', 'wb+')
            file.write(bts)
            file.close()

    def get_sequence_existed(self):
        seqs = list(self.files.keys())
        self.sort_file_names(seqs)
        return seqs

    def sort_file_names(self, seq):
        length = len(seq)
        for i in range(length-1):
            for j in range(length - 1 - i):
                if int(seq[j].split('sequence')[1]) > int(seq[j+1].split('sequence')[1]):
                    temp = seq[j]
                    seq[j] = seq[j+1]
                    seq[j + 1] = temp
        return seq

    def ridge_point_extraction_key_area(self, key_area):
        return self.processing_factory.ridge_point_extraction_key_area(key_area)

    def execute_ridgepoint_extraction(self, input_img):
        return self.processing_factory.execute_ridgepoint_extraction(input_img)

    def execute_Rpca(self, input_matrix):
        return self.processing_factory.execute_rpca(input_matrix)

    def get_frame_length(self):
        ret = 0
        self.framesLock.acquire()
        ret = len(self.frames)
        self.framesLock.release()
        return ret

    def check_workspace(self):
        for root, dirs, files in os.walk(self.workspace_path):
            dirsLength = len(dirs)
            if dirsLength != 0:
                self.folder_count += dirsLength
            print(self.folder_count)
        return self.folder_count

    def open_new_folder(self):
        # check folder existed
        self.check_workspace()

        self.current_sequence_folder = self.workspace_path + self.folder_prefix + str(self.folder_count + 1) + '/'
        os.mkdir(self.current_sequence_folder)

        threading.Thread(None, self.do_frame_state_check).start()

    def do_frame_state_check(self):
        while True:
            self.framesLock.acquire()
            cpt = 0
            for frame in self.frames:
                if frame.get_displayed_state() and (not frame.get_saved_state()):
                    frame.save(self.current_sequence_folder + self.image_prefix + str(self.image_index + cpt) + '.raw')
                    frame.set_state_saved()
                cpt += 1
            self.framesLock.release()
            threading._sleep(1)

    def set_image_state_by_index(self, index):
        self.frames[index].set_state_displayed()

    def append_new_image(self, img):

        image = XRayImage()
        image.set_image_width(self.target_image_width)
        image.set_image_height(self.target_image_height)
        image.do_decode(img)

        self.framesLock.acquire()
        self.frames.append(image)
        self.framesLock.release()

    def tensor_voting(self, img):
        return self.processing_factory.tensor_voting(img)

    def curve_fitting(self, pts, maximum_point_num__per_cluster, x, y, tolerant_area):
        return self.processing_factory.curve_fitting(pts, maximum_point_num__per_cluster, x, y, tolerant_area)

    def do_curve_fitting(self, pts, maximum_point_num__per_cluster, x, y):
        return self.processing_factory.do_curve_fitting(pts, maximum_point_num__per_cluster, x, y)

    def san_ban_fu(self, img):
        return self.processing_factory.san_ban_fu(img)

    def set_image_to_numpyy(self, input):
        return self.processing_factory.set_image_to_numpyy(input)

    def set_total_image_to_numpy(self, input):
        return self.processing_factory.set_total_image_to_numpy(input)

    def numpy_to_vtk(self, input):
        return self.processing_factory.numpy_to_vtk(input)

    def convertt(self, input):
        return self.processing_factory.convertt(input)

    def get_part_NPimage(self, input, centre):
        return self.processing_factory.get_part_NPimage(input, centre)

    def get_part_image_by_size(self, input, center, radius):
        return self.processing_factory.get_part_image_by_size(input, center, radius)

    def predict_movement(self, input):
        return self.processing_factory.predict_movement(input)

    def do_surf_processing(self, input, threshold=250):
        return self.processing_factory.do_surf_processing(input, threshold)

    def frangi_img(self, img):
        return self.processing_factory.frangi_img(img)

    def do_predict_possible_points(self, pts):
        return self.processing_factory.do_predict_possible_points(pts)

    def init_get_part_NPimage(self, input):
        return self.processing_factory.init_get_part_NPimage(input)

    def set_image_to_numpy(self, input):
        return self.processing_factory.set_image_to_numpy(input)

    def enhance_local_guide_wire(self, input):
        return self.processing_factory.enhance_local_guide_wire(input)

    def enhance_guide_wire(self, input):
        return self.processing_factory.enhance_guide_wire(input)

    def surf_guide_wire(self, input):
        return self.processing_factory.surf_guide_wire(input)

    def get_image_by_index(self, index):
        ret = None
        self.framesLock.acquire()
        l = len(self.frames)
        if l != 0 and index < l:
            ret = self.frames[index]
        self.framesLock.release()
        return ret

    def get_image_by_name(self, name):
        ret = None
        for frame in self.frames:
            if name in frame.get_file_name():
                ret = frame.get_values()
                break
        return ret

    def is_target_loaded(self):
        return self.ready

    def get_files_number(self):
        return self.files_count

    def get_target_folder_path(self):
        return self.current_path

    def get_current_sequence_icon_folder(self):

        if sys.platform == 'darwin':
            img_path = self.workspace_path + self.current_sequence + '/icon/'
        elif sys.platform == 'win32':
            img_path = self.workspace_path + self.current_sequence + '\\icon\\'
        else:
            img_path = self.workspace_path + self.current_sequence + '/icon/'
        return img_path

    def get_current_taget_folder(self):
        if sys.platform == 'darwin':
            img_path = self.workspace_path + self.current_sequence + '/'
        elif sys.platform == 'win32':
            img_path = self.workspace_path + self.current_sequence + '\\'
        else:
            img_path = self.workspace_path + self.current_sequence + '/'
        return img_path

    def do_parse_target_folder(self):
        self.files_count = len(self.files[self.current_sequence])

        cpt = 0
        file_size = 0
        for img in self.files[self.current_sequence]:
            # if existed, start processing
            if sys.platform == 'darwin':
                img_path = self.workspace_path + self.current_sequence + '/' + img
            elif sys.platform == 'win32':
                img_path = self.workspace_path + self.current_sequence + '\\' + img
            else:
                img_path = self.workspace_path + self.current_sequence + '/' + img

            if os.path.exists(img_path):
                if cpt == 0:
                    fo = open(img_path, "rb")
                    file_size = len(fo.read())
                    # print file_size
                    fo.close()
                self.do_read_image_by_path(img_path, img, file_size)
            cpt += 1

        self.ready = True
        self.imageSequenceLoaded.emit()

    def set_current_sequence_path(self, current_sequence):
        self.ready = False
        self.frames = []
        self.current_sequence = current_sequence

        threading.Thread(None, self.do_parse_target_folder).start()

    def do_read_image_by_path(self, path, filename, file_size):
        raw_file_image = XRayImage()
        raw_file_image.set_image_width(self.target_image_width)
        raw_file_image.set_image_height(self.target_image_height)
        raw_file_image.raw_file_reader_by_vtk(path, filename, file_size)
        self.frames.append(raw_file_image)

    def count_file(self, dir_name):
        extens = [".raw"]
        for root, dirs, fileNames in os.walk(dir_name):
            for f in fileNames:
                if '.' not in f:
                    continue
                try:
                    ext = f[f.rindex('.'):]
                    if extens.count(ext) > 0:
                        self.files_count += 1
                except:
                    print("Error occur!")
                    pass

    def remove_noise_kmeans_method(self, ridge_point, key_point):
        return self.processing_factory.remove_noise_kmeans_method(ridge_point, key_point)

