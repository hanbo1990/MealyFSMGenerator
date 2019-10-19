#include "MealyFSM.h"

static FSM_t fsmList[MAX_FSM_NUMBER];
static size_t fsmCount = 0;

FSM_t* FSM_New( void* table, size_t tableLineSize, size_t startState, size_t startCondition, size_t defaultState, size_t defaultCondition )
{
    FSM_t* ret = NULL;

    if( fsmCount < MAX_FSM_NUMBER)
    {
        ret = &(fsmList[fsmCount]);
        fsmList[fsmCount].tableEntry = table;
        fsmList[fsmCount].tableLineSize = tableLineSize;
        fsmList[fsmCount].defaultState = defaultState;
        fsmList[fsmCount].defaultCondition = defaultCondition;
        fsmList[fsmCount].currentState = startState;
        fsmList[fsmCount++].currentCondition = startCondition;
    }

    return ret;
}

void FSM_Tick( FSM_t* self )
{
    uint32_t newTransitionOffset = ( self->tableLineSize * self->currentState + 
                                     self->currentCondition * sizeof(Transition_t) );

    Transition_t* currentTransition = (Transition_t*)((self->tableEntry + newTransitionOffset));

    self->currentCondition = self->defaultCondition;

    if( currentTransition->isTransitionValid == true )
    {
        // update next state to be processed
        self->currentState = currentTransition->nextState;

        //execute the function for this event at state if exist
        if(currentTransition->pTransFunc != NULL)
        {
            currentTransition->pTransFunc();
        }
    }
}

void FSM_UpdateCondition( FSM_t* self, size_t newCondition )
{
    self->currentCondition = newCondition;
}
