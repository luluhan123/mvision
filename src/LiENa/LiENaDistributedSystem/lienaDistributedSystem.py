from LiENa.LiENaDistributedSystem.lienaDistributedModule import LienaDistributedModule
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from LiENa.LiENaBasic.lienaDefinition import *


class LienaDistributedSystem(QObject):

    needToRestartServer = pyqtSignal()

    def __init__(self, global_parameter):
        super(LienaDistributedSystem, self).__init__()
        self.globalParameter = global_parameter
        self.moduleIndex = 0
        self.devicesIDs = list()
        self.distributedModules = list()

    def launch_recovery_procedure(self, device_id):
        print("LienaDistributedSystem | launch_recovery_procedure", device_id)

    def check_module_by_addr(self, addr):
        ret = False
        for module in self.distributedModules:
            if module.get_address() == addr:
                ret = True
        return ret

    def close_session_by_device_id(self, device_id):
        for module in self.distributedModules:
            if module.get_device_id() == device_id:
                module.close_session_request(device_id)

    def set_robotic_system_module(self, devices_ids):
        self.devicesIDs = devices_ids

    def generate_reception_channel_by_addr(self, addr, socket_for_reception):
        if DEBUG:
            print("LienaDistributedSystem | generate_reception_channel_by_addr")
        for module in self.distributedModules:
            if module.get_address() == addr:
                if module.is_in_diagnosis():
                    module.repair_reception_channel(socket_for_reception)
                else:
                    module.generate_reception_channel(socket_for_reception)

    def create_distributed_module_with_reception_channel(self, socket_for_reception):
        if DEBUG:
            print("LienaDistributedSystem | create_distributed_module_with_reception_channel")
        module = LienaDistributedModule(self.moduleIndex, self.globalParameter)
        module.lostConnexion[int].connect(self.launch_recovery_procedure)
        module.generate_reception_channel(socket_for_reception)
        self.distributedModules.append(module)
        self.moduleIndex += 1

    def restart_server(self):
        self.needToRestartServer.emit()

    def create_distributed_module_with_transmission_channel(self, target_device_id, motivate, addr, port):
        module = LienaDistributedModule(self.moduleIndex, self.globalParameter)

        module.lostConnexion[int].connect(self.launch_recovery_procedure)
        module.restartServer.connect(self.restart_server)

        module.set_device_id(target_device_id)
        ret = module.generate_transmission_channel(motivate, addr, port)

        if ret == 0:
            if DEBUG:
                print("LienaDistributedSystem | successful create a distributed module with transmission channel")
            self.distributedModules.append(module)
            self.moduleIndex += 1
            return True
        else:
            if DEBUG:
                print("LienaDistributedSystem | failed create a distributed module with transmission channel")
            return False

    def clear(self):
        self.moduleIndex = 0
        self.distributedModules.clear()

    def append(self, moudle):
        self.distributedModules.append(moudle)

    def get_module_count(self):
        return self.distributedModules.size()

    def get_module_index_by_id(self, device_id):
        ret = 1
        len = self.get_module_count()
        for i in len:
            if self.distributedModules[i].get_device_id == device_id:
                ret = self.distributedModules[i].get_index()
        return ret

    def set_device_id_by_index(self, index, device_id):
        self.distributedModules[index].set_device_id(device_id)
