#include <stdio.h>
#include <stdlib.h>
#include <pico/stdlib.h>
#include <pico/stdio.h>
#include <hardware/clocks.h>
#include <hardware/structs/systick.h>
#include <hardware/dma.h>
#include <pico/multicore.h>
#include <pico/cyw43_arch.h>

#include <hardware/gpio.h>

#include "FIFO.h"

#include "read.pio.h"


#define TRIGGER_GPIO    15
#define ENABLE_GPIO     14

#define LSB_GPIO        2
#define PIO_NUM_PIN     8

#define DATA_SIZE       1024

uint read_mask =
    1 << 2 | 1 << 3 | 1 << 4 | 1 << 5 |
    1 << 6 | 1 << 7 | 1 << 8 | 1 << 9;
uint64_t sampleIndex;
uint sampleData[DATA_SIZE] = {0};

PIO pio;
uint sm;
uint offset;


typedef union{
    uint64_t u64;
    uint32_t u32;
    struct{
        uint16_t half[2];
    };

    struct {
        uint8_t quoter[4];
    };
} convert_t;


uint reverseBit(uint64_t data){
    uint reverseData = 0;
    for (int i = 0; i < 32; i++){
        if ((data & (1 << i)))
            reverseData |= 1 << ((32 - 1) - i);
    }
    return reverseData;
}

void gpio_trigInput_callback(uint gpio, uint32_t events){
    while(pio_sm_get_rx_fifo_level(pio, sm)){
        sampleData[sampleIndex] = pio_sm_get(pio, sm);
        sampleIndex++;
    }
}


int main(){
    set_sys_clock_khz(200000, true);
    systick_hw->csr = 0x05;

    gpio_init_mask(read_mask);
    gpio_init(ENABLE_GPIO);
    gpio_init(TRIGGER_GPIO);


    gpio_set_dir_in_masked(read_mask);
    gpio_set_dir(ENABLE_GPIO, true);
    gpio_set_dir(TRIGGER_GPIO, false);


    pio_claim_free_sm_and_add_program_for_gpio_range(&read_gpio_program, &pio, &sm, &offset, LSB_GPIO, PIO_NUM_PIN, true);
    read_gpio_program_init(pio, sm, offset, LSB_GPIO, PIO_NUM_PIN, TRIGGER_GPIO);



    if(cyw43_arch_init()){
        printf("WiFi init failed\n");
        return -1;
    }
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, !cyw43_arch_gpio_get(CYW43_WL_GPIO_LED_PIN));

    stdio_init_all();



    uint dmaPIO = dma_claim_unused_channel(true);
    dma_channel_config dmaPIO_conf = dma_channel_get_default_config(dmaPIO);

    channel_config_set_transfer_data_size(&dmaPIO_conf, DMA_SIZE_32);
    channel_config_set_read_increment(&dmaPIO_conf, false);
    channel_config_set_write_increment(&dmaPIO_conf, true);
    channel_config_set_dreq(&dmaPIO_conf, pio_get_dreq(pio, sm, false));
    channel_config_set_ring(&dmaPIO_conf, false, 0);

    dma_channel_configure(dmaPIO,
        &dmaPIO_conf,
        sampleData,
        &pio->rxf[sm],
        DATA_SIZE,
        true
    );



    // gpio_set_irq_enabled_with_callback(TRIGGER_GPIO, GPIO_IRQ_EDGE_RISE, true, &gpio_trigInput_callback);
    // pio_sm_put(pio, sm, 0);
    sleep_ms(3);

    gpio_put(ENABLE_GPIO, 1);
    sleep_us(1000);
    gpio_put(ENABLE_GPIO, 0);
    sleep_ms(10);


    printf("CPU speed: %.3f\n", frequency_count_mhz(CLOCKS_FC0_SRC_VALUE_CLK_SYS));
    printf("Impulse: %llu\n", sampleIndex);
    for (uint i = 0; i < DATA_SIZE; i++){
        // sampleData[i] = sampleData[i] >> 24;
        sampleData[i] = reverseBit(sampleData[i]);
    }

    for (uint i = 0; i < DATA_SIZE; i = i + 16){
        printf("% 3u\t% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u,% 3u\n", i/16,
            sampleData[0 + i], sampleData[1 + i], sampleData[2 + i],  sampleData[3 + i],  sampleData[4 + i],  sampleData[5 + i],  sampleData[6 + i],  sampleData[7 + i],
            sampleData[8 + i], sampleData[9 + i], sampleData[10 + i], sampleData[11 + i], sampleData[12 + i], sampleData[13 + i], sampleData[14 + i], sampleData[15 + i]
        );
    }

    while (1){
        // uint fifoLen = pio_sm_get_rx_fifo_level(pio, sm);
        // if (fifoLen){
        //     uint read = pio_sm_get(pio, sm);
        //     convert_t data = {.u32 = read};
        //     read = (data.quoter[0] + data.quoter[1] + data.quoter[2] + data.quoter[3])/4;
        //     printf("%3llu\tRead from IRQ: % 3u = 0x%02X\n", sampleIndex, read, read);
        //     // sampleData[sampleIndex] = ;
        //     sampleIndex++;
        //     // pio_sm_put(pio, sm, 0);
        // }

        sleep_ms(10);
    }

}