#include "Example.h"
#include <stddef.h>
#include <stdio.h>

typedef void (*ActionType) ( void );

typedef struct{
    ActionType pActFunc;
    size_t nextState;
}Transition_t;

void ExampleFSM_Private_Reset( void );
void ExampleFSM_Private_Connect( void );
void ExampleFSM_Private_CheckIfTImeToConnect( void );
void ExampleFSM_Private_SayHello( void );

/***************************************************************************************************
           LOCAL VAR
*/
typedef enum{ // leave state 0 for tick function to know transaction is not valid
    EXAMPLE_STATE__START = 1,
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
            .nextState = EXAMPLE_STATE__START,
        },
        [EXAMPLE_CONDITION__READY_TO_CONNECT] = {
            .pActFunc = ExampleFSM_Private_Connect,
            .nextState = EXAMPLE_STATE__CONNECTING,
        },
    },
    [EXAMPLE_STATE__CONNECTING] = {
        [EXAMPLE_CONDITION__CONNECT_FAIL] = {
            .pActFunc = ExampleFSM_Private_Reset,
            .nextState = EXAMPLE_STATE__START,
        },
        [EXAMPLE_CONDITION__DISCONNECTED] = {
            .pActFunc = ExampleFSM_Private_Reset,
            .nextState = EXAMPLE_STATE__START,
        },
        [EXAMPLE_CONDITION__CONNECT_SUCCESS] = {
            .pActFunc = NULL,
            .nextState = EXAMPLE_STATE__CONNECTED,
        },
    },
    [EXAMPLE_STATE__CONNECTED] = {
        [EXAMPLE_CONDITION__NONE] = {
            .pActFunc = ExampleFSM_Private_SayHello,
            .nextState = EXAMPLE_STATE__START, 
        },
    },
};

ResetState_e currentState;
ResetCondition_e currentCondition;

/***************************************************************************************************
           PUBLIC FUNCTION
*/

void EXAMPLE_Init( void )
{
    ExampleFSM_Private_Reset();
}

void EXAMPLE_Tick( void )
{
    Transition_t currentTransition = ResetTransTable[currentState][currentCondition];

    currentCondition = EXAMPLE_CONDITION__NONE;

    if( currentTransition.nextState != 0 )
    {
        // update next state to be processed
        currentState = currentTransition.nextState;

        //execute the function for this event at state if exist
        if(currentTransition.pActFunc != NULL)
        {
            currentTransition.pActFunc();
        }
    }
}

/***************************************************************************************************
           PRIVATE FUNCTION DECLARATION
*/
void ExampleFSM_Private_Reset( void )
{

}

void ExampleFSM_Private_Connect( void )
{

}

void ExampleFSM_Private_CheckIfTImeToConnect( void )
{

}

void ExampleFSM_Private_SayHello( void )
{

}

int main( void )
{
    printf("transaction size is %ld \n", sizeof(Transition_t));
    printf("Table Size is %ld\n", sizeof(ResetTransTable));
}