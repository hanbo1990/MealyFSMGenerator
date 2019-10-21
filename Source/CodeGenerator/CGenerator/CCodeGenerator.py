import os
import errno
import re
import shutil

from CodeGenerator.CodeGenerator import (CodeGenerator,
                                         sm_condition_common,
                                         sm_state_common)
from CodeGenerator.CGenerator.CRelatedDefines import (state_enum_type,
                                                      condition_enum_type,
                                                      transition_name,
                                                      state_type,
                                                      transition_table_name,
                                                      init_func_name,
                                                      tick_func_name,
                                                      header_guard)

RESULT_PATH = "Result"


class CCodeGenerator(CodeGenerator):
    """
    This file help generates .c and .h code for the state machine
    """

    _func_file_name = None
    _header_file_name = None
    _inc_file_name = None
    _h_file_writer = None
    _c_file_writer = None

    def __init__(self, state_machine_name=None):
        super(CCodeGenerator, self).__init__(state_machine_name)

        if not os.path.exists(RESULT_PATH):
            try:
                os.makedirs(RESULT_PATH)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise RuntimeError("Cannot create the folder now")

        self._func_file_name = self._sm_name + "SMFunc.c"
        self._header_file_name = self._sm_name + "SMFunc.h"
        self._inc_file_name = self._sm_name + "SMTable.inc"
        self._prepare_dir()

    def write_file(self, st_list):
        """
        Write to the generated c file
        :param st_list:
        :return:
        """

        prepared_list = self._prepare_st_list(st_list)
        self._write_c_file()
        self._write_inc_file(prepared_list)
        self._write_header_file()
        self._copy_default_files()
        self._create_unit_test(prepared_list)

    def _prepare_dir(self):
        self.__mkdir(RESULT_PATH)
        self.__mkdir(RESULT_PATH + os.sep + "src")
        self.__mkdir(RESULT_PATH + os.sep + "src" + os.sep + "fsmMgr")
        self.__mkdir(RESULT_PATH + os.sep + "unit_test")
        self.__mkdir(RESULT_PATH + os.sep + "unit_test" + os.sep + "test")

    @staticmethod
    def __mkdir(path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise RuntimeError("Cannot create the folder now")

    def _write_c_file(self):
        c_file_writer = open(RESULT_PATH + os.sep + "src" + os.sep + self._func_file_name, 'w+')

        self.__create_include(c_file_writer)
        self.__create_local_variable(c_file_writer)
        self.__create_private_func_define(c_file_writer)
        self.__create_link_to_table(c_file_writer)
        self.__create_private_func_body(c_file_writer)

        c_file_writer.close()

    def __create_link_to_table(self, file_descriptor):
        file_descriptor.write("#include \"" + self._inc_file_name + "\"\n")
        file_descriptor.write("\n")

    def __create_include(self, file_descriptor):
        file_descriptor.write("#include \"MealyFSM.h\"\n")
        file_descriptor.write("#include \"" + self._header_file_name + "\"\n")
        file_descriptor.write("\n")

    def __create_local_variable(self, file_descriptor):
        file_descriptor.write("\n")
        file_descriptor.write("STATIC FSM_t* smHandler;\n")
        file_descriptor.write("\n")

    def __create_private_func_define(self, file_descriptor):
        for item in self._priv_func_name_list:
            file_descriptor.write("STATIC void " + item + "( void );\n")

        file_descriptor.write("\n")

    def __create_private_func_body(self, file_descriptor):
        for item in self._priv_func_name_list:
            priv_func_str = "STATIC void " + item + "( void ){\n" \
                            "\n" \
                            "}\n\n"
            file_descriptor.write(priv_func_str)

    def _write_header_file(self):
        h_file_writer = open(RESULT_PATH + os.sep + "src" + os.sep + self._header_file_name, 'w+')

        h_file_writer.write("#ifndef " + header_guard(self._sm_name) + "\n")
        h_file_writer.write("#define " + header_guard(self._sm_name) + "\n")
        h_file_writer.write("\n")
        h_file_writer.write("#include <stdbool.h>\n")
        h_file_writer.write("\n")
        h_file_writer.write("bool " + init_func_name(self._sm_name) + "( void );\n")
        h_file_writer.write("void " + tick_func_name(self._sm_name) + "( void );\n")
        h_file_writer.write("\n")
        h_file_writer.write("#endif\n")

        h_file_writer.close()

    def _write_inc_file(self, prepared_list):
        table_file_writer = open(RESULT_PATH + os.sep + "src" + os.sep + self._inc_file_name, 'w+')

        self.__create_enumeration(table_file_writer)
        self.__create_transition_table_line_type(table_file_writer)
        self.__create_table(table_file_writer, prepared_list)
        self.__create_init_func(table_file_writer)
        self.__create_tick_func(table_file_writer)

    def __create_enumeration(self, file_descriptor):
        list_nr = len(self._priv_state_name_list)
        file_descriptor.write("typedef enum{\n")
        for i in range(0, list_nr):
            file_descriptor.write("    " + self._priv_state_name_list[i] + ",\n")
        file_descriptor.write("    " + sm_state_common(self._sm_name) + "END,\n")
        file_descriptor.write("}" + state_enum_type(self._sm_name) + ";\n\n")

        list_nr = len(self._priv_condi_name_list)
        file_descriptor.write("typedef enum{\n")
        for i in range(0, list_nr):
            file_descriptor.write("    " + self._priv_condi_name_list[i] + ",\n")
        file_descriptor.write("    " + sm_condition_common(self._sm_name) + "END,\n")
        file_descriptor.write("}" + condition_enum_type(self._sm_name) + ";\n\n")

    def __create_transition_table_line_type(self, file_descriptor):
        file_descriptor.write("typedef struct{\n")
        file_descriptor.write("    Transition_t transition[" +
                              sm_condition_common(self._sm_name) + "END" + "];\n")
        file_descriptor.write("}" + state_type(self._sm_name) + ";\n")
        file_descriptor.write("\n")

    def __create_table(self, file_descriptor, prepared_list):
        file_descriptor.write("STATIC const " + state_type(self._sm_name) + " " +
                                      transition_table_name(self._sm_name) + "[" +
                                      sm_state_common(self._sm_name) + "END" + "] = {\n")

        non_empty_state_list = []
        for state in self._priv_state_name_list:
            for item in prepared_list:
                if item.from_state in state:
                    # we have something to write for this state
                    non_empty_state_list.append(item)

            if len(non_empty_state_list) != 0:  # if list is not empty
                file_descriptor.write("    [" + state + "] = {\n")
                file_descriptor.write("        .transition = {\n")

                for item in non_empty_state_list:
                    file_descriptor.write("            [" + item.condition + "] = {\n")
                    file_descriptor.write("                .pTransFunc = " + item.action + ",\n")
                    file_descriptor.write("                .nextState = " + item.to_state + ",\n")
                    file_descriptor.write("                .isTransitionValid = true,\n")
                    file_descriptor.write("            },\n")

                file_descriptor.write("        },\n")
                file_descriptor.write("    },\n")

            non_empty_state_list = []

        file_descriptor.write("};\n")
        file_descriptor.write("\n")

    def __create_init_func(self, file_descriptor):
        file_descriptor.write("bool " + init_func_name(self._sm_name) + "(void){\n")
        file_descriptor.write("    smHandler = FSM_New((void*) " + transition_table_name(self._sm_name) + ",\n")
        file_descriptor.write("                        sizeof(" + state_type(self._sm_name) + "),\n")
        file_descriptor.write("                        " + self._priv_state_name_list[0] + ",\n")
        file_descriptor.write("                        " + self._priv_condi_name_list[0] + ",\n")
        file_descriptor.write("                        " + self._priv_state_name_list[0] + ",\n")
        file_descriptor.write("                        " + self._priv_condi_name_list[0] + ");\n")
        file_descriptor.write("    return (smHandler == NULL ) ? false : true;\n}\n")
        file_descriptor.write("\n")

    def __create_tick_func(self, file_descriptor):
        file_descriptor.write("void " + tick_func_name(self._sm_name) + "(void){\n")
        file_descriptor.write("    FSM_Tick(smHandler);\n")
        file_descriptor.write("}\n")

    def _copy_default_files(self):
        c_generator_dir = os.path.dirname(os.path.abspath(__file__))
        self.__copytree(c_generator_dir + os.sep + "fsmMgr", RESULT_PATH + os.sep + "src" + os.sep + "fsmMgr")

    def _create_unit_test(self, prepared_list):
        self.__copy_ceedling()
        utest_file_writer = open(RESULT_PATH + os.sep + "unit_test" + os.sep + "test" +
                                 os.sep + "test_" + self._sm_name + "SMFunc.c", 'w+')
        self.__write_include(utest_file_writer)
        self.__create_enumeration(utest_file_writer)
        self.__create_transition_table_line_type(utest_file_writer)
        self.__write_extern(utest_file_writer)
        self.__write_ceedling_func(utest_file_writer)
        self.__write_test_enum_change(utest_file_writer)
        self.__write_test_table_size(utest_file_writer)
        self.__write_test_defined_transition(utest_file_writer, prepared_list)
        self.__write_test_no_new_transition(utest_file_writer, prepared_list)

        utest_file_writer.close()

    def __write_include(self, utest_file_descriptor):
        utest_file_descriptor.write("#include \"unity.h\"\n#include \"" +
                                    self._header_file_name + "\"\n#include \"mock_MealyFSM.h\"\n\n")

    def __write_extern(self, utest_file_descriptor):
        for item in self._priv_func_name_list:
            utest_file_descriptor.write("extern void " + item + "( void );\n")
        utest_file_descriptor.write("extern FSM_t* smHandler;\n")
        utest_file_descriptor.write("extern const " + state_type(self._sm_name) + " " +
                                    transition_table_name(self._sm_name) + "[" +
                                    sm_state_common(self._sm_name) + "END" + "];\n")
        utest_file_descriptor.write("\n")

    def __write_ceedling_func(self, utest_file_descriptor):
        utest_file_descriptor.write("void setUp(void)\n"
                                    "{\n"
                                    "}\n"
                                    "\n"
                                    "void tearDown(void)\n"
                                    "{\n"
                                    "}\n"
                                    "\n")
        utest_file_descriptor.write("void test_InitFailed(void)\n"
                                    "{\n"
                                    "    FSM_New_ExpectAnyArgsAndReturn(NULL);\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(false, " + self._sm_name + "_Init());\n"
                                    "}\n"
                                    "\n"
                                    "void test_InitSuccess(void)\n"
                                    "{\n"
                                    "    FSM_t fsm;\n"
                                    "    FSM_New_ExpectAnyArgsAndReturn(&fsm);\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(true, " + self._sm_name + "_Init());\n"
                                    "}\n"
                                    "\n"
                                    "void test_TickIsCalled(void)\n"
                                    "{\n"
                                    "    FSM_Tick_ExpectAnyArgs();\n"
                                    "\n"
                                    "    " + self._sm_name + "_Tick();\n"
                                    "}\n"
                                    "\n")

    def __write_test_enum_change(self, utest_file_descriptor):
        utest_file_descriptor.write("void test_EnumNotChange(void)\n{\n")

        list_nr = len(self._priv_state_name_list)
        for i in range(0, list_nr):
            utest_file_descriptor.write("    TEST_ASSERT_EQUAL(" + str(i) + ", " +
                                        self._priv_state_name_list[i] + ");\n")
        utest_file_descriptor.write("    TEST_ASSERT_EQUAL(" + str(list_nr) + ", " +
                                    sm_state_common(self._sm_name) + "END);\n\n")
        list_nr = len(self._priv_condi_name_list)
        for i in range(0, list_nr):
            utest_file_descriptor.write("    TEST_ASSERT_EQUAL(" + str(i) + ", " +
                                        self._priv_condi_name_list[i] + ");\n")
        utest_file_descriptor.write("    TEST_ASSERT_EQUAL(" + str(list_nr) + ", " +
                                    sm_condition_common(self._sm_name) + "END);\n")

        utest_file_descriptor.write("}\n\n")

    def __write_test_table_size(self, utest_file_descriptor):
        condition_end_name = sm_condition_common(self._sm_name) + "END"
        state_end_name = sm_state_common(self._sm_name) + "END"

        utest_file_descriptor.write("void test_LineSizeNotChange(void)\n"
                                    "{\n"
                                    "    uint32_t expectedSize = " + condition_end_name + " * sizeof(Transition_t);\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(expectedSize, sizeof(" + state_type(self._sm_name) + "));\n"
                                    "}\n"
                                    "\n"
                                    "void test_TableSizeNotChange(void)\n"
                                    "{\n"
                                    "    uint32_t expectedSize = " + condition_end_name +
                                    " * sizeof(Transition_t) *" + state_end_name + ";\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(expectedSize, sizeof(" + transition_table_name(self._sm_name) + "));\n"
                                    "}\n\n")

    def __write_test_defined_transition(self, utest_file_descriptor, prepared_list):
        for item in prepared_list:
            func_name = "test_Transition_s_" + item.from_state + "_c_" + item.condition
            utest_file_descriptor.write("void " + func_name + "(void)\n")
            utest_file_descriptor.write("{\n"
                                        "    TransitionFunction expectedFunc = " + item.action + ";\n"
                                        "    " + state_enum_type(self._sm_name) + "  expectedNextState = " + item.to_state + ";\n\n")
            utest_file_descriptor.write("    " + state_type(self._sm_name) + " tableLine = " +
                                        transition_table_name(self._sm_name) + "[" + item.from_state + "];\n")
            utest_file_descriptor.write("    Transition_t actualTransition = " +
                                        "tableLine.transition[" + item.condition + "];\n\n")
            utest_file_descriptor.write("    TEST_ASSERT_EQUAL(expectedFunc, actualTransition.pTransFunc);\n"
                                        "    TEST_ASSERT_EQUAL(expectedNextState, actualTransition.nextState);\n"
                                        "    TEST_ASSERT_EQUAL(true, actualTransition.isTransitionValid);\n"
                                        "}\n\n")

    def __write_test_no_new_transition(self, utest_file_descriptor, prepared_list):

        utest_file_descriptor.write("void test_NoTransistionAdded(void)\n"
                                    "{\n"
                                    "    uint8_t expectedValidTransitionNumber = " + str(len(prepared_list)) + ", actualNumber = 0;\n"
                                    "    " + state_type(self._sm_name) + " tableLine;\n"
                                    "    Transition_t actualTransition;\n\n")

        utest_file_descriptor.write("    for (" + state_enum_type(self._sm_name) + " i = " + self._priv_state_name_list[0] +
                                    "; i < " + sm_state_common(self._sm_name) + "END; i++)\n")

        utest_file_descriptor.write("    {\n"
                                    "        for ( " + condition_enum_type(self._sm_name) + " j = " +
                                    self._priv_condi_name_list[0] + "; j < " +
                                    sm_condition_common(self._sm_name) + "END; j++)\n")
        utest_file_descriptor.write("        {\n"
                                    "            tableLine = " + transition_table_name(self._sm_name) + "[i];\n"
                                    "            actualTransition = tableLine.transition[j];\n"
                                    "            if ( true == actualTransition.isTransitionValid )\n"
                                    "            {\n"
                                    "                actualNumber++;\n"
                                    "            }\n"
                                    "        }\n"
                                    "    }\n"
                                    "\n"
                                    "    TEST_ASSERT_EQUAL(expectedValidTransitionNumber, actualNumber);\n"
                                    "}\n\n")

    def __copy_ceedling(self):
        c_generator_dir = os.path.dirname(os.path.abspath(__file__))
        self.__copytree(c_generator_dir + os.sep + "unit_test", RESULT_PATH + os.sep + "unit_test")

    @staticmethod
    def __copytree(src, dst):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

