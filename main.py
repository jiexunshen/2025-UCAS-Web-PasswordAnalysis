from Model.markov_model import MarkovModel
from Model.multi_layer_markov_system import MultiLayerMarkovSystem


if __name__ == "__main__":
    def load_data(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    char_data = load_data('Data/char.txt')
    keyboard_data = load_data('Data/keyboard.txt')
    pinyin_data = load_data('Data/pinyin.txt')
    english_data = load_data('Data/english.txt')

    char_model = MarkovModel(n=2, name="Character"); char_model.train(char_data)
    kb_model = MarkovModel(n=2, name="Keyboard"); kb_model.train(keyboard_data)
    pinyin_model = MarkovModel(n=2, name="Pinyin"); pinyin_model.train(pinyin_data)
    eng_model = MarkovModel(n=2, name="English"); eng_model.train(english_data)

    system = MultiLayerMarkovSystem()
    system.add_layer("char", char_model, weight=0.25)
    system.add_layer("keyboard", kb_model, weight=0.25)
    system.add_layer("pinyin", pinyin_model, weight=0.25)
    system.add_layer("english", eng_model, weight=0.25)

    candidates = system.generate_candidates(per_layer=200)
    final_passwords = system.fuse_and_rank(candidates, top_n=100)

    for pw in final_passwords:
        print(pw)
