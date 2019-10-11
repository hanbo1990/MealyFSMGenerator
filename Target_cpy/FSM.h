#include <stddef.h>

#define MAX_FSM_NUMBER  10U

typedef void (*ActionType) ( void );

typedef struct{
    ActionType pActFunc;
    size_t nextState;
}Transition_t;

typedef struct{
    ActionType actionFunc;
    Transition_t* tableEntry[][];
    size_t newCondition;
    size_t currentCondition;
    size_t currentState;
    size_t defaultCondition;
    size_t defaultState;
}FSM_t;

FSM_t* FSM_New( Transition_t* table, size_t startState, size_t startCondition );
void FSM_Tick( FSM_t* fsm );
void FSM_UpdateCondition( FSM_t* fsm, size_t newCondition );
