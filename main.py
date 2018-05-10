# 把一些警告的訊息暫時関掉
#import warnings
#warnings.filterwarnings('ignore')

# Utilities相關函式庫
import os
import numpy as np
import codecs

# 使用"結巴(jieba)來進行分析
import jieba.analyse

# 圖像處理/展現的相關函式庫
import matplotlib.pyplot as plt
from wordcloud import WordCloud

##

# 專案的根目錄路徑
ROOT_DIR = os.getcwd()

# 訓練/驗證用的資料目錄
DATASET_PATH = os.path.join(ROOT_DIR, "dataset")

# 模型資料目錄
MODEL_PATH = os.path.join(ROOT_DIR, "model")
JIEBA_DICTFILE_PATH = os.path.join(MODEL_PATH,"extra_dict", "dict.txt.big")

# 中文字型目錄
FONT_PATH = os.path.join(ROOT_DIR, "fonts")
FONT_FILE_PATH = os.path.join(FONT_PATH, "NotoSansCJKtc-Black.otf")

# 設定繁體中文字典
jieba.set_dictionary(JIEBA_DICTFILE_PATH)

##

# 將"乾杯"這首歌的關鍵字詞取出來 
# topK代表要取的前幾大的關鍵字 

song_lyrics = os.path.join(DATASET_PATH, "single_song.txt")

with open(song_lyrics, "rb") as f:
    for line in f:
        tags = jieba.analyse.extract_tags(line,topK=10, withWeight=True)
        for tag, weight in tags:
            print(tag + "," + str(int(weight * 10000)))

##

# 把每首歌的tags取出
all_songs_lyrics = os.path.join(DATASET_PATH, "test1.txt")

with open(all_songs_lyrics, "rb") as f:
    for line in f:
        tags = jieba.analyse.extract_tags(line,10)
        print(",".join(tags))

##

# 演唱會歌單出現的 33 首歌詞
all_songs_lyrics = os.path.join(DATASET_PATH, "test1.txt")

#每首歌的前10大tags的集合
all_songs_top10_tags = [] 

with open(all_songs_lyrics, "r", encoding='utf8') as f1:
    for line in f1:
        words = jieba.analyse.extract_tags(line,10) #取10個tags
        all_songs_top10_tags.extend(words) # 把tags存放起來
f1.close()

# 串接所有歌的前10大tags成一長字串
all_songs_top10_tags_text = " ".join(all_songs_top10_tags)

# 最後再找出所有歌的前15大的tags
top15_tags = jieba.analyse.extract_tags(all_songs_top10_tags_text,15) 
print(",".join(top15_tags))

##

# 設定停用字(排除常用詞、無法代表特殊意義的字詞)# 設定停用字 
stopwords = {}.fromkeys(["沒有","一個","什麼","那個"])

# 產生文字雲
wc = WordCloud(font_path="fonts/NotoSansCJKtc-Black.otf", #設置字體
               background_color="black", #背景顏色
               max_words = 2000 ,        #文字雲顯示最大詞數
               stopwords=stopwords)      #停用字詞

wc.generate(all_songs_top10_tags_text)

# 視覺化呈現
plt.imshow(wc)
plt.axis("off")
plt.figure(figsize=(10,6), dpi = 100)
plt.show()

