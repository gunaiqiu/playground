import pyqrcode
import os

def generate_qr_code(data: str) -> str:
    qr = pyqrcode.create(data)
    return qr.terminal(quiet_zone=1)  

def clear_screen():
    # 清除屏幕，根据操作系统选择方法
    os.system('cls' if os.name == 'nt' else 'clear')
    
print("请输入多行字符串，每行一个任务（输入空行结束）:")
lines = []
while True:
    line = input()
    if not line:  # 空行表示输入结束
        break
    lines.append(line.strip())  # 去除行尾的换行符和可能的空白字符

for line in lines:
    if line:  # 确保行不为空
        clear_screen()
        print(generate_qr_code(line))
        input("回车下一个或按Ctrl+C退出...")  # 等待用户按下回车或提供退出选项