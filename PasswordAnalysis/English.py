import re
from collections import Counter
from Constants import COMMON_ENGLISH_WORDS, COMMON_PINYIN
def extract_english_words(password):
    words = re.findall(r'[a-zA-Z]{2,}', password)
    return [word.lower() for word in words]  # 转换为小写进行统计
def analyze_word_usage(passwords):
    word_counter = Counter()
    word_case_stats = {'all_lower': 0, 'all_upper': 0, 'mixed_case': 0, 'capitalized': 0}
    for pwd in passwords:
        words = re.findall(r'[a-zA-Z]{2,}', pwd)
        for word in words:
            word_lower = word.lower()
            if (word_lower in COMMON_ENGLISH_WORDS or 3 <= len(word) <= 10) and word_lower not in COMMON_PINYIN:
                word_counter[word_lower] += 1
                # 分析原始大小写
                if word.islower():
                    word_case_stats['all_lower'] += 1
                elif word.isupper():
                    word_case_stats['all_upper'] += 1
                elif word.istitle():
                    word_case_stats['capitalized'] += 1
                else:
                    word_case_stats['mixed_case'] += 1
    return word_counter, word_case_stats