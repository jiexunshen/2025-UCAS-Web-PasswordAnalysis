import os
import re

def extract_by_re(file_path: str, pattern: str):
    regex = re.compile(pattern, re.MULTILINE)
    with open(file_path, "r", encoding="utf-8") as f:
        return regex.findall(f.read())

def write_passwords(file_path: str, pattern_file_pairs):
    passwords = []
    for pattern, file in pattern_file_pairs:
        passwords += extract_by_re(file, pattern)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(passwords))

def extract_data_from_analysis_result():
    write_passwords(
        'Data/CSDN/char.txt',
        [(r'^\s*\d+\s+([^\s]+)\s+\d+\s*$', './AnalysisResults/① CSDN 密码元素与结构-top10.txt')]
    )
    write_passwords(
        'Data/CSDN/keyboard.txt',
        [(r'^[ \t]*([A-Za-z0-9]+)\s+\d+\s*$', './AnalysisResults/② CSDN 键盘密码模式分析.txt')]
    )
    write_passwords(
        'Data/CSDN/pinyin.txt',
        [(r'\d+\.\s+([a-zA-Z]+)', './AnalysisResults/④ CSDN 拼音使用统计-simplified.txt')]
    )
    write_passwords(
        'Data/CSDN/english.txt',
        [(r'\d+\.\s+([A-Za-z]+)', './AnalysisResults/⑤ CSDN 英文单词使用统计-simplified.txt')]
    )
    write_passwords(
        'Data/YAHOO/char.txt',
        [(r'^\s*\d+\s+([^\s]+)\s+\d+\s*$', './AnalysisResults/① YAHOO 密码元素与结构-top10.txt')]
    )
    write_passwords(
        'Data/YAHOO/keyboard.txt',
        [(r'^[ \t]*([A-Za-z0-9]+)\s+\d+\s*$', './AnalysisResults/② YAHOO 键盘密码模式分析.txt')]
    )
    write_passwords(
        'Data/YAHOO/pinyin.txt',
        [(r'\d+\.\s+([a-zA-Z]+)', './AnalysisResults/④ YAHOO 拼音使用统计-simplified.txt')]
    )
    write_passwords(
        'Data/YAHOO/english.txt',
        [(r'\d+\.\s+([A-Za-z]+)', './AnalysisResults/⑤ YAHOO 英文单词使用统计-simplified.txt')]
    )

if __name__ == '__main__':
    extract_data_from_analysis_result()
