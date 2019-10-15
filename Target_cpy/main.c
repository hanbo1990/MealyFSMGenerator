#include "Example.h"

#include <stdio.h>
#define _BSD_SOURCE
#define _XOPEN_SOURCE 600
#define _POSIX_C_SOURCE 200111L
#define _DEFAULT_SOURCE
#include <unistd.h>

void sleepMs(long ms)
{
    long MS = ms*1000;
    usleep(MS);
}


int main( void )
{
    printf("Init project");
    EXAMPLE_Init();


    while(1){
        sleepMs(50);
        EXAMPLE_Tick();
    }
    
    return 0;
}
