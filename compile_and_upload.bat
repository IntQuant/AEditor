del main.elf main.hex

echo "Compiling"
avr-gcc -mmcu=atmega328p code.C -o main.elf
echo "Converting"
avr-objcopy -j .text -O ihex main.elf main.hex
avrdude -v -patmega328p -carduino -P/dev/ttyUSB0 -b115200 -D -Uflash:w:main.hex:i
