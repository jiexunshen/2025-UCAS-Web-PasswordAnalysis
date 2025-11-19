import re
import os

def pattern_to_regex(pattern: str):
    mapping = {"L": r"[a-z]", "U": r"[A-Z]", "D": r"[0-9]", "S": r"[^a-zA-Z0-9]", "O": r"."}
    regex = ""
    i = 0
    while i < len(pattern):
        t = pattern[i]
        j = i + 1
        num = ""
        while j < len(pattern) and pattern[j].isdigit():
            num += pattern[j]
            j += 1
        count = int(num) if num else 1
        regex += f"{mapping[t]}{{{count}}}"
        i = j
    return "^" + regex + "$"

def load_passwords(files):
    all_pw = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            all_pw.extend([line.strip() for line in f if line.strip()])
    return all_pw

def build_attack_dict_by_source(pattern_list, base_dir, output_prefix):
    password_files = [
        os.path.join(base_dir, "char.txt"),
        os.path.join(base_dir, "keyboard.txt"),
        os.path.join(base_dir, "pinyin.txt"),
        os.path.join(base_dir, "english.txt")
    ]
    passwords = load_passwords(password_files)
    seen = set()
    attack_list = []

    pattern_matched_count = 0
    markov_generated_count = 0

    for pattern in pattern_list:
        regex = re.compile(pattern_to_regex(pattern))
        for pw in passwords:
            if pw not in seen and regex.match(pw):
                seen.add(pw)
                attack_list.append(pw)
                pattern_matched_count += 1

    try:
        from Model.markov_model import MarkovModel
        from Model.multi_layer_markov_system import MultiLayerMarkovSystem

        def train_markov_model(file_path):
            data = load_passwords([file_path])
            model = MarkovModel(n=2, name=os.path.basename(file_path))
            model.train(data)
            return model

        char_model = train_markov_model(os.path.join(base_dir, "char.txt"))
        kb_model = train_markov_model(os.path.join(base_dir, "keyboard.txt"))
        pinyin_model = train_markov_model(os.path.join(base_dir, "pinyin.txt"))
        eng_model = train_markov_model(os.path.join(base_dir, "english.txt"))

        system = MultiLayerMarkovSystem()
        system.add_layer("char", char_model, weight=0.25)
        system.add_layer("keyboard", kb_model, weight=0.25)
        system.add_layer("pinyin", pinyin_model, weight=0.25)
        system.add_layer("english", eng_model, weight=0.25)

        candidates = system.generate_candidates(per_layer=200)
        final_pw = system.fuse_and_rank(candidates, top_n=100)

        for pw in final_pw:
            if pw not in seen:
                attack_list.append(pw)
                seen.add(pw)
                markov_generated_count += 1

    except Exception as e:
        print(f"[WARN] Markov model supplement failed: {e}")

    os.makedirs("Results", exist_ok=True)
    output_file = os.path.join(
        "Results",
        f"{output_prefix}_P{pattern_matched_count}_M{markov_generated_count}.txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(attack_list))

    print(f"[INFO] Attack dictionary saved: {output_file}")
    print(f"[INFO] Total passwords: {len(attack_list)} (Pattern: {pattern_matched_count}, Markov: {markov_generated_count})")


if __name__ == "__main__":
    csdn_patterns = [
        "D8","D9","L8","D11","D10","L3D6","L9","L2D6",
        "L10","D12","L3D7","L4D4","L2D7","D6","L6D3",
        "L6D4","L11","L4D6","L1D7","D6L3"
    ]

    build_attack_dict_by_source(csdn_patterns, "Data/CSDN", "CSDN")
    build_attack_dict_by_source(csdn_patterns, "Data/YAHOO", "YAHOO")
