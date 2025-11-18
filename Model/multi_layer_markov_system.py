from collections import defaultdict

class MultiLayerMarkovSystem:
    def __init__(self):
        self.layers = []

    def add_layer(self, name, model, weight=0.25):
        self.layers.append({"name": name, "model": model, "weight": weight})

    def generate_candidates(self, per_layer=200, max_len=12):
        all_candidates = {}
        for layer in self.layers:
            model = layer["model"]
            candidates = model.generate(max_len=max_len, top_k=per_layer, show_progress=True)
            all_candidates[layer["name"]] = candidates
        return all_candidates

    def fuse_and_rank(self, all_candidates, top_n=50):
        scores = defaultdict(float)
        for layer in self.layers:
            name = layer["name"]
            weight = layer["weight"]
            model = layer["model"]
            for pw in all_candidates.get(name, []):
                scores[pw] += model.score(pw) * weight
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [pw for pw, _ in ranked[:top_n]]
