#include "spi_master.h"

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



uint32_t SPI_master_read(uint8_t address){
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


int SPI_master_write(uint8_t address, uint32_t data){
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


int SPI_master_send(uint16_t data, bool release){
    uint16_t buffer[1] = {data};
    gpio_put(SPI_DEV_SEL, SPI_DEV_SEL_LOGIC);
    int status = spi_write16_blocking(SPI_CHANNEL, buffer, 1);
    if (release)
        gpio_put(SPI_DEV_SEL, !SPI_DEV_SEL_LOGIC);

    return status;
}