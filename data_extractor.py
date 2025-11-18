import os
import re

def extract_by_re(file_path: str, pattern: str):
    regex = re.compile(pattern, re.MULTILINE)
    with open(file_path, "r", encoding="utf-8") as f:
        return regex.findall(f.read())

def write_passwords(file_path: str, patterns_files: list):
    passwords = []
    for pattern, file in patterns_files:
        passwords += extract_by_re(file, pattern)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(passwords))

def extract_data_from_analysis_result():
    write_passwords(
        'Data/char.txt',
        [
            (r'^\s*\d+\s+([^\s]+)\s+\d+\s*$', './AnalysisResults/① CSDN 密码元素与结构-top10.txt'),
            (r'^\s*\d+\s+([^\s]+)\s+\d+\s*$', './AnalysisResults/① YAHOO 密码元素与结构-top10.txt')
        ]
    )
    write_passwords(
        'Data/keyboard.txt',
        [
            (r'^[ \t]*([A-Za-z0-9]+)\s+\d+\s*$', './AnalysisResults/② CSDN 键盘密码模式分析.txt'),
            (r'^[ \t]*([A-Za-z0-9]+)\s+\d+\s*$', './AnalysisResults/② YAHOO 键盘密码模式分析.txt')
        ]
    )
    write_passwords(
        'Data/pinyin.txt',
        [
            (r'\d+\.\s+([a-zA-Z]+)', './AnalysisResults/④ CSDN 拼音使用统计-simplified.txt'),
            (r'\d+\.\s+([a-zA-Z]+)', './AnalysisResults/④ YAHOO 拼音使用统计-simplified.txt')
        ]
    )
    write_passwords(
        'Data/english.txt',
        [
            (r'\d+\.\s+([A-Za-z]+)', './AnalysisResults/⑤ CSDN 英文单词使用统计-simplified.txt'),
            (r'\d+\.\s+([A-Za-z]+)', './AnalysisResults/⑤ YAHOO 英文单词使用统计-simplified.txt')
        ]
    )

if __name__ == '__main__':
    extract_data_from_analysis_result()
