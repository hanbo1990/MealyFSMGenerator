#include "Example.h"
#include "FSM.h"


typedef enum{ // leave state 0 for tick function to know transaction is not valid
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

void ExampleFSM_Private_Reset( void );
void ExampleFSM_Private_Connect( void );
void ExampleFSM_Private_CheckIfTImeToConnect( void );
void ExampleFSM_Private_SayHello( void );

FSM_t* smHandler;

/***************************************************************************************************
           LOCAL VAR
*/

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

/***************************************************************************************************
           PUBLIC FUNCTION
*/

bool EXAMPLE_Init( void )
{
    smHandler = FSM_New((void*) ResetTransTable,
                        sizeof(ExampleState_t),
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

/***************************************************************************************************
           PRIVATE FUNCTION DECLARATION
*/
void ExampleFSM_Private_Reset( void )
{
    printf("ExampleFSM_Private_Reset\n");
}

void ExampleFSM_Private_Connect( void )
{
    FSM_UpdateCondition(smHandler, EXAMPLE_CONDITION__CONNECT_SUCCESS);
    printf("ExampleFSM_Private_Connect\n");
}

void ExampleFSM_Private_CheckIfTImeToConnect( void )
{
    printf("ExampleFSM_Private_CheckIfTImeToConnect\n");
    FSM_UpdateCondition(smHandler, EXAMPLE_CONDITION__READY_TO_CONNECT);
}

void ExampleFSM_Private_SayHello( void )
{
    static bool flag = true;
    if( flag )
    {
        printf("ExampleFSM_Private_SayHello\n");
        printf("\n\nHello\n\n");
        flag = false;
    }
}
