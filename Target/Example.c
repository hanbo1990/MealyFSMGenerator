#include <stdtype.h>

#include "Test.h"




/***************************************************************************************************
           LOCAL VAR
*/

static StateMachineHandle_t ResetHandle = {
    .process = private_Process,
    .reset = private_Reset,
    .currentState = EXAMPLE_STATE__IDLE,
    .currentCondition = EXAMPLE_CONDITION__NONE
};

/***************************************************************************************************
           PUBLIC FUNCTION
*/

void EXAMPLE_Init( void )
{
    private_Reset();
}

void EXAMPLE_Execute( void )
{
    private_Process();
}

/***************************************************************************************************
           PRIVATE FUNCTION DECLARATION
*/



static void private_SM_Connect( void )
{

}

static void private_SM_CheckIfTImeToConnect( void )
{

}

static void private_SM_Reset( void )
{

}

