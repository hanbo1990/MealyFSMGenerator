#include <stddef.h>
#include <stddef.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define MAX_FSM_NUMBER  10U

typedef void (*TransitionFunction) ( void );

typedef struct{
    TransitionFunction pTransFunc;
    uint8_t nextState;
    bool isTransaitionValid;
}Transition_t;

typedef struct{
    void* tableEntry;
    size_t tableLineSize;
    size_t currentCondition;
    size_t currentState;
    size_t defaultCondition;
    size_t defaultState;
}FSM_t;

FSM_t* FSM_New( void* table, 
                size_t tableLineSize,
                size_t startState, 
                size_t startCondition, 
                size_t defaultState, 
                size_t defaultCondition );

void FSM_Tick( FSM_t* self );
void FSM_UpdateCondition( FSM_t* self, size_t newCondition );
