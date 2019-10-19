from abc import ABCMeta, abstractmethod


class SMInfoParser(metaclass=ABCMeta):
    
    state_jump_info = []

    @abstractmethod
    def get_sm_jump_info_list_from_file(self, file_path):
        pass
