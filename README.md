# Raspberry Pi Pico development platform for PlatformIO

**A few words in the beginning**
* **Version: 1.0.0** The project is a work in progress and is **very beta version** - there may be bugs...
* This project not an official platform and is based on [**pico-sdk**](https://github.com/raspberrypi/pico-sdk)
* Frameworks:
* * Baremetal ( pico-sdk as is, [TinyUSB](https://github.com/raspberrypi/tinyusb/tree/e0aa405d19e35dbf58cf502b8106455c1a3c2a5c) present but is not linked ) 
* * Arduino ( basic ... in progress )
* **Systems**
* * windows, windows_x8, windows_amd64
* * linux_x86_64, linux_armv6l, linux_armv7l, linux_armv8l
* * darwin_x86_64, darwin_i386
* [Baremetal Examples](https://github.com/Wiz-IO/wizio-pico/tree/main/examples/baremetal)
* [Arduino Examples](https://github.com/Wiz-IO/wizio-pico/tree/main/examples/arduino)
* [Framework code](https://github.com/Wiz-IO/framework-wizio-pico)
* Note: _I am in Home-Office, it's hard for me to test any hardware_

![pico](https://raw.githubusercontent.com/Wiz-IO/LIB/master/pico/pio-pico.jpg)

## Install Platform

PIO Home > Platforms > Advanced Installation 

paste https://github.com/Wiz-IO/wizio-pico

## Baremetal - New Project
PlatformIO -> Home -> New
* Enter Project Name - Board search '**WizIO-PICO**' boards - Select **Baremetal**
* Click BUILD and you will have basic template project
* For CPP project, rename main.c to main.cpp ( if you delete main file, builder will create new main.c as template )
* Open 'platformio.ini' and edit your settings
* Connect Pico as Mass Storage Device and UPLOAD

## Arduino - New Project
PlatformIO -> Home -> New
* Enter Project Name - Board search '**WizIO-PICO**' boards - Select **Arduino**
* Open 'platformio.ini' and edit your settings
* Connect Pico as Mass Storage Device and UPLOAD

## platformio.ini
```ini
[env:pico]
platform = wizio-pico
board = pico
framework = baremetal

upload_port   = select PICO-DRIVE:/ or select HARD-DRIVE:/ to save the UF2 file ( example C:/ )
monitor_port  = COM1
monitor_speed = 115200

;heap = size ; default Baremetal 2048, Arduino 65536
;boot = folder_name ; ( checksummed.S ) see folder framework-wizio-pico/common/boot2/
```

## TODO
* **USB**
* **Arduino**
* * Libraries ( ADC, PWM, SPI, Wire, etc )


## Thanks to

* [Ivan Kravets ( PlatformIO )](https://platformio.org/)
* [Comet Electronics](https://www.comet.bg/en/)

>If you want to help / support:   
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)
