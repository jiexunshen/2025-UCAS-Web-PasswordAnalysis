def extract_passwords(input_file, output_file):
    """
    从原始文件中提取密码部分并保存到新文件

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
            if line:  # 确保不是空行
                # 使用冒号分割，取最后一个部分作为密码
                parts = line.split(':')
                if len(parts) >= 2:  # 确保有冒号分隔
                    password = parts[-1]  # 取最后一个部分（密码）
                    passwords.append(password)

        # 将密码写入新文件
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for password in passwords:
                f_out.write(password + '\n')

        print(f"成功提取 {len(passwords)} 个密码到 {output_file}")

    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
    except Exception as e:
        print(f"处理文件时出错：{e}")


# 使用示例
if __name__ == "__main__":
    input_filename = "../data/plaintxt_yahoo.txt"
    output_filename = "../Password_data/password_1.txt"

    extract_passwords(input_filename, output_filename)

    # 可选：显示提取结果
    print("\n提取的密码内容：")
    try:
        with open(output_filename, 'r', encoding='utf-8') as f:
            print(f.read())
    except:
        pass