import os
from collections import Counter
import matplotlib.pyplot as plt

# --- 1. 键盘布局和配置 ---

# QWERTY 键盘相邻键位定义 (只包含常用字母和数字、字符)
# 键值是当前键，键值是它在上下左右斜方向上的相邻键的集合。
KEYBOARD_ADJACENCY = {
    # 数字行
    '`': {'1', '~'}, '~': {'`', '1'},
    '1': {'`', '2', 'q', 'w', '!', '~'}, '!': {'1', '2', 'q', 'w'},
    '2': {'1', '3', 'q', 'w', 'e', '@', '!'}, '@': {'2', '3', 'w', 'e'},
    '3': {'2', '4', 'w', 'e', 'r', '#', '@'}, '#': {'3', '4', 'e', 'r'},
    '4': {'3', '5', 'e', 'r', 't', '$', '#'}, '$': {'4', '5', 'r', 't'},
    '5': {'4', '6', 'r', 't', 'y', '%', '$'}, '%': {'5', '6', 't', 'y'},
    '6': {'5', '7', 't', 'y', 'u', '^', '%'}, '^': {'6', '7', 'y', 'u'},
    '7': {'6', '8', 'y', 'u', 'i', '&', '^'}, '&': {'7', '8', 'u', 'i'},
    '8': {'7', '9', 'u', 'i', 'o', '*', '&'}, '*': {'8', '9', 'i', 'o'},
    '9': {'8', '0', 'i', 'o', 'p', '(', '*'}, '(': {'9', '0', 'o', 'p'},
    '0': {'9', '-', 'o', 'p', ')', '('}, ')': {'0', '-', 'p'},
    '-': {'0', '=', 'p', '[', '_', ')'}, '_': {'-', '=', '['},
    '=': {'-', '[', ']', '+'}, '+': {'=', '[', ']'},
    
    # 字母行 - 上排
    'q': {'1', '2', 'w', 'a', 's', 'tab'}, 
    'w': {'1', '2', '3', 'q', 'e', 'a', 's', 'd'}, 
    'e': {'2', '3', '4', 'w', 'r', 's', 'd', 'f'}, 
    'r': {'3', '4', '5', 'e', 't', 'd', 'f', 'g'},
    't': {'4', '5', '6', 'r', 'y', 'f', 'g', 'h'}, 
    'y': {'5', '6', '7', 't', 'u', 'g', 'h', 'j'},
    'u': {'6', '7', '8', 'y', 'i', 'h', 'j', 'k'}, 
    'i': {'7', '8', '9', 'u', 'o', 'j', 'k', 'l'},
    'o': {'8', '9', '0', 'i', 'p', 'k', 'l', ';'}, 
    'p': {'9', '0', '-', 'o', '[', 'l', ';'},
    '[': {'p', '-', '=', ']', ';', "'", '{'}, '{': {'[', ']', "'"},
    ']': {'[', '=', "'", '}', '{'}, '}': {']', "'"},
    
    # 字母行 - 中排
    'a': {'q', 'w', 's', 'z', 'x', 'caps'}, 
    's': {'q', 'w', 'e', 'a', 'd', 'z', 'x', 'c'}, 
    'd': {'w', 'e', 'r', 's', 'f', 'x', 'c', 'v'}, 
    'f': {'e', 'r', 't', 'd', 'g', 'c', 'v', 'b'},
    'g': {'r', 't', 'y', 'f', 'h', 'v', 'b', 'n'}, 
    'h': {'t', 'y', 'u', 'g', 'j', 'b', 'n', 'm'},
    'j': {'y', 'u', 'i', 'h', 'k', 'n', 'm', ','}, 
    'k': {'u', 'i', 'o', 'j', 'l', 'm', ',', '.'},
    'l': {'i', 'o', 'p', 'k', ';', '.', '/'}, 
    ';': {'o', 'p', '[', 'l', "'", '/', ':'}, ':': {';', "'", '/'},
    "'": {'[', ']', ';', '"', ':'}, '"': {"'"},
    
    # 字母行 - 下排
    'z': {'a', 's', 'x', 'shift'}, 
    'x': {'s', 'd', 'z', 'c'}, 
    'c': {'d', 'f', 'x', 'v'}, 
    'v': {'f', 'g', 'c', 'b'}, 
    'b': {'g', 'h', 'v', 'n'}, 
    'n': {'h', 'j', 'b', 'm'}, 
    'm': {'j', 'k', 'n', ','}, 
    ',': {'k', 'l', 'm', '.', '<'}, '<': {',', '.', '/'},
    '.': {'l', ';', ',', '/', '>'}, '>': {'.', '/', '?'},
    '/': {';', "'", '.', '?', ':'}, '?': {'/', "'", ':'},
}

# 定义通用的基础目录
BASE_DATA_DIR = 'data'
BASE_OUTPUT_DIR = 'analysis_results'
ANALYSIS_STEP = 'analysis_2_keyboard'

# --- 2. 辅助函数 ---

def get_paths(dataset_name):
    """根据数据集名称生成所有路径。"""
    file_path = os.path.join(BASE_DATA_DIR, dataset_name, f'{dataset_name}.txt')
    output_dir = os.path.join(BASE_OUTPUT_DIR, dataset_name, ANALYSIS_STEP)
    return file_path, output_dir

def create_output_directory(output_dir):
    """创建输出文件夹"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

# --- 3. 核心分析函数 ---

def check_keyboard_pattern(password, min_length=4):
    """
    检查密码是否包含至少 min_length 长度的键盘相邻模式。
    返回：(模式类型, 识别到的模式子串) 或 None。
    """
    password = password.strip().lower()  # 统一转为小写处理
    if len(password) < min_length:
        return None, None

    def check_sequence(pwd):
        """检查严格的数字/字母连续序列 (e.g., 1234, abcd)"""
        for i in range(len(pwd) - 1):
            if ord(pwd[i+1]) != ord(pwd[i]) + 1:
                return False
        return True

    def check_adjacency(pwd):
        """检查通用的相邻键模式 (e.g., qwerty, asdfgh)"""
        for i in range(len(pwd) - 1):
            char1 = pwd[i]
            char2 = pwd[i+1]
            if char1 not in KEYBOARD_ADJACENCY or char2 not in KEYBOARD_ADJACENCY.get(char1, set()):
                return False
        return True
    
    # 遍历密码，查找是否存在符合 min_length 长度的键盘模式子串
    for i in range(len(password) - min_length + 1):
        # 检查从 min_length 开始的所有可能子串 (寻找最长的匹配)
        for j in range(len(password), i + min_length - 1, -1):
            sub_pwd = password[i:j]

            # 严格的连续序列
            if sub_pwd.isdigit() or sub_pwd.isalpha():
                if check_sequence(sub_pwd):
                    return "Sequence", sub_pwd
            
            # 通用的相邻键模式
            if check_adjacency(sub_pwd):
                return "Adjacency", sub_pwd

    return None, None

def analyze_keyboard_patterns(passwords):
    """
    统计键盘密码模式的类型、频率以及高频模式子串。
    """
    pattern_counter = Counter()
    sequence_subpatterns = Counter()
    adjacency_subpatterns = Counter()
    
    total_passwords = len([p for p in passwords if p.strip()]) 
    
    for pwd in passwords:
        pwd = pwd.strip()
        if not pwd:
            continue
            
        pattern_type, sub_pattern = check_keyboard_pattern(pwd, min_length=4)  # 最小模式长度设为4
        
        if pattern_type == "Sequence":
            pattern_counter['Sequence (连续键)'] += 1
            sequence_subpatterns[sub_pattern] += 1
        elif pattern_type == "Adjacency":
            pattern_counter['Adjacency (相邻键)'] += 1
            adjacency_subpatterns[sub_pattern] += 1
        
    return pattern_counter, sequence_subpatterns, adjacency_subpatterns, total_passwords

# --- 4. 可视化和保存结果 ---

def plot_and_save_results(pattern_counter, sequence_subpatterns, adjacency_subpatterns, total_passwords, output_dir, dataset_name):
    
    # 计算是键盘模式的密码总数
    pattern_sum = sum(pattern_counter.values())
    non_pattern_count = total_passwords - pattern_sum
    
    # 准备饼图数据 (基础模式占比)
    labels = list(pattern_counter.keys())
    sizes = list(pattern_counter.values())
    if non_pattern_count > 0 or not sizes:
        labels.append('Other (非键盘模式)')
        sizes.append(non_pattern_count)
    
    if not sizes:
        print("数据集中没有有效密码或无法识别模式。")
        return

    # 1. 键盘模式分布饼图
    plt.figure(figsize=(10, 6))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#cccccc'] 
    
    plt.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90, 
            wedgeprops={'edgecolor': 'black'}, pctdistance=0.75, colors=colors)
    plt.title(f'{dataset_name.upper()} Keyboard Pattern Analysis (Min 4 Keys)')
    plt.axis('equal')
    plt.tight_layout()
    
    filename_png = f'01_{dataset_name}_keyboard_pattern_pie.png'
    plt.savefig(os.path.join(output_dir, filename_png))
    plt.close()
    
    # 2. 文本报告 (包含 Top 10 子串)
    filename_txt = f'02_{dataset_name}_keyboard_pattern_report.txt'
    with open(os.path.join(output_dir, filename_txt), 'w', encoding='utf-8') as f:
        f.write(f"--- {dataset_name.upper()} 键盘密码模式分析报告 ---\n\n")
        f.write(f"总密码数: {total_passwords}\n")
        f.write(f"识别出的键盘模式密码数: {pattern_sum}\n")
        f.write(f"键盘模式密码占比: {pattern_sum/total_passwords * 100:.2f}%\n\n")
        f.write("-" * 40 + "\n")
        
        # 模式类型频率统计
        f.write("{:<25} {:>10} {:>10}\n".format("模式类型", "频率 (Count)", "占比 (%)"))
        f.write("-" * 40 + "\n")
        
        for pattern, count in pattern_counter.items():
            percentage = (count / total_passwords) * 100
            f.write("{:<25} {:>10} {:>10.2f}\n".format(pattern, count, percentage))

        if non_pattern_count > 0:
             non_pattern_percentage = (non_pattern_count / total_passwords) * 100
             f.write("{:<25} {:>10} {:>10.2f}\n".format('Other (非键盘模式)', non_pattern_count, non_pattern_percentage))
        
        # --- 高频连续键模式输出 ---
        f.write("\n\n" + "=" * 40 + "\n")
        f.write("## 3. 高频连续键模式 (Sequence, Top 10)\n")
        f.write("=" * 40 + "\n")
        f.write("{:<20} {:>10}\n".format("子串 (Sub-Pattern)", "频率 (Count)"))
        f.write("-" * 31 + "\n")
        
        top_sequences = sequence_subpatterns.most_common(10)
        for sub_pattern, count in top_sequences:
            f.write("{:<20} {:>10}\n".format(sub_pattern, count))

        # --- 高频相邻键模式输出 ---
        f.write("\n\n" + "=" * 40 + "\n")
        f.write("## 4. 高频相邻键模式 (Adjacency, Top 10)\n")
        f.write("=" * 40 + "\n")
        f.write("{:<20} {:>10}\n".format("子串 (Sub-Pattern)", "频率 (Count)"))
        f.write("-" * 31 + "\n")
        
        top_adjacencies = adjacency_subpatterns.most_common(10)
        for sub_pattern, count in top_adjacencies:
            f.write("{:<20} {:>10}\n".format(sub_pattern, count))


# --- 5. 主执行函数 (参数化) ---

def run_analysis(dataset_name):
    """主程序入口"""
    file_path, output_dir = get_paths(dataset_name)
    
    create_output_directory(output_dir)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = f.readlines()
        
        print(f"共读取 {len(passwords)} 条口令。")

        pattern_counter, sequence_subpatterns, adjacency_subpatterns, total_passwords = analyze_keyboard_patterns(passwords)
        
        plot_and_save_results(pattern_counter, sequence_subpatterns, adjacency_subpatterns, total_passwords, output_dir, dataset_name)

        print(f"结果已保存在目录: {output_dir}")

    except Exception as e:
        print(f"分析过程中发生错误: {e}")

if __name__ == '__main__':
    
    # 如需修改只需要在这里切换数据集名称
    
    # DATASET_TO_ANALYZE = 'yahoo'
    DATASET_TO_ANALYZE = 'csdn'
    
    run_analysis(DATASET_TO_ANALYZE)