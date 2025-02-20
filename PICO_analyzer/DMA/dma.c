#include "dma.h"
#include "hardware/irq.h"


uint dma_1, dma_2;
static uint *_writeAddress;


static inline bool _DMA_config(volatile void *writeAddress, const volatile void *readAddress, uint dreq, uint dma, dma_channel_config *config){
    channel_config_set_transfer_data_size(config, DMA_SIZE_32);
    channel_config_set_read_increment(config, false);
    channel_config_set_write_increment(config, true);
    channel_config_set_dreq(config, dreq);


    dma_channel_configure(dma,
        config,
        writeAddress,
        readAddress,
        DATA_SIZE,
        false
    );
    return true;
}


void _dma_1_handler(){
    dma_hw->ints0 = 1 << dma_1;
    dma_channel_set_write_addr(dma_1, _writeAddress, false);
    dma_channel_set_trans_count(dma_1, DATA_SIZE, false);
}

void _dma_2_handler(){
    dma_hw->ints1 = 1 << dma_2;
    dma_channel_set_write_addr(dma_2, _writeAddress, false);
    dma_channel_set_trans_count(dma_1, DATA_SIZE, false);
}


bool DMA_clear(){
    // Clear write address DMA 1
    dma_channel_set_write_addr(dma_1, _writeAddress, false);
    dma_channel_set_trans_count(dma_1, DATA_SIZE, false);

    // Clear write address DMA 2
    dma_channel_set_write_addr(dma_2, _writeAddress, false);
    dma_channel_set_trans_count(dma_1, DATA_SIZE, false);

    return true;
}



bool DMA_PIOconfig(void *writeAddress, const volatile void *readAddress, uint dreq, uint *dmaOut_1, uint *dmaOut_2){
    dma_1 = dma_claim_unused_channel(true);
    dma_2 = dma_claim_unused_channel(true);
    _writeAddress = writeAddress;

    *dmaOut_1 = dma_1;
    *dmaOut_2 = dma_2;

    dma_channel_config config_1 = dma_channel_get_default_config(dma_1);
    dma_channel_config config_2 = dma_channel_get_default_config(dma_2);
    channel_config_set_chain_to(&config_1, dma_2);
    channel_config_set_chain_to(&config_2, dma_1);

    dma_channel_set_irq0_enabled(dma_1, true);
    irq_set_exclusive_handler(DMA_IRQ_0, _dma_1_handler);
    irq_set_enabled(DMA_IRQ_0, true);

    dma_channel_set_irq1_enabled(dma_2, true);
    irq_set_exclusive_handler(DMA_IRQ_1, _dma_2_handler);
    irq_set_enabled(DMA_IRQ_1, true);

    _DMA_config(writeAddress, readAddress, dreq, dma_1, &config_1);
    _DMA_config(writeAddress, readAddress, dreq, dma_2, &config_2);





    return true;
}



void DMA_setEnable(uint dmaChannel, bool enabled){
    dma_channel_config config = dma_get_channel_config(dmaChannel);
    dma_channel_set_config(dmaChannel, &config, enabled);
}




uint dma_getCurrentIndex(uint dmaChannel){
    dma_channel_hw_t *channel = dma_channel_hw_addr(dmaChannel);
    uint transfer_count = channel->al3_transfer_count;
    return DATA_SIZE - transfer_count;
}



// uint dma_getCurrentIndex(uint dmaChannel){
//     uint writeAddress = dma_channel_hw_addr(dmaChannel)->write_addr;
//     uint dataStartAddress = (uintptr_t)(_writeAddress);
//     uint diff = (writeAddress - dataStartAddress) / 4;
//     return diff;
// }