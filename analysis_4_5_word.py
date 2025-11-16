import re
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from Constants import COMMON_PINYIN, COMMON_CHINESE_NAMES, COMMON_ENGLISH_WORDS
    from Chinese import (
        is_chinese_char,
        extract_chinese_text,
        chinese_to_pinyin,
        extract_pinyin_from_text,
        analyze_pinyin_usage
    )
    from English import (
        extract_english_words,
        analyze_word_usage
    )
    from Chart import create_statistical_charts
except ImportError as e:
    print(f"导入模块时出错: {e}")
    print("请确保 Constants.py, Chinese.py, English.py 和 Chart.py 文件都在同一目录下")
    sys.exit(1)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
def load_passwords(filename):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        return passwords
    except FileNotFoundError:
        print(f"错误：找不到文件 {filename}")
        return []
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return []
def print_top10(title, counter, case_stats=None):
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}")
    if not counter:
        print("没有找到相关数据")
        return
    print(f"\nTop 10 使用统计:")
    print("-" * 40)
    for i, (item, count) in enumerate(counter.most_common(10), 1):
        print(f"{i:2d}. {item:<15} - 出现次数: {count}")
    if case_stats:
        print(f"\n大小写使用统计:")
        print("-" * 40)
        total = sum(case_stats.values())
        if total > 0:
            for case_type, count in case_stats.items():
                percentage = (count / total) * 100
                print(f"{case_type:<15}: {count:>4} 次 ({percentage:>5.1f}%)")
def save_statistics_to_file(passwords, pinyin_counter, pinyin_case_stats,
                            word_counter, word_case_stats, pinyin_combination_counter=None, filename="total.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("密码分析统计报告\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"总共分析密码数量: {len(passwords)}\n")
        chinese_passwords = [pwd for pwd in passwords if any(is_chinese_char(char) for char in pwd)]
        f.write(f"包含中文字符的密码数量: {len(chinese_passwords)}\n")
        word_passwords = [pwd for pwd in passwords if any(len(word) >= 2 for word in re.findall(r'[a-zA-Z]+', pwd))]
        f.write(f"包含英文单词的密码数量: {len(word_passwords)}\n")
        if passwords:
            avg_length = sum(len(pwd) for pwd in passwords) / len(passwords)
            max_length = max(len(pwd) for pwd in passwords)
            min_length = min(len(pwd) for pwd in passwords)
            f.write(f"密码长度统计 - 平均: {avg_length:.1f}, 最短: {min_length}, 最长: {max_length}\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("拼音使用统计\n")
        f.write("=" * 60 + "\n\n")
        if pinyin_counter:
            f.write("Top 20 拼音使用统计:\n")
            f.write("-" * 40 + "\n")
            for i, (item, count) in enumerate(pinyin_counter.most_common(20), 1):
                f.write(f"{i:2d}. {item:<15} - 出现次数: {count}\n")
            f.write("\n拼音大小写使用统计:\n")
            f.write("-" * 40 + "\n")
            total = sum(pinyin_case_stats.values())
            if total > 0:
                for case_type, count in pinyin_case_stats.items():
                    percentage = (count / total) * 100
                    f.write(f"{case_type:<15}: {count:>4} 次 ({percentage:>5.1f}%)\n")
        else:
            f.write("没有找到拼音数据\n")
        if pinyin_combination_counter and len(pinyin_combination_counter) > 0:
            f.write("\n拼音组合使用统计:\n")
            f.write("-" * 40 + "\n")
            for i, (item, count) in enumerate(pinyin_combination_counter.most_common(10), 1):
                f.write(f"{i:2d}. {item:<20} - 出现次数: {count}\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("英文单词使用统计\n")
        f.write("=" * 60 + "\n\n")
        if word_counter:
            f.write("Top 20 英文单词使用统计:\n")
            f.write("-" * 40 + "\n")
            for i, (item, count) in enumerate(word_counter.most_common(20), 1):
                f.write(f"{i:2d}. {item:<15} - 出现次数: {count}\n")
            f.write("\n英文单词大小写使用统计:\n")
            f.write("-" * 40 + "\n")
            total = sum(word_case_stats.values())
            if total > 0:
                for case_type, count in word_case_stats.items():
                    percentage = (count / total) * 100
                    f.write(f"{case_type:<15}: {count:>4} 次 ({percentage:>5.1f}%)\n")
        else:
            f.write("没有找到英文单词数据\n")
    print(f"统计数据已保存到 {filename}")
def save_all_statistics_to_file(passwords, pinyin_counter, pinyin_case_stats,
                                word_counter, word_case_stats, pinyin_combination_counter=None, filename="total_2.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("完整密码分析统计报告\n")
        f.write("=" * 60 + "\n\n")
        # 基本统计
        f.write(f"总共分析密码数量: {len(passwords)}\n")
        # 包含中文的密码数量
        chinese_passwords = [pwd for pwd in passwords if any(is_chinese_char(char) for char in pwd)]
        f.write(f"包含中文字符的密码数量: {len(chinese_passwords)}\n")
        # 包含英文单词的密码数量
        word_passwords = [pwd for pwd in passwords if any(len(word) >= 2 for word in re.findall(r'[a-zA-Z]+', pwd))]
        f.write(f"包含英文单词的密码数量: {len(word_passwords)}\n")
        # 密码长度统计
        if passwords:
            avg_length = sum(len(pwd) for pwd in passwords) / len(passwords)
            max_length = max(len(pwd) for pwd in passwords)
            min_length = min(len(pwd) for pwd in passwords)
            f.write(f"密码长度统计 - 平均: {avg_length:.1f}, 最短: {min_length}, 最长: {max_length}\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("拼音使用统计（完整列表）\n")
        f.write("=" * 60 + "\n\n")
        if pinyin_counter:
            f.write(f"总共发现 {len(pinyin_counter)} 种不同的拼音\n")
            f.write(f"拼音总出现次数: {sum(pinyin_counter.values())}\n\n")
            f.write("所有拼音使用统计（按出现频率排序）:\n")
            f.write("-" * 40 + "\n")
            for i, (item, count) in enumerate(pinyin_counter.most_common(), 1):
                f.write(f"{i:4d}. {item:<15} - 出现次数: {count}\n")
            f.write("\n拼音大小写使用统计:\n")
            f.write("-" * 40 + "\n")
            total = sum(pinyin_case_stats.values())
            if total > 0:
                for case_type, count in pinyin_case_stats.items():
                    percentage = (count / total) * 100
                    f.write(f"{case_type:<15}: {count:>4} 次 ({percentage:>5.1f}%)\n")
        else:
            f.write("没有找到拼音数据\n")
        if pinyin_combination_counter and len(pinyin_combination_counter) > 0:
            f.write("\n拼音组合使用统计（完整列表）:\n")
            f.write("-" * 40 + "\n")
            for i, (item, count) in enumerate(pinyin_combination_counter.most_common(), 1):
                f.write(f"{i:4d}. {item:<20} - 出现次数: {count}\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("英文单词使用统计（完整列表）\n")
        f.write("=" * 60 + "\n\n")
        if word_counter:
            f.write(f"总共发现 {len(word_counter)} 种不同的英文单词\n")
            f.write(f"英文单词总出现次数: {sum(word_counter.values())}\n\n")
            f.write("所有英文单词使用统计（按出现频率排序）:\n")
            f.write("-" * 40 + "\n")
            for i, (item, count) in enumerate(word_counter.most_common(), 1):
                f.write(f"{i:4d}. {item:<15} - 出现次数: {count}\n")
            f.write("\n英文单词大小写使用统计:\n")
            f.write("-" * 40 + "\n")
            total = sum(word_case_stats.values())
            if total > 0:
                for case_type, count in word_case_stats.items():
                    percentage = (count / total) * 100
                    f.write(f"{case_type:<15}: {count:>4} 次 ({percentage:>5.1f}%)\n")
        else:
            f.write("没有找到英文单词数据\n")
    print(f"完整统计数据已保存到 {filename}")
def detailed_analysis(passwords):
    print("开始分析密码文件...")
    print(f"总共分析 {len(passwords)} 个密码")
    print("\n正在分析拼音使用情况...")
    pinyin_counter, pinyin_case_stats, pinyin_combination_counter = analyze_pinyin_usage(passwords)
    print_top10("拼音使用统计", pinyin_counter, pinyin_case_stats)
    if pinyin_combination_counter and len(pinyin_combination_counter) > 0:
        print(f"\n拼音组合使用统计:")
        print("-" * 40)
        for i, (item, count) in enumerate(pinyin_combination_counter.most_common(10), 1):
            print(f"{i:2d}. {item:<20} - 出现次数: {count}")
    print("\n正在分析英文单词使用情况...")
    word_counter, word_case_stats = analyze_word_usage(passwords)
    print_top10("英文单词使用统计", word_counter, word_case_stats)
    print(f"\n{'=' * 60}")
    print("额外统计信息")
    print(f"{'=' * 60}")
    chinese_passwords = [pwd for pwd in passwords if any(is_chinese_char(char) for char in pwd)]
    print(f"包含中文字符的密码数量: {len(chinese_passwords)}")
    word_passwords = [pwd for pwd in passwords if any(len(word) >= 2 for word in re.findall(r'[a-zA-Z]+', pwd))]
    print(f"包含英文单词的密码数量: {len(word_passwords)}")
    if passwords:
        avg_length = sum(len(pwd) for pwd in passwords) / len(passwords)
        max_length = max(len(pwd) for pwd in passwords)
        min_length = min(len(pwd) for pwd in passwords)
        print(f"密码长度统计 - 平均: {avg_length:.1f}, 最短: {min_length}, 最长: {max_length}")
    save_statistics_to_file(passwords, pinyin_counter, pinyin_case_stats,
                            word_counter, word_case_stats, pinyin_combination_counter, "total.txt")

    save_all_statistics_to_file(passwords, pinyin_counter, pinyin_case_stats,
                                word_counter, word_case_stats, pinyin_combination_counter, "total_2.txt")
    create_statistical_charts(pinyin_counter, pinyin_case_stats,
                              word_counter, word_case_stats, pinyin_combination_counter, "total.png")
def main():
    """主函数"""


    # 调用时只需直接切换
    # filename = "data\csdn\csdn.txt"
    filename = "data\yahoo\yahoo.txt"


    if not os.path.exists(filename):
        print(f"错误：文件 {filename} 不存在")
        print("请确保文件路径正确，并且Password_data目录存在")
        return
    passwords = load_passwords(filename)
    if not passwords:
        print("没有找到密码数据，程序退出。")
        return
    detailed_analysis(passwords)
    print("\n分析完成！")
    print("统计结果已保存到 total.txt")
    print("完整统计结果已保存到 total_2.txt")
    print("统计图表已保存到 total.png")
if __name__ == "__main__":
    main()