#ifndef __COMMUNICATION_H__
#define __COMMUNICATION_H__

#include <pico/stdlib.h>

#define NOWRITE_DELAY_MAX  1024
#define COMMUNICATION_SPEED_TEST false


volatile uint dma_getCurrentIndex(uint dma, uint *data);

void communication_init();
void communication_run(uint dma, uint *data);

static inline uint communication_read(const char *str);
void communication_sendProcedure(uint dma, uint *data);


#if COMMUNICATION_SPEED_TEST
uint measureTime_tud();
uint measureTime_uartPutChar();
uint measureTime_printf();
#endif

#endif