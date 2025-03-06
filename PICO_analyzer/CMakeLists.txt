cmake_minimum_required(VERSION 3.25)

# Select board:
set(BOARD_TYPE "BOARD_PICO")
# set(BOARD_TYPE "BOARD_PICO_W")

# Select communication protocol
set(COMMUNICATION_TYPE "USB")
# set(COMMUNICATION_TYPE "UART")



include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
include($ENV{PICO_SDK_PATH}/tools/CMakeLists.txt)

project(main C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()


if(NOT BOARD_TYPE)
    # message(WARNING "Board not selected, using default pico")
    set(BOARD_TYPE "BOARD_PICO")
endif()
if (NOT COMMUNICATION_TYPE)
    set(COMMUNICATION_TYPE "USB")
endif()


if (BOARD_TYPE STREQUAL "BOARD_PICO")
    set(PICO_BOARD pico)
    add_compile_definitions(BUILD_PICO)
elseif(BOARD_TYPE STREQUAL "BOARD_PICO_W")
    set(PICO_BOARD pico_w)
    add_compile_definitions(BUILD_PICO_W)
endif()


if (COMMUNICATION_TYPE STREQUAL "USB")
    add_compile_definitions(COMMUNICATION_VIA_USB)
    SET(ENABLE_USB 1)
    SET(ENABLE_UART 0)
elseif(COMMUNICATION_TYPE STREQUAL "UART")
    add_compile_definitions(COMMUNICATION_VIA_UART)
    SET(ENABLE_USB 0)
    SET(ENABLE_UART 1)
endif()


add_compile_definitions(SYS_CLK_MHZ=200)


add_executable(${PROJECT_NAME}
    main.c
    DMA/dma.c
    LED/led.c
    Communication/communication.c
)

include_directories(${PROJECT_NAME}
    DMA
    LED
    Communication
)

pico_generate_pio_header(${PROJECT_NAME}
    ${CMAKE_CURRENT_LIST_DIR}/PIO/read.pio
)

pico_add_extra_outputs(${PROJECT_NAME})


target_link_libraries(${PROJECT_NAME}
    pico_stdlib
    pico_multicore

    hardware_gpio
    hardware_pio
    hardware_clocks
    hardware_dma
    hardware_irq
)

if (PICO_BOARD STREQUAL "pico_w")
target_link_libraries(${PROJECT_NAME}
    pico_cyw43_arch_none
)
endif()



pico_enable_stdio_usb(${PROJECT_NAME}  ${ENABLE_USB})
pico_enable_stdio_uart(${PROJECT_NAME} ${ENABLE_UART})