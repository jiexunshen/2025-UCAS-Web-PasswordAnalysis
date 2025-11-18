# markov_model.py
import random
from collections import defaultdict, Counter
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

class MarkovModel:
    def __init__(self, n=2, name="UnnamedModel"):
        self.n = n
        self.model = defaultdict(Counter)
        self.start_states = Counter()
        self.name = name

    def train(self, sequences, visualize=False):
        print(f"\n[INFO] Training MarkovModel({self.name}) on {len(sequences)} samples...")
        for seq in tqdm(sequences, desc=f"Training {self.name}", ncols=80):
            seq = f"<s>{seq}</s>"
            for i in range(len(seq) - self.n):
                context = seq[i:i+self.n-1]
                next_char = seq[i+self.n-1]
                self.model[context][next_char] += 1
                if i == 0:
                    self.start_states[context] += 1

        print(f"[INFO] Training completed: {len(self.model)} contexts learned.")

        if visualize:
            self.visualize_transition_matrix(top_k=15)

    def visualize_transition_matrix(self, top_k=15):
        """绘制最常见 n-gram 转移概率热力图"""
        print(f"[VISUAL] Drawing top-{top_k} transition heatmap for {self.name}...")
        # 取出前 top_k 上下文
        contexts = list(self.model.keys())[:top_k]
        chars = sorted({c for ctx in contexts for c in self.model[ctx]})
        matrix = np.zeros((len(contexts), len(chars)))

        for i, ctx in enumerate(contexts):
            total = sum(self.model[ctx].values())
            for j, ch in enumerate(chars):
                matrix[i, j] = self.model[ctx][ch] / total if total > 0 else 0

        plt.figure(figsize=(10, 6))
        plt.imshow(matrix, cmap='YlGnBu', aspect='auto')
        plt.xticks(range(len(chars)), chars)
        plt.yticks(range(len(contexts)), contexts)
        plt.colorbar(label="Transition Probability")
        plt.title(f"Transition Heatmap - {self.name}")
        plt.tight_layout()
        plt.show()

    # def generate(self, max_len=12, top_k=1000, show_progress=True):
    #     generated = set()
    #     sorted_starts = [k for k, _ in self.start_states.most_common()]

    #     if show_progress:
    #         iterator = tqdm(total=top_k, desc=f"Generating {self.name}", ncols=80)
    #     else:
    #         iterator = None

    #     while len(generated) < top_k:
    #         context = random.choice(sorted_starts)
    #         password = context.replace("<s>", "")
    #         while len(password) < max_len:
    #             next_chars = self.model[context]
    #             if not next_chars:
    #                 break
    #             next_char = random.choices(
    #                 population=list(next_chars.keys()),
    #                 weights=list(next_chars.values())
    #             )[0]
    #             if next_char == "</s>":
    #                 break
    #             password += next_char
    #             context = password[-(self.n-1):]
    #         generated.add(password)
    #         if iterator:
    #             iterator.update(1)

    #     if iterator:
    #         iterator.close()
    #     return list(generated)

    def generate(self, max_len=12, top_k=1000, show_progress=True):
        generated = set()
        sorted_starts = [k for k, _ in self.start_states.most_common()]

        # 最大迭代次数 = top_k * 20（完全足够避免死循环）
        max_iter = top_k * 20
        current_iter = 0

        if show_progress:
            iterator = tqdm(total=top_k, desc=f"Generating {self.name}", ncols=80)
        else:
            iterator = None

        while len(generated) < top_k and current_iter < max_iter:
            current_iter += 1

            context = random.choice(sorted_starts)
            password = context.replace("<s>", "")

            for _ in range(max_len):
                next_chars = self.model.get(context, None)
                if not next_chars:
                    break
                next_char = random.choices(
                    population=list(next_chars.keys()),
                    weights=list(next_chars.values())
                )[0]
                if next_char == "</s>":
                    break
                password += next_char
                context = password[-(self.n-1):]

            if password not in generated:
                generated.add(password)
                if iterator:
                    iterator.update(1)

        if iterator:
            iterator.close()

        if len(generated) < top_k:
            print(f"[WARN] {self.name}: only generated {len(generated)} unique passwords (requested {top_k}).")

        return list(generated)


    def score(self, password):
        seq = f"<s>{password}</s>"
        score = 1.0
        for i in range(len(seq) - self.n):
            context = seq[i:i+self.n-1]
            next_char = seq[i+self.n-1]
            total = sum(self.model[context].values())
            if total == 0:
                continue
            prob = self.model[context][next_char] / total
            score *= prob
        return score
