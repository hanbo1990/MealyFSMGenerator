# -*- coding: UTF-8 -*-
from SMInfoParser.StateMachineInfo import StateJumpInfo
from SMInfoParser.StateMachineInfoParser import SMInfoParser
from re import (findall,
                sub)

class GraphvizSMInfoExtractor(SMInfoParser):
    """
    State Machine information extractor, this class help extract information from graphviz graph
    """

    def __init__(self):
        pass

    def get_sm_jump_info_list_from_file(self, file_path):
        """
        Get state machine information from graphviz dot file.
        :param file_path: path to the file
        :return:
        """
        state_machine_content_handler = self.__StateMachineContentHandler(file_path)
        return state_machine_content_handler.get_transition_list()


    class __StateMachineContentHandler():
        
        __transition_list = None

        def __init__(self, file_path):
            if ".dot" not in file_path:
                raise RuntimeError("Please use '.dot' file")
            
            self.__update_transitions_list(file_path)
            self.__transition_list = self.__sort_list(self.__transition_list)
            pass
        

        def get_transition_list(self):
            return self.__transition_list


        def __update_transitions_list(self, file_path):
            state_name_dict = {}
            self.__transition_list = []

            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines: # find state symbol-name pair
                    # has label but no transition symbol, it's a state, get the name from it
                    if '->' not in line and 'label' in line:
                        state_symbol = line.split("[")[0]
                        state_symbol = sub(r'\s', "", state_symbol)
                        state_name = findall(r'label="[1-9|a-z|A-Z|_]+', line)[0]
                        state_name = state_name.split('"')[1]
                        state_name_dict[state_symbol] = state_name
                
                for line in lines: # find transition
                    if '->' in line and 'label' in line:
                        state_jump_info = StateJumpInfo()
                        line = sub(r'\s', "", line)

                        states = line.split('[')[0]
                        from_state, to_state = states.split('->')
                        transition = findall(r'label="[1-9|a-z|A-Z|_|\\n]+', line)[0]
                        transition = transition.split('"')[1]

                        state_jump_info.condition, state_jump_info.action = transition.split("\\n")
                        state_jump_info.from_state = state_name_dict[from_state]
                        state_jump_info.to_state = state_name_dict[to_state]

                        self.__transition_list.append(state_jump_info)

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
