# -*- coding: UTF-8 -*-
from SMInfoParser.StateMachineInfo import StateJumpInfo
from SMInfoParser.StateMachineInfoParser import SMInfoParser
from re import (findall,
                sub)
from bs4 import BeautifulSoup

class DrawioSMInfoExtractor(SMInfoParser):
    """
    State Machine information extractor, this class help extract information from draw.io graph
    """

    def __init__(self):
        pass

    def get_sm_jump_info_list_from_file(self, file_path):
        """
        Get state machine information from draw io xml file.
        :param file_path: path to the file
        :return:
        """
        if ".xml" not in file_path:
            raise ValueError("xml file expected but get " + file_path)
        state_machine_content_handler = self.__StateMachineContentHandler(file_path)
        return state_machine_content_handler.get_transition_list()


    class __StateMachineContentHandler():
        
        __soup = None
        __transition_list = None


        def __init__(self, file_path):
            self.__soup = BeautifulSoup(open(file_path), "xml")
            # find cells with useful information
            for br in self.__soup.find_all("br"):
                br.replace_with("\n")

            cells = \
                [item for item in self.__soup.findAll(name="mxCell") \
                if item is not None and "value" in item.attrs.keys() \
                and item["value"]!= ""]
            
            self.__update_transitions_list(cells, self.__get_state_id_mapping_dict(cells))
            self.__transition_list = self.__sort_list(self.__transition_list)
            pass
        

        def get_transition_list(self):
            return self.__transition_list


        def __update_transitions_list(self, cells, state_id_dict):
            self.__transition_list = []
            err_str = 'source or target not connected on line where condition is {} and action is {}'
            for cell in cells:
                cell_val = cell.attrs["value"]
                cell_val = sub('<br\s*?>', '\n', cell_val)
                if '\n' in cell_val: # cell is transition
                    state_jump_info = StateJumpInfo()
                    state_jump_info.condition, state_jump_info.action = cell_val.split()
                    if "source" in cell.attrs.keys():
                        try:
                            state_jump_info.from_state = state_id_dict[cell.attrs["source"]]
                            state_jump_info.to_state = state_id_dict[cell.attrs["target"]]
                        except KeyError:
                            raise RuntimeError(err_str.format(state_jump_info.condition, state_jump_info.action))
                    else:  
                        # the source and dest is deinfed in its parnet node (parent here means the parent in drawio, not xml)
                        parent = self.__soup.findAll("mxCell", {"id": cell.attrs["parent"]})
                        if len(parent) == 1:
                            parent = parent[0]

                        try:
                            state_jump_info.from_state = state_id_dict[parent.attrs["source"]]
                            state_jump_info.to_state = state_id_dict[parent.attrs["target"]]
                        except KeyError:
                            raise RuntimeError(err_str.format(state_jump_info.condition, state_jump_info.action))
                    self.__transition_list.append(state_jump_info)


        @staticmethod
        def __get_state_id_mapping_dict(cells):
            state_id_dict = dict()

            for cell in cells:
                cell_val = cell.attrs["value"]
                cell_val = sub('<br\s*?>', '\n', cell_val)
                if '\n' not in cell_val:
                    print(cell.attrs["value"])
                    state_id_dict[cell.attrs["id"]] = cell.attrs["value"]

            return state_id_dict


        @staticmethod
        def __sort_list(st_list):
            ret_list = []
            state_list = []
            for item in st_list:
                if item.from_state not in state_list:
                    state_list.append(item.from_state)
            
            state_list.sort(key=lambda x: findall(r'[0-9]+',x)[0])

            for state in state_list:
                if "2WAIT_FOR_STATION_RES" in state:
                    state = state
                state_st_list = []
                for item in st_list:
                    if item.from_state == state:
                        print(item.from_state)
                        print(item.condition)
                        print(item.to_state)
                        print("")
                        state_st_list.append(item)
                state_st_list.sort(key=lambda x: int(findall(r'^[0-9]+',x.condition)[0]))
                for item in state_st_list:
                    ret_list.append(item)

            return ret_list
