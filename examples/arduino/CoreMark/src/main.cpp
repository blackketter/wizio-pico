#include <Arduino.h>

// CoreMark Benchmark for Arduino compatible boards
//   original CoreMark code: https://github.com/eembc/coremark

#include <stdarg.h>

// A way to call the C-only coremark function from Arduino's C++ environment
extern "C" int coremark_main(void);

void setup()
{
  //set_sys_clock_khz(250000, false);

  Serial.begin(115200);
  while (!Serial)
    ; // wait for Arduino Serial Monitor
  delay(500);
  Serial.println("CoreMark Performance Benchmark");
  Serial.println();
  Serial.println("CoreMark measures how quickly your processor can manage linked");
  Serial.println("lists, compute matrix multiply, and execute state machine code.");
  Serial.println();
  Serial.println("Iterations/Sec is the main benchmark result, higher numbers are better");
  Serial.println("Running.... (usually requires 12 to 20 seconds)");
  Serial.println();
  delay(250);
  coremark_main(); // Run the benchmark  :-)
}

void loop()
{
}

// CoreMark calls this function to print results.
extern "C" int ee_printf(const char *format, ...)
{
  va_list args;
  va_start(args, format);
  for (; *format; format++)
  {
    if (*format == '%')
    {
      bool islong = false;
      format++;
      if (*format == '%')
      {
        Serial.print(*format);
        continue;
      }
      if (*format == '-')
        format++; // ignore size
      while (*format >= '0' && *format <= '9')
        format++; // ignore size
      if (*format == 'l')
      {
        islong = true;
        format++;
      }
      if (*format == '\0')
        break;
      if (*format == 's')
      {
        Serial.print((char *)va_arg(args, int));
      }
      else if (*format == 'f')
      {
        Serial.print(va_arg(args, double));
      }
      else if (*format == 'd')
      {
        if (islong)
          Serial.print(va_arg(args, long));
        else
          Serial.print(va_arg(args, int));
      }
      else if (*format == 'u')
      {
        if (islong)
          Serial.print(va_arg(args, unsigned long));
        else
          Serial.print(va_arg(args, unsigned int));
      }
      else if (*format == 'x')
      {
        if (islong)
          Serial.print(va_arg(args, unsigned long), HEX);
        else
          Serial.print(va_arg(args, unsigned int), HEX);
      }
      else if (*format == 'c')
      {
        Serial.print(va_arg(args, int));
      }
    }
    else
    {
      if (*format == '\n')
        Serial.print('\r');
      Serial.print(*format);
    }
  }
  va_end(args);
  return 1;
}

// CoreMark calls this function to measure elapsed time
extern "C" uint32_t Arduino_millis(void)
{
  return millis();
}

/* 
CoreMark Performance Benchmark - 48 MHz
CoreMark measures how quickly your processor can manage linked lists, compute matrix multiply, and execute state machine code.
Iterations/Sec is the main benchmark result, higher numbers are better
Running.... (usually requires 12 to 20 seconds)
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 13644
Total time (secs): 13.64
Iterations/Sec   : 146.58
Iterations       : 2000
Compiler version : GCC7.2.1 20170904 (release) [ARM/embedded-7-branch revision 255204]
Compiler flags   : (flags unknown)
Memory location  : STACK
seedcrc          : 0xE9F5
[0]crclist       : 0xE714
[0]crcmatrix     : 0x1FD7
[0]crcstate      : 0x8E3A
[0]crcfinal      : 0x4983
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 146.58 / GCC7.2.1 20170904 (release) [ARM/embedded-7-branch revision 255204] (flags unknown) / STACK
*/

/*
CoreMark Performance Benchmark - 250 Mhz
CoreMark measures how quickly your processor can manage linked lists, compute matrix multiply, and execute state machine code.
Iterations/Sec is the main benchmark result, higher numbers are better
Running.... (usually requires 12 to 20 seconds)
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 13643
Total time (secs): 13.64
Iterations/Sec   : 293.19
Iterations       : 4000
Compiler version : GCC7.2.1 20170904 (release) [ARM/embedded-7-branch revision 255204]
Compiler flags   : (flags unknown)
Memory location  : STACK
seedcrc          : 0xE9F5
[0]crclist       : 0xE714
[0]crcmatrix     : 0x1FD7
[0]crcstate      : 0x8E3A
[0]crcfinal      : 0x65C5
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 293.19 / GCC7.2.1 20170904 (release) [ARM/embedded-7-branch revision 255204] (flags unknown) / STACK
*/