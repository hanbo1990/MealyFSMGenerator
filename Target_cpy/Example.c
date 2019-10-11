#include "Example.h"
#include <stddef.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef void (*ActionType) ( void );



typedef struct{
    ActionType pTransFunc;
    uint8_t nextState;
    bool isTransaitionValid;
}Transition_t;

void ExampleFSM_Private_Reset( void );
void ExampleFSM_Private_Connect( void );
void ExampleFSM_Private_CheckIfTImeToConnect( void );
void ExampleFSM_Private_SayHello( void );


ResetState_e currentState;
ResetCondition_e currentCondition;

/***************************************************************************************************
           LOCAL VAR
*/
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


typedef struct{
    Transition_t transition[EXAMPLE_CONDITION__END];
}State_t;

static const State_t ResetTransTable[EXAMPLE_STATE__END] = {
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
                .nextState = EXAMPLE_STATE__START, 
                .isTransaitionValid = true,
            },
        }
    },
};

/***************************************************************************************************
           PUBLIC FUNCTION
*/

void EXAMPLE_Init( void )
{
    ExampleFSM_Private_Reset();
}

void EXAMPLE_Tick( void )
{
    const Transition_t* const currentTransition = &((ResetTransTable[currentState]).transition[currentCondition]);

    currentCondition = EXAMPLE_CONDITION__NONE;

    if( currentTransition->isTransaitionValid == true )
    {
        // update next state to be processed
        currentState = currentTransition->nextState;

        //execute the function for this event at state if exist
        if(currentTransition->pTransFunc != NULL)
        {
            currentTransition->pTransFunc();
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
    printf("func size is %d\n", sizeof(ActionType));
    printf("transaction size is %ld \n", sizeof(Transition_t));
    printf("Table Size is %ld\n", sizeof(ResetTransTable));
}