import os
import json
import re
import nltk
import pymorphy2
from collections import defaultdict

nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()
stop_words = set(stopwords.words("russian"))

DATA_DIR = "wiki_docs"
INDEX_FILE = "inverted_index.json"

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  
    tokens = word_tokenize(text)
    return [morph.parse(word)[0].normal_form for word in tokens if word not in stop_words]

def build_index():
    index = defaultdict(lambda: defaultdict(int)) 
    documents = {}

    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            tokens = preprocess_text(text)
            documents[file] = tokens 
            
            for token in tokens:
                index[token][file] += 1 


    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)

    print(f"✅ Индекс построен и сохранён в {INDEX_FILE}")

build_index()
