from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class MSAController(QObject):

    # signals
    imageSequenceLoaded = pyqtSignal()
    volumeImageLoaded = pyqtSignal()
    newConnection = pyqtSignal()

    def __init__(self, model, communication_stack):
        super(MSAController, self).__init__()
        self.model = model
        self.communicationStack = communication_stack
        self.model.imageSequenceLoaded.connect(self.is_image_sequence_loaded)
        self.model.volumeImageLoaded.connect(self.is_volume_imageLoaded)
        self.communicationStack.newConnection.connect(self.get_local_addr_port)

    def centerline_extraction(self, input):
        return self.model.centerline_extraction(input)

    def get_current_taget_folder(self):
        return self.model.get_current_taget_folder()

    def get_local_addr_port(self):
        self.newConnection.emit()

    def get_handshake_commit_addr(self):
        self.communicationStack.get_handshake_commit_addr()

    def get_handshake_commit_port(self):
        return self.communicationStack.get_handshake_commit_port()

    def set_message_cache(self, input_message, output_message):
        self.model.set_message_cache(input_message, output_message)

    def launch_communication_stack(self):
        self.communicationStack.launch()

    def terminate_communication_stack(self):
        self.communicationStack.terminate()

    def do_handshake(self, ip, port):
        self.communicationStack.open_session_request(0, ip, port)

    def channel_close_request(self, device_id):
        self.communicationStack.close_session_request(device_id)

    def close_communication_stack(self):
        self.communicationStack.terminate()

    def reinitialiser_base_de_donnee(self):
        self.model.reinitialiser_base_de_donnee()

    def set_global_workspace(self, workspace):
        self.model.set_global_workspace(workspace)

    def is_global_workspace_configured(self):
        return self.model.is_global_workspace_configured()

    def get_current_sequence_count(self):
        return self.model.get_current_sequence_count()

    def get_part_image_by_size_by_vtk(self, img, center, box_w, box_h, w, h):
        return self.model.get_part_image_by_size_by_vtk(img, center, box_w, box_h, w, h)

    def set_global_image_size(self, w, h):
        self.model.set_global_image_size(w, h)

    def is_image_sequence_loaded(self):
        self.imageSequenceLoaded.emit()

    def check_system_meta_file(self):
        return self.model.check_system_meta_file()

    def set_global_workspace_by_meta_file(self):
        self.model.set_global_workspace_by_meta_file()

    def is_volume_imageLoaded(self):
        self.volumeImageLoaded.emit()

    def do_read_volume_image_by_path(self, filepath):
        self.model.do_read_volume_image_by_path(filepath)

    def get_image_by_name(self, name):
        return self.model.get_image_by_name(name)

    def get_current_sequence_folder(self):
        return self.model.get_current_sequence_folder()

    def get_current_sequence_icon_folder(self):
        return self.model.get_current_sequence_icon_folder()

    def get_sequence_existed(self):
        return self.model.get_sequence_existed()

    def ridge_point_extraction_key_area(self, key_area):
        return self.model.ridge_point_extraction_key_area(key_area)

    def execute_ridgepoint_extraction(self, input_img):
        return self.model.execute_ridgepoint_extraction(input_img)

    def execute_Rpca(self,input_matrix):
        return self.model.execute_rpca(input_matrix)

    def set_image_to_numpyy(self, input):
        return self.model.set_image_to_numpyy(input)

    def set_total_image_to_numpy(self, input):
        return self.model.set_total_image_to_numpy(input)

    def numpy_to_vtk(self, input):
        return self.model.numpy_to_vtk(input)

    def convertt(self, input):
        return self.model.convertt(input)

    def get_part_NPimage(self, input, centre):
        return self.model.get_part_NPimage(input, centre)

    def get_part_image_by_size(self, input, center, radius):
        return self.model.get_part_image_by_size(input, center, radius)

    def predict_movement(self, input):
        return self.model.predict_movement(input)

    def do_surf_processing(self, input, threshold=250):
        return self.model.do_surf_processing(input, threshold)

    def curve_fitting(self, pts, maximum_point_num__per_cluster, x, y, tolerant_area):
        return self.model.curve_fitting(pts, maximum_point_num__per_cluster, x, y, tolerant_area)

    def do_curve_fitting(self, pts, maximum_point_num__per_cluster, x, y):
        return self.model.do_curve_fitting(pts, maximum_point_num__per_cluster, x, y)

    def san_ban_fu(self,img):
        return self.model.san_ban_fu(img)

    def tensor_voting(self, img):
        return self.model.tensor_voting(img)

    def frangi_img(self, img):
        return self.model.frangi_img(img)

    def do_predict_possible_points(self, pts):
        return self.model.do_predict_possible_points(pts)

    def init_get_part_NPimage(self, input):
        return self.model.init_get_part_NPimage(input)

    def set_image_to_numpy(self, input):
        self.model.set_image_to_numpy(input)

    def set_image_state_by_index(self, index):
        self.model.set_image_state_by_index(index)

    def launch_tcp_server(self):
        self.communicationStack.launch_server()

    def terminate_tcp_server(self):
        self.communicationStack.terminate_server()

    def do_read_image_by_path(self, target):
        return self.model.do_read_image_by_path(target)

    def set_current_sequence_path(self, path):
        self.model.set_current_sequence_path(path)

    def get_files_number(self):
        return self.model.get_files_number()

    def is_target_loaded(self):
        return self.model.is_target_loaded()

    def get_image_by_index(self, index):
        return self.model.get_image_by_index(index)

    def enhance_guide_wire(self, input):
        return self.model.enhance_guide_wire(input)

    def surf_guide_wire(self, input):
        return self.model.surf_guide_wire(input)

    def enhance_local_guide_wire(self, input):
        return self.model.enhance_local_guide_wire(input)

    def removeNoiseKmeansMethod(self,ridge_point,key_point):
        return self.model.remove_noise_kmeans_method(ridge_point, key_point)

    def generate_input_cache(self):
        self.communicationStack.generate_input_cache()

    def generate_output_cache(self):
        self.communicationStack.generate_output_cache()
