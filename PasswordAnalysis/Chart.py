import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
def setup_chinese_font():
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        return True
    except:
        try:
            font_paths = [
                r'C:\Windows\Fonts\simhei.ttf',  # Windows 黑体
                r'C:\Windows\Fonts\msyh.ttc',  # Windows 微软雅黑
                '/System/Library/Fonts/Arial Unicode.ttf',  # macOS
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'  # Linux
            ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    font_prop = fm.FontProperties(fname=font_path)
                    plt.rcParams['font.family'] = font_prop.get_name()
                    plt.rcParams['axes.unicode_minus'] = False
                    return True
            return False
        except:
            print("警告: 无法设置中文字体，图表中的中文可能无法正常显示")
            return False
def create_statistical_charts(pinyin_counter, pinyin_case_stats,
                              word_counter, word_case_stats,
                              pinyin_combination_counter=None,
                              filename="pinyin_analysis.png"):
    font_setup_success = setup_chinese_font()
    fig = plt.figure(figsize=(20, 12))
    if font_setup_success:
        fig.suptitle('密码分析统计图表', fontsize=18, fontweight='bold')
    else:
        fig.suptitle('Password Analysis Statistics', fontsize=18, fontweight='bold')
    ax1 = plt.subplot(2, 3, 1)
    if pinyin_counter:
        top10_pinyin = pinyin_counter.most_common(10)
        pinyin_words, pinyin_counts = zip(*top10_pinyin) if top10_pinyin else ([], [])
        if pinyin_words:
            bars = ax1.bar(range(len(pinyin_words)), pinyin_counts, color='skyblue', alpha=0.7)
            if font_setup_success:
                ax1.set_title('拼音使用Top10', fontsize=14, fontweight='bold')
                ax1.set_xlabel('拼音', fontsize=12)
                ax1.set_ylabel('出现次数', fontsize=12)
            else:
                ax1.set_title('Pinyin Usage Top10', fontsize=14, fontweight='bold')
                ax1.set_xlabel('Pinyin', fontsize=12)
                ax1.set_ylabel('Frequency', fontsize=12)
            ax1.set_xticks(range(len(pinyin_words)))
            ax1.set_xticklabels(pinyin_words, rotation=45, fontsize=10)
            for bar, v in zip(bars, pinyin_counts):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height + max(pinyin_counts) * 0.05,
                         f'{v}', ha='center', va='bottom', fontsize=10)
    else:
        if font_setup_success:
            ax1.text(0.5, 0.5, '无拼音数据', ha='center', va='center', transform=ax1.transAxes, fontsize=14)
            ax1.set_title('拼音使用Top10', fontsize=14, fontweight='bold')
        else:
            ax1.text(0.5, 0.5, 'No Pinyin Data', ha='center', va='center', transform=ax1.transAxes, fontsize=14)
            ax1.set_title('Pinyin Usage Top10', fontsize=14, fontweight='bold')
    ax2 = plt.subplot(2, 3, 2)
    if sum(pinyin_case_stats.values()) > 0:
        if font_setup_success:
            case_labels = ['全小写', '全大写', '混合大小写', '首字母大写']
        else:
            case_labels = ['All Lower', 'All Upper', 'Mixed Case', 'Capitalized']

        case_values = [pinyin_case_stats.get('all_lower', 0),
                       pinyin_case_stats.get('all_upper', 0),
                       pinyin_case_stats.get('mixed_case', 0),
                       pinyin_case_stats.get('capitalized', 0)]
        filtered_labels = [label for label, val in zip(case_labels, case_values) if val > 0]
        filtered_values = [val for val in case_values if val > 0]
        filtered_indices = [i for i, val in enumerate(case_values) if val > 0]
        if filtered_values:
            colors = ['lightcoral', 'gold', 'lightgreen', 'lightskyblue']
            selected_colors = [colors[i] for i in filtered_indices]
            wedges, texts = ax2.pie(filtered_values, colors=selected_colors, startangle=90)
            if font_setup_success:
                ax2.set_title('拼音大小写分布', fontsize=14, fontweight='bold')
            else:
                ax2.set_title('Pinyin Case Distribution', fontsize=14, fontweight='bold')
            legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                          markerfacecolor=selected_colors[i], markersize=10,
                                          label=f'{filtered_labels[i]} ({filtered_values[i]}次, {filtered_values[i] / sum(filtered_values) * 100:.1f}%)')
                               for i in range(len(filtered_labels))]
            ax2.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.1),
                       ncol=2, fontsize=10)
    else:
        if font_setup_success:
            ax2.text(0.5, 0.5, '无拼音数据', ha='center', va='center', transform=ax2.transAxes, fontsize=14)
            ax2.set_title('拼音大小写分布', fontsize=14, fontweight='bold')
        else:
            ax2.text(0.5, 0.5, 'No Pinyin Data', ha='center', va='center', transform=ax2.transAxes, fontsize=14)
            ax2.set_title('Pinyin Case Distribution', fontsize=14, fontweight='bold')
    ax3 = plt.subplot(2, 3, 3)
    if pinyin_combination_counter and sum(pinyin_combination_counter.values()) > 0:
        top10_combo = pinyin_combination_counter.most_common(10)
        combos, combo_counts = zip(*top10_combo)
        bars = ax3.bar(range(len(combos)), combo_counts, color='orange', alpha=0.7)
        if font_setup_success:
            ax3.set_title('拼音组合Top10', fontsize=14, fontweight='bold')
            ax3.set_xlabel('拼音组合', fontsize=12)
            ax3.set_ylabel('出现次数', fontsize=12)
        else:
            ax3.set_title('Pinyin Combination Top10', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Pinyin Combination', fontsize=12)
            ax3.set_ylabel('Frequency', fontsize=12)
        ax3.set_xticks(range(len(combos)))
        ax3.set_xticklabels(combos, rotation=45, fontsize=10)
        for bar, v in zip(bars, combo_counts):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width() / 2., height + max(combo_counts) * 0.05,
                     f'{v}', ha='center', va='bottom', fontsize=10)
    else:
        if font_setup_success:
            ax3.text(0.5, 0.5, '无拼音组合数据', ha='center', va='center', transform=ax3.transAxes, fontsize=14)
            ax3.set_title('拼音组合Top10', fontsize=14, fontweight='bold')
        else:
            ax3.text(0.5, 0.5, 'No Pinyin Combination Data', ha='center', va='center', transform=ax3.transAxes,
                     fontsize=14)
            ax3.set_title('Pinyin Combination Top10', fontsize=14, fontweight='bold')
    ax4 = plt.subplot(2, 3, 4)
    if word_counter and sum(word_counter.values()) > 0:
        top10_words = word_counter.most_common(10)
        words, word_counts = zip(*top10_words)
        bars = ax4.bar(range(len(words)), word_counts, color='lightgreen', alpha=0.7)
        if font_setup_success:
            ax4.set_title('英文单词Top10', fontsize=14, fontweight='bold')
            ax4.set_xlabel('单词', fontsize=12)
            ax4.set_ylabel('出现次数', fontsize=12)
        else:
            ax4.set_title('English Word Top10', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Word', fontsize=12)
            ax4.set_ylabel('Frequency', fontsize=12)

        ax4.set_xticks(range(len(words)))
        ax4.set_xticklabels(words, rotation=45, fontsize=10)
        for bar, v in zip(bars, word_counts):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width() / 2., height + max(word_counts) * 0.05,
                     f'{v}', ha='center', va='bottom', fontsize=10)
    else:
        if font_setup_success:
            ax4.text(0.5, 0.5, '无英文单词数据', ha='center', va='center', transform=ax4.transAxes, fontsize=14)
            ax4.set_title('英文单词Top10', fontsize=14, fontweight='bold')
        else:
            ax4.text(0.5, 0.5, 'No English Word Data', ha='center', va='center', transform=ax4.transAxes, fontsize=14)
            ax4.set_title('English Word Top10', fontsize=14, fontweight='bold')
    ax5 = plt.subplot(2, 3, 5)
    if sum(word_case_stats.values()) > 0:
        if font_setup_success:
            word_case_labels = ['全小写', '全大写', '混合大小写', '首字母大写']
        else:
            word_case_labels = ['All Lower', 'All Upper', 'Mixed Case', 'Capitalized']
        word_case_values = [word_case_stats.get('all_lower', 0),
                            word_case_stats.get('all_upper', 0),
                            word_case_stats.get('mixed_case', 0),
                            word_case_stats.get('capitalized', 0)]
        filtered_word_labels = [label for label, val in zip(word_case_labels, word_case_values) if val > 0]
        filtered_word_values = [val for val in word_case_values if val > 0]
        filtered_word_indices = [i for i, val in enumerate(word_case_values) if val > 0]
        if filtered_word_values:
            colors = ['lightcoral', 'gold', 'lightgreen', 'lightskyblue']
            selected_word_colors = [colors[i] for i in filtered_word_indices]
            wedges, texts = ax5.pie(filtered_word_values, colors=selected_word_colors, startangle=90)
            if font_setup_success:
                ax5.set_title('英文单词大小写分布', fontsize=14, fontweight='bold')
            else:
                ax5.set_title('English Word Case Distribution', fontsize=14, fontweight='bold')
            legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                          markerfacecolor=selected_word_colors[i], markersize=10,
                                          label=f'{filtered_word_labels[i]} ({filtered_word_values[i]}次, {filtered_word_values[i] / sum(filtered_word_values) * 100:.1f}%)')
                               for i in range(len(filtered_word_labels))]
            ax5.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.1),
                       ncol=2, fontsize=10)
    else:
        if font_setup_success:
            ax5.text(0.5, 0.5, '无英文单词数据', ha='center', va='center', transform=ax5.transAxes, fontsize=14)
            ax5.set_title('英文单词大小写分布', fontsize=14, fontweight='bold')
        else:
            ax5.text(0.5, 0.5, 'No English Word Data', ha='center', va='center', transform=ax5.transAxes, fontsize=14)
            ax5.set_title('English Word Case Distribution', fontsize=14, fontweight='bold')
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')  # 不显示坐标轴
    total_pinyin = sum(pinyin_counter.values()) if pinyin_counter else 0
    total_words = sum(word_counter.values()) if word_counter else 0
    total_combinations = sum(pinyin_combination_counter.values()) if pinyin_combination_counter else 0
    unique_pinyin = len(pinyin_counter) if pinyin_counter else 0
    unique_words = len(word_counter) if word_counter else 0
    unique_combinations = len(pinyin_combination_counter) if pinyin_combination_counter else 0
    if font_setup_success:
        summary_text = f"""
数据摘要统计:
拼音使用情况:
- 总拼音出现次数: {total_pinyin:,}
- 唯一拼音数量: {unique_pinyin:,}
英文单词使用情况:
- 总单词出现次数: {total_words:,}
- 唯一单词数量: {unique_words:,}

拼音组合使用情况:
- 总组合出现次数: {total_combinations:,}
- 唯一组合数量: {unique_combinations:,}
"""
    else:
        summary_text = f"""
Data Summary:
Pinyin Usage:
- Total Pinyin Occurrences: {total_pinyin:,}
- Unique Pinyin Count: {unique_pinyin:,}
English Word Usage:
- Total Word Occurrences: {total_words:,}
- Unique Word Count: {unique_words:,}
Pinyin Combination Usage:
- Total Combination Occurrences: {total_combinations:,}
- Unique Combination Count: {unique_combinations:,}
"""
    if font_setup_success:
        ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=11,
                 verticalalignment='top')
    else:
        ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=11,
                 verticalalignment='top', fontfamily='monospace')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"统计图表已保存到 {filename}")
def create_statistical_charts_fallback(pinyin_counter, pinyin_case_stats,
                                       word_counter, word_case_stats,
                                       pinyin_combination_counter=None,
                                       filename="pinyin_analysis.png"):
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('Password Analysis Statistics', fontsize=18, fontweight='bold')
    create_statistical_charts(pinyin_counter, pinyin_case_stats,
                              word_counter, word_case_stats,
                              pinyin_combination_counter, filename)