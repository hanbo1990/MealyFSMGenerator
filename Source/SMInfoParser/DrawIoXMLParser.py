# -*- coding: UTF-8 -*-

import xml.sax
from os.path import isfile
from SMInfoParser.StateMachineInfo import StateJumpInfo
from SMInfoParser.StateMachineInfoParser import SMInfoParser

SM__STATE_JUMP = "state jump"
SM__STATE_JUMP_PARENT = "state jump parent"
SM__STATE = "state"


class StateMachineInfoExtractor(SMInfoParser):
    """
    State Machine information extractor, this class help extract information from draw.io graph
    """

    def __init__(self):
        # create a xml sax parser
        self.parser = xml.sax.make_parser()
        # turn off name spaces
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.state_machine_content_handler = self.__StateMachineContentHandler()
        self.parser.setContentHandler(self.state_machine_content_handler)
        pass

    def get_sm_jump_info_list_from_file(self, file_path):
        """
        Get state machine information from draw io xml file.
        :param file_path: path to the file
        :return:
        """
        if isfile(file_path) is False or ".xml" not in file_path:
            raise ValueError("Invalid input path. expect a xml file with valid path\n")

        # parse the xml file
        self.parser.parse(file_path)

        return self.__sort_list(self.state_machine_content_handler.state_jump_list)

    @staticmethod
    def __sort_list(st_list):
        ret_list = []
        state_list = []
        for item in st_list:
            if item.from_state not in state_list:
                state_list.append(item.from_state)

        state_list.sort()

        for state in state_list:
            state_st_list = []
            for item in st_list:
                if item.from_state is state:
                    state_st_list.append(item)
            state_st_list.sort(key=lambda x: x.condition)
            for item in state_st_list:
                ret_list.append(item)

        return ret_list


    class __StateMachineContentHandler(xml.sax.ContentHandler):

        def __init__(self):
            super()
            self.xml_item_list = []
            self.state_id_to_key = {}
            self.currentItem = None
            self.state_jump_list = []

        def startElement(self, tag, attributes):
            if tag == "mxCell":
                self.currentItem = self._XmlItem()
                if "style" in attributes.keys():
                    # if the style contains rounded, meaning it's a state
                    if "whiteSpace" in attributes["style"]:
                        if "value" in attributes.keys():
                            self.currentItem.id = attributes["id"]
                            self.currentItem.type = SM__STATE
                            self.currentItem.value = attributes["value"]
                    else:
                        if "source" in attributes.keys() and "target" in attributes.keys():
                            if attributes["parent"] == '1':
                                if "value" in attributes.keys() and attributes["value"] is not "":
                                    self.currentItem.type = SM__STATE_JUMP
                                    self.currentItem.value = attributes["value"]
                                    self.currentItem.source = attributes["source"]
                                    self.currentItem.target = attributes["target"]
                                else:
                                    self.currentItem.id = attributes["id"]
                                    self.currentItem.type = SM__STATE_JUMP_PARENT
                                    self.currentItem.source = attributes["source"]
                                    self.currentItem.target = attributes["target"]
                                    print("find parent, "
                                          + str(self.currentItem.source) +
                                          self.currentItem.target +
                                          str(self.currentItem.id))
                        else:
                            # it's a line and source, target info is inside its parent
                            if "value" in attributes.keys() and attributes["parent"] != '1':
                                self.currentItem.type = SM__STATE_JUMP
                                self.currentItem.value = attributes["value"]
                                self.currentItem.parentId = attributes["parent"]

        def endElement(self, tag):
            if tag == "mxCell":
                if self.currentItem.type == SM__STATE_JUMP:
                    if len(self.currentItem.value.split("<br>")) in [2, 3]:
                        self.currentItem.condition = self.currentItem.value.split("<br>")[0]
                        self.currentItem.action = self.currentItem.value.split("<br>")[1]
                elif self.currentItem.type == SM__STATE:
                    self.state_id_to_key[self.currentItem.id] = self.currentItem.value
                else:
                    pass

                self.xml_item_list.append(self.currentItem)
                self.currentItem = None

        def endDocument(self):
            for item in self.xml_item_list:
                if item.type == SM__STATE_JUMP:
                    state_jump_info = StateJumpInfo()
                    if item.source is None:
                        state_jump_info.from_state, state_jump_info.to_state = self._get_from_to_state(item.parentId)
                    else:
                        state_jump_info.from_state = item.source
                        state_jump_info.to_state = item.target
                    if state_jump_info.from_state is not None:
                        state_jump_info.action = item.action
                        state_jump_info.condition = item.condition
                        state_jump_info.from_state = self.state_id_to_key[state_jump_info.from_state]
                        state_jump_info.to_state = self.state_id_to_key[state_jump_info.to_state]
                        self.state_jump_list.append(state_jump_info)

        def _get_from_to_state(self, parent_id):
            for item in self.xml_item_list:
                if item.type == SM__STATE_JUMP_PARENT and parent_id == item.id:
                    return item.source, item.target
            return None, None

        class _XmlItem:

            def __init__(self):
                self.type = None
                self.id = None
                self.parentId = None
                self.value = None

                self.source = None
                self.target = None

                self.condition = None
                self.action = None
                self.from_state = None
                self.to_state = None


