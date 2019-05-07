# 创建数据写入.xls文件
import xlwt

# 密码：123456 转码: Neiz5WXbTTFKNcMkYMgFFg==
studentNum = "20152649"
password = "Neiz5WXbTTFKNcMkYMgFFg=="
username = "凌峰"

workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
sheet1 = workbook.add_sheet("student_sheet")  # 新建sheet
sheet1.write(0, 0, "学号")  # 第1行第1列数据
sheet1.write(0, 1, "密码")  # 第1行第2列数据
sheet1.write(0, 2, "姓名")
sheet1.write(0, 3, "电话")
sheet1.write(0, 4, "邮箱")
data_number = 100  # 数据的个数
for i in range(1, data_number + 1):
    print("studentNum", studentNum)
    phone = "159" + studentNum
    print("phone", phone)
    email = studentNum + "@qq.com"
    print("email", email)
    sheet1.write(i, 0, studentNum)  # 第i行第1列数据
    sheet1.write(i, 1, password)  # 第i行第2列数据
    sheet1.write(i, 2, username)
    sheet1.write(i, 3, phone)
    sheet1.write(i, 4, email)
    studentNum = str(int(studentNum) + 1)
workbook.save(r'/root/pycharm_project_365/UserInfo.xls')  # 保存