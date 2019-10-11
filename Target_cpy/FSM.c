#include "FSM.h"

static FSM_t fsmList[MAX_FSM_NUMBER] = {0};
static size_t fsmCount = 0;

FSM_t* FSM_New( Transition_t* table, size_t startState, size_t startCondition )
{
    FSM_t* ret = NULL;

    if( fsmCount < MAX_FSM_NUMBER)
    {
        ret = &(fsmList[++fsmCount]);
        fsmList[fsmCount].tableEntry = table;
        fsmList[fsmCount].defaultState = startState;
        fsmList[fsmCount].defaultCondition = startCondition;
    }

    return ret;
}

void FSM_Tick( FSM_t* fsm )
{
    Transition_t currentTransition = fsm->tableEntry[fsm->currentState][fsm->currentCondition];

    fsm->currentCondition = fsm->defaultCondition;

    if( currentTransition != NULL)
    {
        // update next state to be processed
        fsm->currentState = currentTransition->nextState;

        //execute the function for this event at state if exist
        if(currentTransition->pActFunc != NULL)
        {
            currentTransition->pActFunc();
        }
    }
}


void FSM_UpdateCondition( FSM_t* fsm, size_t newCondition );

void private_Process( void )
{

}

void private_Reset( void )
{
    ResetHandle.currentState = EXAMPLE_STATE__START;
    ResetHandle.currentCondition = EXAMPLE_CONDITION__NONE;
}