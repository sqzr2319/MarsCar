from machine import Pin, PWM
import time

# 配置参数 - 根据你的接线修改！
pwm_pin_number = 14  # 对应舵机接口5 (GPIO14)
MIN_PULSE_WIDTH = 1000  # 最小油门脉冲宽度 (微秒)
MAX_PULSE_WIDTH = 2000  # 最大油门脉冲宽度 (微秒)
STOP_PULSE_WIDTH = 1000  # 停止油门脉冲宽度 (微秒)
FREQUENCY = 50          # PWM频率 (Hz)
PERIOD_US = 1000000 // FREQUENCY  # 周期(微秒) = 20,000us

# 初始化引脚和PWM对象
def init_pwm():
    try:
        # 创建Pin对象并初始化为输出模式
        pwm_pin = Pin(pwm_pin_number, Pin.OUT)
        
        # 初始化为低电平确保安全
        pwm_pin.value(0)
        
        # 创建PWM对象
        esc_pwm = PWM(pwm_pin, freq=FREQUENCY)
        
        # 初始占空比设为0 (安全状态)
        esc_pwm.duty_u16(0)
        
        print(f"PWM initialized on GPIO{pwm_pin_number}")
        print(f"频率: {FREQUENCY}Hz, 周期: {PERIOD_US}us")
        return esc_pwm
    except Exception as e:
        print(f"PWM初始化失败: {e}")
        return None

# 关键函数：设置油门
def set_throttle(esc_pwm, pulse_width_us):
    if esc_pwm is None:
        print("错误: PWM未初始化!")
        return
    
    # 确保油门值在安全范围内
    pulse_width_us = max(MIN_PULSE_WIDTH, min(pulse_width_us, MAX_PULSE_WIDTH))
    
    # 正确计算占空比 (使用duty_u16范围)
    duty = int(pulse_width_us * 65535 / PERIOD_US)
    
    # 设置占空比
    esc_pwm.duty_u16(duty)
    
    # 调试信息
    print(f"设置油门: {pulse_width_us}us -> 占空比: {duty}/65535")

# 电调校准函数
def calibrate_esc(esc_pwm):
    print("\n===== 电调校准模式 =====")
    print("注意: 请先断开电池连接!")
    print("1. 发送最大油门信号(2000us)")
    set_throttle(esc_pwm, 2000)
    
    input("2. 连接电池后按Enter...")
    print("听到'哔哔'两声后...")
    time.sleep(2)
    
    print("3. 发送最小油门信号(1000us)")
    set_throttle(esc_pwm, 1000)
    print("听到确认音后校准完成")
    time.sleep(3)
    
    print("校准完成! 现在可以正常使用")

# 主程序
if __name__ == "__main__":
    # 初始化PWM
    esc_pwm = init_pwm()
    
    if esc_pwm is None:
        print("无法初始化PWM，程序退出")
        while True:
            pass  # 阻塞执行
    
    print("重要: 确保电机螺旋桨已取下!")
    
    # 询问是否需要校准
    if input("是否需要电调校准? (y/n): ").lower() == 'y':
        calibrate_esc(esc_pwm)
    
    print("\n发送停止信号(1000us) - 等待ESC初始化...")
    
    # 发送停止信号
    set_throttle(esc_pwm, STOP_PULSE_WIDTH)
    time.sleep(5)  # 等待ESC初始化
    
    try:
        print("开始油门测试...")
        
        # 缓加速到最大油门
        print("加速...")
        for pulse in range(STOP_PULSE_WIDTH, MAX_PULSE_WIDTH + 1, 10):
            set_throttle(esc_pwm, pulse)
            time.sleep(0.05)  # 小延时使加速平滑
        
        print("在最大油门保持2秒")
        time.sleep(2)
        
        # 缓减速到最小油门
        print("减速...")
        for pulse in range(MAX_PULSE_WIDTH, STOP_PULSE_WIDTH - 1, -10):
            set_throttle(esc_pwm, pulse)
            time.sleep(0.05)
        
        print("测试完成，电机应已停止")
    
    except KeyboardInterrupt:
        print("用户中断")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 安全措施：确保最后发送停止信号
        set_throttle(esc_pwm, STOP_PULSE_WIDTH)
        print("安全: 发送停止信号")