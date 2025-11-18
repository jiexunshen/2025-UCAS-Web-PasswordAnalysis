# main.py

# 示例训练数据（后续替换为你的真实分析文件读取）
from Model.markov_model import MarkovModel
from Model.multi_layer_markov_system import MultiLayerMarkovSystem


char_data = ["123456", "password", "admin", "qwerty"]
keyboard_data = ["asdfgh", "qwerty", "zxcvbn"]
pinyin_data = ["woaini", "zhangsan", "wangwu"]
english_data = ["hello", "iloveyou", "welcome"]

# 初始化模型并训练
char_model = MarkovModel(n=2, name="Character"); char_model.train(char_data, visualize=True)
kb_model = MarkovModel(n=2, name="Keyboard"); kb_model.train(keyboard_data)
pinyin_model = MarkovModel(n=2, name="Pinyin"); pinyin_model.train(pinyin_data)
eng_model = MarkovModel(n=2, name="English"); eng_model.train(english_data)

# 构建多层系统
system = MultiLayerMarkovSystem()
system.add_layer("char", char_model, weight=0.4)
system.add_layer("keyboard", kb_model, weight=0.2)
system.add_layer("pinyin", pinyin_model, weight=0.2)
system.add_layer("english", eng_model, weight=0.2)

# 生成与融合
candidates = system.generate_candidates(per_layer=200)
final_passwords = system.fuse_and_rank(candidates, top_n=50)

# 输出结果
print("\n=== Top 20 Generated Passwords ===")
for pw in final_passwords[:20]:
    print(pw)
