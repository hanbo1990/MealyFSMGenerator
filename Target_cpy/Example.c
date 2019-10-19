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



/***************************************************************************************************
           PUBLIC FUNCTION
*/


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

// include the transistion table
#include "Example.inc"