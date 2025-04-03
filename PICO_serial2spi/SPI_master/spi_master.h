#ifndef __MY_SPI_MASTER__H__
#define __MY_SPI_MASTER__H__

#include <pico/stdio.h>
#include <pico/stdlib.h>
#include <stdio.h>
#include <hardware/gpio.h>

#include <hardware/spi.h>
#include "util.h"


#define SPI_CLK     2
#define SPI_TX      3
#define SPI_RX      4

#define SPI_DEV_SEL 5

#define SPI_DEV_SEL_LOGIC   (1)
#define READ                (1)
#define WRITE               (!READ)
#define SPI_SPEED           (1 * MHz)


#define FIFO_START_ADDRESS  0xC0
#define FIFO_END_ADDRESS    0xD7
#define FIFO_SIZE           (FIFO_END_ADDRESS - FIFO_START_ADDRESS + 1)




void SPI_master_init();
int SPI_master_write(uint16_t address, uint32_t data);
uint32_t SPI_master_read(uint16_t address);
uint SPI_master_read_multiple(uint16_t address, uint count, uint32_t *data);

int SPI_master_send(uint16_t data, bool release);
int SPI_master_write_multiple(uint16_t address, uint count, uint32_t *data);

#endif