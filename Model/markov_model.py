import random
from collections import defaultdict, Counter
from tqdm import tqdm

class MarkovModel:
    def __init__(self, n=3, name="UnnamedModel"):
        self.n = n
        self.model = defaultdict(Counter)
        self.start_states = Counter()
        self.name = name

    def train(self, sequences):
        print(f"\n[INFO] Training MarkovModel({self.name}) on {len(sequences)} samples...")
        for seq in tqdm(sequences, desc=f"Training {self.name}", ncols=80):
            seq = seq.replace("<s>", "").replace("</s>", "").strip()
            if len(seq) < self.n:
                continue
            for i in range(len(seq) - self.n + 1):
                context = seq[i:i+self.n-1]
                next_char = seq[i+self.n-1]
                self.model[context][next_char] += 1
                if i == 0:
                    self.start_states[context] += 1
        print(f"[INFO] Training completed: {len(self.model)} contexts learned.")

    def generate(self, max_len=12, top_k=1000, show_progress=True):
        generated = set()
        sorted_starts = [k for k, _ in self.start_states.most_common()]
        if not sorted_starts:
            raise ValueError(f"[ERROR] {self.name}: no start states learned, cannot generate passwords.")
        max_iter = top_k * 20
        current_iter = 0
        if show_progress:
            iterator = tqdm(total=top_k, desc=f"Generating {self.name}", ncols=80)
        else:
            iterator = None
        while len(generated) < top_k and current_iter < max_iter:
            current_iter += 1
            context = random.choice(sorted_starts)
            password = context
            for _ in range(max_len):
                next_chars = self.model.get(context, None)
                if not next_chars:
                    break
                next_char = random.choices(
                    population=list(next_chars.keys()),
                    weights=list(next_chars.values())
                )[0]
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
        seq = password
        if len(seq) < self.n:
            return 0.0
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
