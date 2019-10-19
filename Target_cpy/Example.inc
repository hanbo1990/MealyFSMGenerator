typedef struct{
    Transition_t transition[EXAMPLE_CONDITION__END];
}ExampleState_t;

static const ExampleState_t ResetTransTable[EXAMPLE_STATE__END] = {
    [EXAMPLE_STATE__START] = {
        .transition = {
            [EXAMPLE_CONDITION__NONE] = {
                .pTransFunc = ExampleFSM_Private_CheckIfTImeToConnect,
                .nextState = EXAMPLE_STATE__START,
                .isTransaitionValid = true,
            },
            [EXAMPLE_CONDITION__READY_TO_CONNECT] = {
                .pTransFunc = ExampleFSM_Private_Connect,
                .nextState = EXAMPLE_STATE__CONNECTING,
                .isTransaitionValid = true,
            },
        }
    },
    [EXAMPLE_STATE__CONNECTING] = {
        .transition = {
            [EXAMPLE_CONDITION__CONNECT_FAIL] = {
                .pTransFunc = ExampleFSM_Private_Reset,
                .nextState = EXAMPLE_STATE__START,
                .isTransaitionValid = true,
            },
            [EXAMPLE_CONDITION__DISCONNECTED] = {
                .pTransFunc = ExampleFSM_Private_Reset,
                .nextState = EXAMPLE_STATE__START,
                .isTransaitionValid = true,
            },
            [EXAMPLE_CONDITION__CONNECT_SUCCESS] = {
                .pTransFunc = NULL,
                .nextState = EXAMPLE_STATE__CONNECTED,
                .isTransaitionValid = true,
            },
        }
    },
    [EXAMPLE_STATE__CONNECTED] = {
        .transition = {
            [EXAMPLE_CONDITION__NONE] = {
                .pTransFunc = ExampleFSM_Private_SayHello,
                .nextState = EXAMPLE_STATE__CONNECTED, 
                .isTransaitionValid = true,
            },
        }
    },
};

bool EXAMPLE_Init( void )
{
    smHandler = FSM_New((void*) ResetTransTable,
                        sizeof(Transition_t) * EXAMPLE_CONDITION__END,
                        EXAMPLE_STATE__START,
                        EXAMPLE_CONDITION__NONE,
                        EXAMPLE_STATE__START,
                        EXAMPLE_CONDITION__NONE);
    
    return (smHandler == NULL ) ? false : true;
}

void EXAMPLE_Tick( void )
{
    FSM_Tick(smHandler);
}

