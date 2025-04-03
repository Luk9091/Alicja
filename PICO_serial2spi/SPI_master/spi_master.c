#include "spi_master.h"
#include <stdlib.h>

// SPI
// MSB - read/write = 1/0

#define SPI_CHANNEL spi0
#define SPI_CLK     2
#define SPI_TX      3
#define SPI_RX      4
// #define SPI_CS      5

#define SPI_DEV_SEL 5

#define SPI_BIT_LEN 16

#define MSB         15


void SPI_master_init(){
    spi_init(SPI_CHANNEL, SPI_SPEED);
    
    gpio_set_function(SPI_CLK, GPIO_FUNC_SPI);
    gpio_set_function(SPI_RX, GPIO_FUNC_SPI);
    gpio_set_function(SPI_TX, GPIO_FUNC_SPI);

    gpio_init(SPI_DEV_SEL);
    gpio_set_dir(SPI_DEV_SEL, GPIO_OUT);
    
    spi_set_format(SPI_CHANNEL, SPI_BIT_LEN, SPI_CPOL_0, SPI_CPHA_1, SPI_MSB_FIRST);

    gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);
}



uint32_t SPI_master_read(uint16_t address){
    uint16_t header = 
          READ << MSB
        | address << 6
    ;

    uint16_t send[1] = {header};
    uint16_t read[2] = {-1, -1};

    gpio_put(SPI_DEV_SEL, SPI_DEV_SEL_LOGIC);
    spi_write16_blocking(SPI_CHANNEL, send, 1);
    spi_read16_blocking(SPI_CHANNEL, 0, read, 2);
    gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);

    if (address < 0xC0){
        read[1] = -1;
    }

    return ~(read[1] << 16 | read[0]);
}

uint SPI_master_read_multiple(uint16_t address, uint count, uint32_t *data){
    int upper_address = address + count;
    int high_count  = 0;
    if (upper_address >= 0xC0){
        high_count = upper_address - 0xC0;
    }
    int low_count   = count - high_count;
    if (low_count < 0){
        low_count = 0;
    }

    uint16_t *data_16 = (uint16_t*)(malloc((low_count  + 1) * sizeof(uint16_t)));
    if (data_16 == NULL) return -1;
    uint16_t *data_32 = (uint16_t*)(malloc((high_count + 1) * sizeof(uint16_t) * 2));
    if (data_32 == NULL) return -1;


    if (low_count > 0){
        uint16_t header = 
                (READ << MSB)
            |   (address << 6)
        ;

        uint16_t send[1]    = {header};
        gpio_put(SPI_DEV_SEL, SPI_DEV_SEL_LOGIC);
        spi_write16_blocking(SPI_CHANNEL, send, 1);
        spi_read16_blocking(SPI_CHANNEL, 0, data_16, low_count);
        gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);
    }

    if (high_count > 0){
        uint16_t header = 
                (READ << MSB)
            |   ((address + low_count) << 6)
        ;

        uint16_t send[1]    = {header};

        gpio_put(SPI_DEV_SEL, SPI_DEV_SEL_LOGIC);
        spi_write16_blocking(SPI_CHANNEL, send, 1);
        spi_read16_blocking(SPI_CHANNEL, 0, data_32, high_count*2);
        gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);
    }
    

    for (uint i = 0; i < low_count; i++){
        data[i] = ~((uint32_t)((-1) << 16) | data_16[i]);
    }

    for (uint i = 0; i < high_count; i++){
        uint32_t dataH = data_32[i*2 + 1] << 16;
        uint32_t dataL = data_32[i*2];
        uint32_t sum   = ~(dataH | dataL);
        data[low_count + i] = sum;
    }

    free(data_16);
    free(data_32);

    return high_count + low_count;
}

int SPI_master_write(uint16_t address, uint32_t data){
    uint16_t header = 
          WRITE << MSB
        | address << 6
    ;

    uint16_t send[3] = {header, data, data >> 16};


    gpio_put(SPI_DEV_SEL, SPI_DEV_SEL_LOGIC);
    int status = spi_write16_blocking(SPI_CHANNEL, send, 3);
    gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);

    return status;
}


int SPI_master_write_multiple(uint16_t address, uint count, uint32_t *data){
    // uint16_t header = 
    //       WRITE << MSB
    //     | address << 6
    // ;

   int upper_address = address + count;
    int high_count  = 0;
    if (upper_address >= 0xC0){
        high_count = upper_address - 0xC0;
    }
    int low_count   = count - high_count;
    if (low_count < 0){
        low_count = 0;
    }

    uint16_t *data_16 = (uint16_t*)(malloc((low_count  + 1) * sizeof(uint16_t)));
    if (data_16 == NULL) return -1;
    uint16_t *data_32 = (uint16_t*)(malloc((high_count + 1) * sizeof(uint16_t) * 2));
    if (data_32 == NULL) return -1;

    for (uint i = 0; i < low_count; i++){
        data_16[1 + i] = data[i];
    }
    for (uint i = 0; i < high_count; i++){
        data_32[1 + 2*i]        = (uint16_t)(data[low_count + i]);
        data_32[1 + 2*i + 1]    = (uint16_t)(data[low_count + i] >> 16);
    }

    int status = 0;
    if (low_count > 0){
        data_16[0] = (WRITE << MSB) | (address << 6);
        gpio_put(SPI_DEV_SEL, SPI_DEV_SEL_LOGIC);
        status = spi_write16_blocking(SPI_CHANNEL, data_16, low_count + 1);
        gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);
    }

    if (high_count > 0){
        data_32[0] = (WRITE << MSB) | ((address + low_count) << 6);
        gpio_put(SPI_DEV_SEL, SPI_DEV_SEL_LOGIC);
        status += spi_write16_blocking(SPI_CHANNEL, data_32, high_count*2 + 1);
        gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);
    }
    
    free(data_16);
    free(data_32);
    return status;
}


// int SPI_master_send(uint16_t data, bool release){
//     uint16_t buffer[1] = {data};
//     gpio_put(SPI_DEV_SEL, SPI_DEV_SEL_LOGIC);
//     int status = spi_write16_blocking(SPI_CHANNEL, buffer, 1);
//     if (release)
//         gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);

//     return status;
// }