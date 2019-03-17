#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.sax
from Source.DrawIoXMLParser.StateMachineInfo import StateJumpInfo
from os.path import isfile

SM__STATE_JUMP = "state jump"
SM__STATE = "state"


class StateMachineInfoExtractor:
    """
    State Machine information extractor, this class help extract information from draw.io graph
    """

    state_jump_info = []

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

        # return state jump information list
        self.state_machine_content_handler.state_jump_list.sort(key=lambda x: x.from_state)
        return self.state_machine_content_handler.state_jump_list

    class __StateMachineContentHandler(xml.sax.ContentHandler):

        def __init__(self):
            super()
            self.type = None
            self.id = None
            self.value = None
            self.source = None
            self.target = None
            # list containing all state key
            self.state_id_to_key = {}
            # list containing all state jump information
            self.state_jump_list = []

        def startElement(self, tag, attributes):
            if tag == "mxCell":
                if "source" in attributes.keys() and "target" in attributes.keys():
                    self.value = attributes["value"]
                    self.type = SM__STATE_JUMP
                    self.source = attributes["source"]
                    self.target = attributes["target"]
                else:
                    if "value" in attributes.keys():
                        self.type = SM__STATE
                        self.id = attributes["id"]
                        self.value = attributes["value"]

        def endElement(self, tag):
            if tag == "mxCell":
                if self.type == SM__STATE_JUMP:
                    if len(self.value.split("<br>")) == 3:
                        sm_jump_info = StateJumpInfo()
                        sm_jump_info.from_state = self.source
                        sm_jump_info.to_state = self.target
                        sm_jump_info.condition = self.value.split("<br>")[0]
                        sm_jump_info.action = self.value.split("<br>")[1]
                        self.state_jump_list.append(sm_jump_info)
                elif self.type == SM__STATE:
                    self.state_id_to_key[self.id] = self.value

        def endDocument(self):
            for sm_jump_info in self.state_jump_list:
                if sm_jump_info.from_state in self.state_id_to_key.keys() and\
                   sm_jump_info.to_state in self.state_id_to_key.keys():
                    sm_jump_info.from_state = self.state_id_to_key[sm_jump_info.from_state]
                    sm_jump_info.to_state = self.state_id_to_key[sm_jump_info.to_state]
                else:
                    raise RuntimeError("Arrow is not connected properly")
