.equ F_CPU = 8000000
.equ USART_BAUD = 9600

.equ TIMER1_INTERVAL = 500
.equ TIMER2_INTERVAL = 1000

.def TEMP = R16

.equ TIMER1_STR = "ping\r\n"
.equ TIMER2_STR = "pong\r\n"

.org 0x0000
rjmp main

.org 0x0024
rjmp timer1_isr

.org 0x0032
rjmp timer2_isr

.org 0x0040
rjmp usart_tx_empty_isr

main:
  ldi TEMP, low(RAMEND)
  out SPL, TEMP
  ldi TEMP, high(RAMEND)
  out SPH, TEMP

  ldi TEMP, low((F_CPU / (16 * USART_BAUD)) - 1)
  out UBRRH, TEMP
  ldi TEMP, high((F_CPU / (16 * USART_BAUD)) - 1)
  out UBRRL, TEMP
  ldi TEMP, (1 << TXEN) | (1 << RXEN)
  out UCSRB, TEMP
  ldi TEMP, (1 << UCSZ1) | (1 << UCSZ0)
  out UCSRC, TEMP

  ldi TEMP, (1 << WGM12) | (1 << CS11)
  out TCCR1B, TEMP
  ldi TEMP, (F_CPU / 8) * TIMER1_INTERVAL / 1000 - 1
  out OCR1AH, TEMP
  ldi TEMP, TEMP >> 8
  out OCR1AL, TEMP
  ldi TEMP, (1 << OCIE1A)
  out TIMSK, TEMP

  ldi TEMP, (1 << WGM21) | (1 << CS22) | (1 << CS21) | (1 << CS20)
  out TCCR2, TEMP
  ldi TEMP, F_CPU / 1024 * TIMER2_INTERVAL / 1000 - 1
  out OCR2, TEMP
  ldi TEMP, (1 << OCIE2)
  out TIMSK, TEMP

  sei

main_loop:
  rjmp main_loop

timer1_isr:
  ldi TEMP, low(TIMER1_STR)
  call usart_send_string
  reti

timer2_isr:
  ldi TEMP, low(TIMER2_STR)
  call usart_send_string
  reti

usart_send_string:
  movw ZL, TEMP

usart_send_string_loop:
  ld TEMP, Z+
  cp TEMP, r1
  brne usart_send_char
  ret

usart_send_char:
  sbis UCSRA, UDRE
  rjmp usart_send_char

  out UDR, TEMP
  ret