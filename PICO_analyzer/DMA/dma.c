#include "dma.h"


uint DMA_PIOconfig(volatile void *writeData, const volatile void *readData, uint dreq){
    uint dmaPIO = dma_claim_unused_channel(true);
    dma_channel_config dmaPIO_conf = dma_channel_get_default_config(dmaPIO);

    channel_config_set_transfer_data_size(&dmaPIO_conf, DMA_SIZE_32);
    channel_config_set_read_increment(&dmaPIO_conf, false);
    channel_config_set_write_increment(&dmaPIO_conf, true);
    channel_config_set_dreq(&dmaPIO_conf, dreq);
    channel_config_set_ring(&dmaPIO_conf, true, 0);

    dma_channel_configure(dmaPIO,
        &dmaPIO_conf,
        writeData,
        readData,
        DATA_SIZE,
        false
    );

    return dmaPIO;
}



void DMA_setEnable(uint dmaChannel, bool enabled){
    dma_channel_config config = dma_get_channel_config(dmaChannel);
    dma_channel_set_config(dmaChannel, &config, enabled);
}