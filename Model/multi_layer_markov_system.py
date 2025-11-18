# multi_layer_markov.py
from collections import Counter
from tqdm import tqdm

class MultiLayerMarkovSystem:
    def __init__(self):
        self.layers = {}
        self.weights = {}

    def add_layer(self, name, model, weight):
        self.layers[name] = model
        self.weights[name] = weight
        print(f"[INFO] Added layer '{name}' (weight={weight})")

    def generate_candidates(self, per_layer=300):
        all_candidates = {}
        print("\n[INFO] Generating candidates for each layer...")
        for name, model in self.layers.items():
            print(f"  → {name} ({per_layer} samples)")
            all_candidates[name] = model.generate(top_k=per_layer)
        return all_candidates

    def fuse_and_rank(self, candidates, top_n=500):
        print(f"\n[FUSION] Fusing results from {len(self.layers)} layers...")
        fused_scores = Counter()
        total_candidates = sum(len(v) for v in candidates.values())

        for layer_name, pw_list in tqdm(candidates.items(), desc="Scoring fusion", ncols=80):
            model = self.layers[layer_name]
            w = self.weights[layer_name]
            for pw in pw_list:
                fused_scores[pw] += w * model.score(pw)

        ranked = [pw for pw, _ in fused_scores.most_common(top_n)]
        print(f"[INFO] Fusion complete. Top-{top_n} passwords selected.")
        return ranked
