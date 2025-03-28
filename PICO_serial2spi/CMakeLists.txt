cmake_minimum_required(VERSION 3.25)

# select board:
# set(PICO_BOARD pico_w)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
include($ENV{PICO_SDK_PATH}/tools/CMakeLists.txt)

project(main C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()



add_executable(${PROJECT_NAME}
    main.c
    LED/led.c
    SPI_master/spi_master.c
)

include_directories(${PROJECT_NAME}
    .
    LED
    SPI_master
)

pico_add_extra_outputs(${PROJECT_NAME})


target_link_libraries(${PROJECT_NAME}
    pico_stdlib
    
    hardware_gpio
    hardware_irq
    hardware_spi
)


pico_enable_stdio_usb(${PROJECT_NAME} 0)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
