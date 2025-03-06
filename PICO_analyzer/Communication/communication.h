#ifndef __COMMUNICATION_H__
#define __COMMUNICATION_H__

#include <pico/stdlib.h>

#define NOWRITE_DELAY_MAX  1024
#define COMMUNICATION_SPEED_TEST false
#define ENABLE_GPIO     19


void communication_init();
void communication_run(uint dma_1, uint dma_2, uint *data);

static inline uint communication_read(const char *str);
void communication_sendProcedure(uint dma_1, uint dam_2, uint *data);


extern uint getMainFreq();


#if COMMUNICATION_SPEED_TEST
uint measureTime_tud();
uint measureTime_uartPutChar();
uint measureTime_printf();
#endif

#endif