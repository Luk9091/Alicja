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
#define SPI_SPEED           (10 * MHz)




void SPI_master_init();
int SPI_master_write(uint8_t address, uint32_t data);
uint32_t SPI_master_read(uint8_t address);

int SPI_master_send(uint16_t data, bool release);

#endif