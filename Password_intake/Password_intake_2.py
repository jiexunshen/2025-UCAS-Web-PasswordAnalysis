def extract_passwords(input_file, output_file):
    """
    从原始文件中提取第一个#和第二个#之间的密码部分

    参数:
    input_file: 输入文件名
    output_file: 输出文件名
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            lines = f_in.readlines()

        passwords = []

        for line in lines:
            line = line.strip()  # 去除首尾空白字符
            if line and '#' in line:  # 确保不是空行且包含#
                # 使用#分割
                parts = line.split('#')
                if len(parts) >= 3:  # 确保至少有两个#分隔符
                    # 第一个#和第二个#之间的部分是索引1的部分
                    password = parts[1].strip()  # 去除前后空格
                    passwords.append(password)
                else:
                    print(f"警告：行格式不正确，跳过: {line}")

        # 将密码写入新文件
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for password in passwords:
                f_out.write(password + '\n')

        print(f"成功提取 {len(passwords)} 个密码到 {output_file}")

        # 显示提取结果
        print("\n提取的密码列表：")
        for i, pwd in enumerate(passwords, 1):
            print(f"{i}: {pwd}")

    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except Exception as e:
        print(f"处理文件时出错：{e}")


# 更简洁的版本
def extract_passwords_simple():
    """简洁版本的密码提取函数"""
    try:
        with open('../data/www.csdn.net.txt', 'r', encoding='utf-8') as f:
            passwords = []
            for line in f:
                line = line.strip()
                if line and line.count('#') >= 2:
                    password = line.split('#')[1].strip()
                    passwords.append(password)

        with open('../Password_data/password_2.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(passwords))

        print(f"成功提取 {len(passwords)} 个密码")
        return passwords

    except Exception as e:
        print(f"错误: {e}")
        return []


# 使用示例
if __name__ == "__main__":
    input_filename = "../data/www.csdn.net.txt"
    output_filename = "../Password_data/password_2.txt"

    # 使用方法1：详细版本
    extract_passwords(input_filename, output_filename)

    print("\n" + "=" * 50 + "\n")

    # 使用方法2：简洁版本
    passwords = extract_passwords_simple()
    print("提取完成！")