import random
import time
from datetime import datetime, timedelta

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

#def generate_employee_id():
 #   return random.randint(10000, 99999)
def idCardCheck():
    # 地址码
    addr_code = ''.join(random.choice('1234567890') for _ in range(6))
    # 随机生成一个在1995-2002之间的年份
    year = random.randint(1995, 2002)
    # 生成随机的月和日
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # 为了简单起见，这里假设每个月都有28天
    # 出生日期码
    birth_code = '{:04d}{:02d}{:02d}'.format(year, month, day)
    # 顺序码
    order_code = ''.join(random.choice('1234567890') for _ in range(3))
    # 计算校验位
    check_code = calculate_check_code(addr_code + birth_code + order_code)
    # 返回身份证号码
    return addr_code + birth_code + order_code + check_code

def calculate_check_code(id17):
    # 加权因子
    weight_factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码映射
    check_code_dict = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
    # 计算校验位
    sum = 0
    for i in range(0, len(id17)):
        sum += int(id17[i]) * weight_factor[i]
    return check_code_dict[sum % 11]

def generate_employee():
    start = datetime(2023, 10, 1)
    end = datetime(2024, 6, 30)
    employee = {
        "idCard": idCardCheck(),
        "name": "Employee",
        "gender": random.choice(["Male", "Female"]),
        "phoneNumber": "13" + str(random.randint(100000000, 999999999)),
        "address": "Address",
        "salary": random.randint(5000, 20000),
        "hireDate": random_date(start, end).strftime("%Y-%m-%d"),
        "position": "Position",
        "departmentId": random.randint(1, 10)
    }
    return employee

employees = []
for _ in range(10):  # Generate 10 employees
    employee = generate_employee()
    employees.append(employee)

for employee in employees:
    print(employee)