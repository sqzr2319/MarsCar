'''
修改信息
作者：
日期：
esp32有3个串口，UART0给程序调试下载使用，一般做成TPYEC；
本程序是UART2,也就是2号串口
硬件上还预留了UART1，也就是串口1给其他扩展使用
'<': '>',   # Type1: <...> 格式
'{': '}',   # Type2: {...} 格式
'#': '!',   # Type3: #...! 格式
'$': '!'    # Type4: $...! 格式
'''
import machine
from machine import PWM
import time

#程序入口
if __name__ == '__main__':
    
    pwm = PWM(machine.Pin(14),freq=5000)
    pwm.duty(0)
    
    while True:
        pwm.duty(0)
        time.sleep(3)
        
        pwm.duty(50)
        time.sleep(5)
        
        pwm.duty(100)
        time.sleep(5)
        
        pwm.duty(200)
        time.sleep(5)
        
        pwm.duty(1023)
        time.sleep(5)