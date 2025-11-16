import os
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# --- 1. 配置和文件路径生成函数 ---

BASE_DATA_DIR = 'data'
BASE_OUTPUT_DIR = 'analysis_results'
ANALYSIS_STEP = 'analysis_1_composition'

def get_paths(dataset_name):
    """根据数据集名称生成所有路径。"""
    file_path = os.path.join(BASE_DATA_DIR, dataset_name, f'{dataset_name}.txt')
    output_dir = os.path.join(BASE_OUTPUT_DIR, dataset_name, ANALYSIS_STEP)
    return file_path, output_dir

def create_output_directory(output_dir):
    """创建输出文件夹"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

# --- 2. 核心分析函数 (get_char_type, extract_structure_pattern, analyze_element_composition ---

def get_char_type(char):
    if char.islower(): return 'L'
    if char.isupper(): return 'U'
    if char.isdigit(): return 'D'
    if not char.isalnum(): return 'S'
    return 'O' 

def extract_structure_pattern(password):
    password = password.strip()
    if not password: return None
    pattern_parts = []
    current_char_type = get_char_type(password[0])
    count = 1
    for i in range(1, len(password)):
        next_char_type = get_char_type(password[i])
        if next_char_type == current_char_type:
            count += 1
        else:
            pattern_parts.append(f"{current_char_type}{count}")
            current_char_type = next_char_type
            count = 1
    pattern_parts.append(f"{current_char_type}{count}")
    return "".join(pattern_parts)

def analyze_element_composition(passwords):
    lengths_counter = Counter()
    composition_counter = Counter()
    for pwd in passwords:
        pwd = pwd.strip()
        if not pwd: continue
        lengths_counter[len(pwd)] += 1
        has_lower = any(c.islower() for c in pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_symbol = any(not c.isalnum() for c in pwd)
        composition = []
        if has_lower: composition.append('L')
        if has_upper: composition.append('U')
        if has_digit: composition.append('D')
        if has_symbol: composition.append('S')
        composition_counter['+'.join(composition)] += 1
    return lengths_counter, composition_counter


def analyze_pattern_structure(passwords):
    """
    统计密码中最常见的结构模式，并记录每个模式下所有实际口令的频率。
    返回: 
        - pattern_counter: 结构模式的频率计数
        - password_by_pattern: defaultdict(Counter)，存储每个模式下的口令频率
    """
    pattern_counter = Counter()
    password_by_pattern = defaultdict(Counter) 
    
    for pwd in passwords:
        pwd_stripped = pwd.strip()
        if not pwd_stripped:
            continue
            
        pattern = extract_structure_pattern(pwd_stripped)
        if pattern:
            pattern_counter[pattern] += 1
            # 记录该模式下，这个口令出现的次数
            password_by_pattern[pattern][pwd_stripped] += 1
            
    return pattern_counter, password_by_pattern

# --- 3. 可视化和保存函数---

def plot_and_save_results(lengths_counter, composition_counter, pattern_counter, password_by_pattern, output_dir, dataset_name):
    """生成图表和结果文件，包含每个模式下的 Top 10 口令。"""
    
    # 1. 密码长度分布图
    plt.figure(figsize=(12, 6))
    top_lengths = dict(lengths_counter.most_common(30))
    lengths = sorted(top_lengths.keys())
    counts = [top_lengths[l] for l in lengths]

    plt.bar(lengths, counts, color='skyblue')
    plt.xlabel('Password Length')
    plt.ylabel('Frequency')
    plt.title(f'{dataset_name.upper()} Passwords Length Distribution (Top 30)')
    plt.xticks(lengths, rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    filename_png = f'01_{dataset_name}_length_distribution.png' 
    plt.savefig(os.path.join(output_dir, filename_png))
    plt.close()
    
    # 2. 元素构成组合图
    plt.figure(figsize=(10, 6))
    top_composition = composition_counter.most_common(10)
    labels = [item[0] for item in top_composition]
    sizes = [item[1] for item in top_composition]

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
            wedgeprops={'edgecolor': 'black'}, pctdistance=0.85)
    plt.title(f'Top 10 Password Element Combinations in {dataset_name.upper()}')
    plt.axis('equal')
    plt.tight_layout()
    filename_png_comp = f'02_{dataset_name}_element_composition.png'
    plt.savefig(os.path.join(output_dir, filename_png_comp))
    plt.close()

    # 3. 结构模式分析结果 (文本保存 Top 20 模式及其 Top 10 口令)
    
    top_patterns = pattern_counter.most_common(20)
    filename_txt = f'03_{dataset_name}_structure_patterns_with_top_passwords.txt'
    
    with open(os.path.join(output_dir, filename_txt), 'w', encoding='utf-8') as f:
        f.write(f"--- {dataset_name.upper()} 密码结构模式及高频口令分析结果 ---\n\n")
        f.write("模式说明：L=小写字母, U=大写字母, D=数字, S=符号, O=其他。数字表示连续出现的次数。\n\n")
        
        f.write("=" * 60 + "\n")
        f.write("{:<10} {:<20} {:>10}\n".format("Rank", "Pattern (模式)", "Total Count"))
        f.write("=" * 60 + "\n")

        for rank, (pattern, total_count) in enumerate(top_patterns, 1):
            f.write(f"\n--- Rank {rank}: Pattern {pattern} (Count: {total_count}) ---\n")
            f.write("{:<4} {:<30} {:>10}\n".format("Sub", "Password", "Count"))
            f.write("-" * 45 + "\n")
            
            # 获取该模式下频率最高的 Top 10 口令
            top_passwords = password_by_pattern[pattern].most_common(10)
            
            for sub_rank, (pwd, count) in enumerate(top_passwords, 1):
                # 限制口令长度，避免排版混乱
                display_pwd = pwd if len(pwd) <= 28 else pwd[:25] + "..."
                f.write("{:<4} {:<30} {:>10}\n".format(sub_rank, display_pwd, count))

    
    # 4. 模式分布柱状图 (Top 10)
    plt.figure(figsize=(14, 7))
    top_10_patterns_plot = top_patterns[:10]
    patterns = [item[0] for item in top_10_patterns_plot]
    counts = [item[1] for item in top_10_patterns_plot]

    plt.bar(patterns, counts, color='coral')
    plt.xlabel('Password Structure Pattern (L/U/D/S)')
    plt.ylabel('Frequency')
    plt.title(f'Top 10 Most Common Password Structure Patterns in {dataset_name.upper()}')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    filename_png_pattern = f'04_{dataset_name}_top_patterns_distribution.png'
    plt.savefig(os.path.join(output_dir, filename_png_pattern))
    plt.close()


# --- 4. 主执行函数 ---

def run_analysis(dataset_name):
    """主程序入口"""
    file_path, output_dir = get_paths(dataset_name)
    
    create_output_directory(output_dir)

    if not os.path.exists(file_path):
        print(f"错误：文件未找到 -> {file_path}")
        return

    print(f"正在读取文件: {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = f.readlines()
        
        print(f"共读取 {len(passwords)} 条口令。")

        # A. 构成元素分析
        lengths_counter, composition_counter = analyze_element_composition(passwords)
        
        # B. 结构模式分析 (返回模式计数和口令-按模式分组)
        pattern_counter, password_by_pattern = analyze_pattern_structure(passwords)

        # C. 可视化和保存
        plot_and_save_results(lengths_counter, composition_counter, pattern_counter, password_by_pattern, output_dir, dataset_name)

        print(f"结果文件和图表已保存在目录: {output_dir}")

    except Exception as e:
        print(f"分析过程中发生错误: {e}")

if __name__ == '__main__':
    
    # 如需修改只需要在这里切换数据集名称
    
    # DATASET_TO_ANALYZE = 'yahoo'
    DATASET_TO_ANALYZE = 'csdn'
    
    run_analysis(DATASET_TO_ANALYZE)