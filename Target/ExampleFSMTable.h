#include "FSM.h"
#include "ExampleFSMFunc.h"

typedef enum{
    EXAMPLE_STATE__START,
    EXAMPLE_STATE__CONNECTING,
    EXAMPLE_STATE__CONNECTED,
    EXAMPLE_STATE__END,
} ResetState_e;

typedef enum{
    EXAMPLE_CONDITION__NONE,
    EXAMPLE_CONDITION__READY_TO_CONNECT,
    EXAMPLE_CONDITION__CONNECT_FAIL,
    EXAMPLE_CONDITION__DISCONNECTED,
    EXAMPLE_CONDITION__CONNECT_SUCCESS,
    EXAMPLE_CONDITION__END,
} ResetCondition_e;

static const Transition_t ResetTransTable[EXAMPLE_STATE__END][EXAMPLE_CONDITION__END] = {
    [EXAMPLE_STATE__START] = {
        [EXAMPLE_CONDITION__NONE] = {
            .pActFunc = ExampleFSM_Private_CheckIfTImeToConnect,
            .nextState = EXAMPLE_STATE__START}
        },
        [EXAMPLE_CONDITION__READY_TO_CONNECT] = {
            .pActFunc = ExampleFSM_Private_Connect,
            .nextState = EXAMPLE_STATE__CONNECTING
        },
        [EXAMPLE_CONDITION__CONNECT_FAIL] = NULL,
        [EXAMPLE_CONDITION__DISCONNECTED] = NULL,
        [EXAMPLE_CONDITION__CONNECT_SUCCESS] = NULL,
    },
    [EXAMPLE_STATE__CONNECTING] = {
        [EXAMPLE_CONDITION__NONE] = NULL,
        [EXAMPLE_CONDITION__READY_TO_CONNECT] = NULL,
        [EXAMPLE_CONDITION__CONNECT_FAIL] = {
            .pActFunc = ExampleFSM_Private_Reset,
            .nextState = EXAMPLE_STATE__START
        },
        [EXAMPLE_CONDITION__DISCONNECTED] = {
            .pActFunc = ExampleFSM_Private_Reset,
            .nextState = EXAMPLE_STATE__START
        },
        [EXAMPLE_CONDITION__CONNECT_SUCCESS] = {
            .pActFunc = NULL,
            .nextState = EXAMPLE_STATE__CONNECTED
        },
    },
    [EXAMPLE_STATE__CONNECTED] = {
        [EXAMPLE_CONDITION__NONE] = NULL,
        [EXAMPLE_CONDITION__READY_TO_CONNECT] = NULL,
        [EXAMPLE_CONDITION__CONNECT_FAIL] = NULL,
        [EXAMPLE_CONDITION__DISCONNECTED] = NULL,
        [EXAMPLE_CONDITION__CONNECT_SUCCESS] = NULL,
    },
};