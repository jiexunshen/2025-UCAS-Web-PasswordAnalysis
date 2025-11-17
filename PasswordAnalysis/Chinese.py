import re
from collections import Counter, defaultdict
from pypinyin import pinyin, Style
from Constants import COMMON_PINYIN, COMMON_CHINESE_NAMES, COMMON_ENGLISH_WORDS
def is_chinese_char(c: str) -> bool:
    if not c or len(c) != 1:
        return False
    return '\u4e00' <= c <= '\u9fff'
def extract_chinese_text(text: str) -> str:
    return ''.join(c for c in text if is_chinese_char(c))
def chinese_to_pinyin(chinese_text: str):
    try:
        return [p[0] for p in pinyin(chinese_text, style=Style.NORMAL)]
    except:
        return []
VALID_SYLLABLES = set(s.lower() for s in COMMON_PINYIN if s)
COMMON_NAMES_PINYIN = set(n.lower() for n in COMMON_CHINESE_NAMES)
ALL_VALID_PINYIN = VALID_SYLLABLES.union(COMMON_NAMES_PINYIN)
COMMON_PINYIN_PATTERNS = defaultdict(set)
def init_pinyin_patterns():
    common_combinations = [
        "wangwei", "zhangwei", "liwei", "liuming", "wangfang", "zhangli",
        "lina", "wanghao", "lihao", "zhanghao", "chenwei", "liuyang",
        "zhongguo", "beijing", "shanghai", "xiexie", "nihao", "zaijian"
    ]
    for combo in common_combinations:
        if 4 <= len(combo) <= 10:
            COMMON_PINYIN_PATTERNS[len(combo)].add(combo)

init_pinyin_patterns()
def is_valid_individual_pinyin(text: str) -> bool:
    """判断单个拼音是否合法"""
    if not text:
        return False
    return text.lower() in ALL_VALID_PINYIN
def greedy_pinyin_segmentation(text: str):
    text_lower = text.lower()
    if 4 <= len(text_lower) <= 10 and text_lower in COMMON_PINYIN_PATTERNS[len(text_lower)]:
        segments = split_known_pattern(text_lower)
        if segments and len(segments) >= 2:
            return segments
    segments = []
    i, n = 0, len(text_lower)
    while i < n:
        matched = False
        for L in range(min(6, n - i), 0, -1):
            seg = text_lower[i:i + L]
            if seg in ALL_VALID_PINYIN:
                segments.append(seg)
                i += L
                matched = True
                break
        if not matched:
            flexible_segment = flexible_pinyin_segmentation(text_lower[i:])
            if flexible_segment:
                segments.extend(flexible_segment)
                return segments
            else:
                return None
    return segments if len(segments) >= 2 else None
def flexible_pinyin_segmentation(text: str):
    text_lower = text.lower()
    n = len(text_lower)
    if 4 <= n <= 10:
        for num_parts in [2, 3]:
            segments = split_into_n_parts(text_lower, num_parts)
            if segments and validate_pinyin_combination(segments):
                return segments
        dp_segments = dynamic_pinyin_segmentation(text_lower)
        if dp_segments and validate_pinyin_combination(dp_segments):
            return dp_segments
    return None
def split_into_n_parts(text: str, n: int):
    if n <= 1 or len(text) < n:
        return None
    avg_len = len(text) // n
    segments = []
    start = 0
    for i in range(n - 1):
        end = start + avg_len
        for adjust in range(-2, 3):
            test_end = min(len(text), max(start + 1, end + adjust))
            seg = text[start:test_end]
            if seg in ALL_VALID_PINYIN:
                segments.append(seg)
                start = test_end
                break
        else:
            best_seg = None
            for L in range(min(6, len(text) - start), 1, -1):
                seg = text[start:start + L]
                if seg in ALL_VALID_PINYIN:
                    best_seg = seg
                    break
            if best_seg:
                segments.append(best_seg)
                start += len(best_seg)
            else:
                return None
    last_seg = text[start:]
    if last_seg in ALL_VALID_PINYIN:
        segments.append(last_seg)
        return segments if len(segments) == n else None
    return None
def split_known_pattern(text: str):
    text_lower = text.lower()
    n = len(text_lower)
    for split_point in range(2, min(7, n - 1)):
        part1 = text_lower[:split_point]
        part2 = text_lower[split_point:]
        if part1 in ALL_VALID_PINYIN and part2 in ALL_VALID_PINYIN:
            return [part1, part2]
    if n >= 6:
        for split1 in range(2, min(7, n - 3)):
            for split2 in range(split1 + 2, min(split1 + 5, n - 1)):
                part1 = text_lower[:split1]
                part2 = text_lower[split1:split2]
                part3 = text_lower[split2:]
                if part1 in ALL_VALID_PINYIN and part2 in ALL_VALID_PINYIN and part3 in ALL_VALID_PINYIN:
                    return [part1, part2, part3]
    return None
def name_based_segmentation(text: str):
    text_lower = text.lower()
    for surname in COMMON_CHINESE_NAMES:
        surname_l = surname.lower()
        if text_lower.startswith(surname_l):
            remaining = text_lower[len(surname_l):]
            if remaining and remaining in ALL_VALID_PINYIN:
                return [surname_l, remaining]
            if len(remaining) >= 4:
                sub_segments = flexible_pinyin_segmentation(remaining)
                if sub_segments and 1 <= len(sub_segments) <= 2:
                    return [surname_l] + sub_segments
    return None
def dynamic_pinyin_segmentation(text: str):
    text_lower = text.lower()
    n = len(text_lower)
    dp = [-10 ** 9] * (n + 1)
    dp[0] = 0
    path = [None] * (n + 1)
    for i in range(1, n + 1):
        for j in range(max(0, i - 6), i):
            seg = text_lower[j:i]
            if seg in ALL_VALID_PINYIN:
                score = get_pinyin_segment_score(seg)
                total_score = dp[j] + score if j > 0 else score
                if total_score > dp[i]:
                    dp[i] = total_score
                    path[i] = j
    if dp[n] <= 0:
        return None
    res = []
    pos = n
    while pos > 0:
        prev = path[pos]
        if prev is None:
            return None
        res.append(text_lower[prev:pos])
        pos = prev
    res.reverse()
    if 2 <= len(res) <= 3:
        return res
    elif len(res) > 3:
        merged = merge_short_pinyins(res)
        if 2 <= len(merged) <= 3:
            return merged
    return res if len(res) >= 2 else None
def merge_short_pinyins(segments):
    if len(segments) <= 2:
        return segments
    merged = []
    i = 0
    while i < len(segments):
        if i < len(segments) - 1 and len(segments[i]) + len(segments[i + 1]) <= 6:
            combined = segments[i] + segments[i + 1]
            if combined in ALL_VALID_PINYIN:
                merged.append(combined)
                i += 2
                continue
        merged.append(segments[i])
        i += 1
    return merged
def get_pinyin_segment_score(seg: str):
    s = seg.lower()
    if s in COMMON_NAMES_PINYIN:
        return 6
    if s in VALID_SYLLABLES:
        length_bonus = {2: 0.5, 3: 0.7, 4: 0.9, 5: 0.6, 6: 0.4}.get(len(s), 0)
        return 5 + length_bonus
    return -10
def basic_pinyin_checks(text: str):
    text_lower = text.lower()
    if len(text_lower) < 4 or len(text_lower) > 12:
        return False
    if is_keyboard_sequence(text_lower) or is_likely_english_word(text_lower) or is_random_string(text_lower) or has_unlikely_pinyin_pattern(text_lower):
        return False
    return True
def validate_pinyin_combination(segments):
    if not segments or len(segments) < 2 or len(segments) > 3:
        return False
    valid_count = sum(1 for s in segments if s in ALL_VALID_PINYIN)
    return valid_count >= len(segments) * 0.8
def validate_segmentation(segments):
    if not segments:
        return False
    valid_count = sum(1 for s in segments if s in ALL_VALID_PINYIN)
    return valid_count >= len(segments) * 0.8
def validate_segmentation_quality(segments, original):
    if not segments or sum(len(s) for s in segments) != len(original):
        return False
    if 2 <= len(segments) <= 3:
        return validate_pinyin_combination(segments)
    return all(s in ALL_VALID_PINYIN for s in segments)
def segmentation_quality_score(segments, original):
    if not segments or sum(len(s) for s in segments) != len(original):
        return 0
    score = 0
    if len(segments) == 2:
        score += 5
    elif len(segments) == 3:
        score += 4
    elif len(segments) == 4:
        score += 2
    else:
        score += 1
    for s in segments:
        if s in COMMON_NAMES_PINYIN:
            score += 3
        elif s in VALID_SYLLABLES:
            score += 2
    total_length = sum(len(s) for s in segments)
    avg_length = total_length / len(segments)
    if 2 <= avg_length <= 4:
        score += 2
    return score
def is_valid_pinyin_combination(text: str):
    text_lower = text.lower()
    if not basic_pinyin_checks(text_lower):
        return False
    if 4 <= len(text_lower) <= 10 and text_lower in COMMON_PINYIN_PATTERNS[len(text_lower)]:
        return True
    best_segmentation = find_best_pinyin_segmentation(text_lower)
    if not best_segmentation:
        return False
    return validate_segmentation_quality(best_segmentation, text_lower)
def find_best_pinyin_segmentation(text: str):
    text_lower = text.lower()
    segmentations = []
    for seg_func in [greedy_pinyin_segmentation, name_based_segmentation, dynamic_pinyin_segmentation]:
        segmentation = seg_func(text_lower)
        if segmentation and validate_segmentation(segmentation):
            segmentations.append(segmentation)
    if not segmentations:
        return None
    best_segmentation = max(segmentations, key=lambda seg: segmentation_quality_score(seg, text_lower))
    if 2 <= len(best_segmentation) <= 3:
        return best_segmentation
    optimized = optimize_segmentation(best_segmentation, text_lower)
    return optimized if optimized else best_segmentation
def optimize_segmentation(segments, original):
    if len(segments) <= 3:
        return segments
    for i in range(len(segments) - 1):
        combined = segments[i] + segments[i + 1]
        if combined in ALL_VALID_PINYIN and len(combined) <= 6:
            new_segments = segments[:i] + [combined] + segments[i + 2:]
            if 2 <= len(new_segments) <= 3 and validate_pinyin_combination(new_segments):
                return new_segments
    return segments
def is_likely_pinyin_combination(text: str):
    text_lower = text.lower()
    if len(text_lower) < 4 or len(text_lower) > 12:
        return False
    if 4 <= len(text_lower) <= 10 and text_lower in COMMON_PINYIN_PATTERNS[len(text_lower)]:
        return True
    segmentation = find_best_pinyin_segmentation(text_lower)
    if not segmentation:
        return False
    if 2 <= len(segmentation) <= 3:
        valid_count = sum(1 for s in segmentation if s in ALL_VALID_PINYIN)
        return valid_count >= len(segmentation) * 0.7
    return validate_segmentation_quality(segmentation, text_lower)
def is_keyboard_sequence(text: str):
    t = text.lower()
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for r in rows:
        if t in r or t in r[::-1]:
            return True
    return False
def is_likely_english_word(text: str):
    t = text.lower()
    if t in COMMON_ENGLISH_WORDS:
        return True
    if len(t) >= 6 and t.endswith(("ing", "tion", "ment", "ness")):
        return True
    if re.search(r"[^aeiou]{4,}", t):
        return True
    return False
def is_random_string(text: str):
    t = text.lower()
    return bool(re.fullmatch(r"(.)\1{3,}", t))
def has_unlikely_pinyin_pattern(text: str):
    t = text.lower()
    if any(bad in t for bad in ["vv", "qq", "xx"]):
        return True
    if re.search(r'[^aeiouü]{4,}', t):
        return True
    if re.fullmatch(r'([a-z]{1,3})\1{2,}', t):
        return True
    return False
def extract_pinyin_from_text(text: str):
    result = []
    sequences = re.findall(r'[A-Za-z]{1,12}', text)
    for seq in sequences:
        seq_lower = seq.lower()
        if seq_lower in ALL_VALID_PINYIN:
            result.append(seq)
        elif is_likely_pinyin_combination(seq_lower):
            result.append(seq)
        else:
            possible_segments = split_into_pinyin_simple(seq)
            if possible_segments:
                result.extend(possible_segments)
    return result
def split_into_pinyin_simple(text: str):
    result = []
    i, n = 0, len(text)
    text_lower = text.lower()
    if is_likely_pinyin_combination(text_lower):
        segmentation = find_best_pinyin_segmentation(text_lower)
        if segmentation:
            return segmentation
    while i < n:
        found = False
        for length in range(min(6, n - i), 0, -1):
            segment = text_lower[i:i + length]
            if segment in ALL_VALID_PINYIN:
                result.append(segment)
                i += length
                found = True
                break
        if not found:
            i += 1
    return result if result else None
def analyze_pinyin_usage(passwords):
    pinyin_counter = Counter()
    pinyin_case_stats = {'all_lower': 0, 'all_upper': 0, 'mixed_case': 0, 'capitalized': 0}
    pinyin_combination_counter = Counter()
    for pwd in passwords:
        chinese_text = extract_chinese_text(pwd)
        if chinese_text:
            pinyin_list = chinese_to_pinyin(chinese_text)
            for p in pinyin_list:
                pinyin_counter[p.lower()] += 1
                pinyin_case_stats['all_lower'] += 1
        pinyin_from_text = extract_pinyin_from_text(pwd)
        for word in pinyin_from_text:
            word_lower = word.lower()
            if word.islower():
                pinyin_case_stats['all_lower'] += 1
            elif word.isupper():
                pinyin_case_stats['all_upper'] += 1
            elif word[0].isupper() and word[1:].islower():
                pinyin_case_stats['capitalized'] += 1
            else:
                pinyin_case_stats['mixed_case'] += 1
            if word_lower in ALL_VALID_PINYIN:
                pinyin_counter[word_lower] += 1
            elif is_likely_pinyin_combination(word_lower):
                pinyin_combination_counter[word] += 1
                best_segmentation = find_best_pinyin_segmentation(word_lower)
                if best_segmentation:
                    for segment in best_segmentation:
                        pinyin_counter[segment] += 1
    return pinyin_counter, pinyin_case_stats, pinyin_combination_counter
