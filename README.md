# **UCAS-PasswordAnalysis — 使用说明文档**

本项目用于从真实泄露的密码集合中分析结构特征，并结合模式匹配 + 多层马尔科夫模型生成高质量攻击字典。整个流程包含数据抽取、模式过滤、Markov 生成及最终字典融合。

## 项目功能概述

本工具能够完成以下任务：

- 从CSDN/YAHOO分析结果文件中按类别（元素结构、键盘模式、拼音密码、英文密码）整理数据

- 根据密码结构模式（如：D8, L3D6, L2D7 等）搜索真实密码

- 使用多层马尔科夫模型（字符层、键盘层、拼音层、英文层）补充可能存在的密码

- 生成攻击词典，格式为：

```
`数据源_P{模式匹配数量}_M{马尔科夫数量}.txt`
```

## 文件结构

```
`├── AnalysisResults/        # 原始分析结果`
`├── Data/                   # 提取后的分类密码`
`│   ├── CSDN/`
`│   │   ├── char.txt`
`│   │   ├── keyboard.txt`
`│   │   ├── pinyin.txt`
`│   │   ├── english.txt`
`│   ├── YAHOO/`
`│       ├── char.txt`
`│       ├── keyboard.txt`
`│       ├── pinyin.txt`
`│       ├── english.txt`
`│`
`├── Results/           # 最终生成的攻击字典文件`
`│   ├── attack_dict_CSDN_Pxxxx_Mxxxx.txt`
`│   ├── attack_dict_YAHOO_Pxxxx_Mxxxx.txt`
`│`
`├── Model/`
`│   ├── markov_model.py`
`│   ├── multi_layer_markov_system.py`
`│`
`├── data_extractor.py       # 数据抽取脚本`
`├── main.py                 # 构建攻击字典主程序`
`└── README.md`
```

## 使用教程

### Step 1：清洗与抽取数据


运行 data_extractor.py 解析原始分析结果文件，通过正则表达式自动提取出密码，完成后，得到如下结果：

```
Data/
 ├─ CSDN/char.txt
 ├─ CSDN/keyboard.txt
 ├─ ...
 ├─ YAHOO/char.txt
 ├─ YAHOO/keyboard.txt
 └─ ...
```

### Step 2：生成攻击字典


运行 main.py 

1. 基于模式分析筛选真实密码

系统根据密码结构模式，如：D8, L3D6, L9, L2D7, D6L3 ... 从数据源中筛选符合模式的所有密码。

2. 启动多层马尔科夫模型进行补充生成

模型包含四层：Character Layer（字符序列）、Keyboard Layer（键盘邻接序列）、Pinyin Layer（拼音结构）、English Layer（英文单词结构），每层独立建模并生成候选密码，随后多层融合加权排名，补充模式分析未覆盖的潜在密码。

3. 生成字典文件

输出文件位于 Results/ 目录。

