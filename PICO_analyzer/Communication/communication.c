#include "communication.h"

#include <stdio.h>
#include <string.h>

#include "dma.h"
#include "led.h"



typedef union{
    // uint64_t u64;
    uint32_t u32;
    struct{
        uint16_t half[2];
    };

    struct {
        uint8_t quoter[4];
    };
} convert_t;
#include "tusb.h"


void waitUntilOK(){
    bool wait = true;
    char readMsg[256];
    int index = 0;
    do{
        if (communication_read(readMsg)){
            wait = strncmp(readMsg, "OK", 1);
        }

        LED_toggle();
        sleep_ms(100);
    }while (wait);
    LED_on();
}


void communication_run(uint dma, uint *data){
    waitUntilOK();
    DMA_setEnable(dma, true);

    communication_sendProcedure(dma, data);
}




#if defined(COMMUNICATION_VIA_USB)
void communication_init(){
    stdio_usb_init();
}


uint communication_read(const char *str){
    return tud_cdc_read((void*)str, CFG_TUD_CDC_RX_BUFSIZE);
}


void communication_sendProcedure(uint dma, uint *data){
    uint32_t index = 0;
    uint32_t sampleIndex = 0;
    uint32_t nowriteDelay = 0;

    while (1){
        // printf("Enter to transfer function\n");
        sampleIndex = dma_getCurrentIndex(dma);
        // printf("Get DMA index %u\n", sampleIndex);
        if (index != sampleIndex){
            uint sample = data[index];
            // printf("Index: %u\tdma: %u\n", index, sampleIndex);
            tud_cdc_write(&sample, 2);               // store two byte on USB write buffer
            index++;
            if (index >= DATA_SIZE){
                // index = 0;
            }
            nowriteDelay = 0;
        } else{
            if (nowriteDelay >= NOWRITE_DELAY_MAX){
                tud_cdc_write_flush();                          // send buffer even is not full
                nowriteDelay = 0;
            }

            uint buffCapacity = tud_cdc_write_available();
            if (buffCapacity != CFG_TUD_CDC_TX_BUFSIZE){
                nowriteDelay++; // if the buffer is not empty, count cycles until unconditional send
            }

        }
        sleep_us(1);
    }
}

#elif defined(COMMUNICATION_VIA_UART)
#define UART_ID uart0
int dmaUART;
void communication_init(){
    stdio_uart_init();
}


void communication_sendProcedure(uint dma, uint *data){
    uint index = 0;
    uint sampleIndex = 0;

    while(1){
        sampleIndex = dma_getCurrentIndex(dma, data);
        if (index != sampleIndex){
            for (uint i = 0; i < 2; i++){
                uart_putc_raw(UART_ID, (convert_t){.u32 = data[index]}.quoter[i]);
            }
            index++;
        }
    }
}


#endif





// ##############################
// ###### SPEED TEST ############
// ##############################
#if COMMUNICATION_SPEED_TEST

#define SEND_SAMPLE 500
uint measureTime_tud(){
    uint start = time_us_32();
    for(uint i = 0; i < SEND_SAMPLE; i ++){
        tud_cdc_write("Hello\n\r", 8);
    }
    uint stop = time_us_32();

   return stop - start;
}

uint measureTime_printf(){
    uint start = time_us_32();
    for(uint i = 0; i < SEND_SAMPLE; i ++){
        printf("Hello\n\r");
    }
    uint stop = time_us_32();

   return stop - start;
}

uint measureTime_uartPutChar(){
    uint start = time_us_32();
    char str[] = "Hello\n\r";
    for (uint i = 0; i < SEND_SAMPLE; i++){
        for (uint j = 0; j < 8; j++){
            uart_putc_raw(UART_ID, str[j]);
        }
    }
    uint stop = time_us_32();
    return stop - start;
}


#endif