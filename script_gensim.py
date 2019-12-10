import gensim
import logging, multiprocessing, os, sys
from gensim.models import FastText
from gensim.models import Word2Vec
import time
import json

class SentencesIterator:
                def __init__(self, texts):
                        self.texts = texts

                def __iter__(self):
                        for sentence in self.texts:
                                sentence = sentence.split()
                                yield list(sentence)


for t in range(6, 48, 3): 
    for b in range(10, 17, 2): 
        for n in range(5, 15, 3):
            for w in range(5, 10, 2):
                execution_times = dict()
                logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
                input_texts = open(os.getcwd() + "/trainables/text8.txt", "r", encoding="utf8")
                vocabulary = SentencesIterator(input_texts)
                model_w2v_skpg = gensim.models.Word2Vec(sg=1, size=200, workers=t, batch_words=b, iter=15, negative=n, min_count=5, window = w, sample = 1e-4, alpha = 0.025)
                model_w2v_skpg.build_vocab(vocabulary)
                files = os.listdir(os.getcwd() + "/trainables/")

                for file in files:
                        if file.startswith("corpus"):
                                open_file = open(os.getcwd() + "/trainables/" + file)
                                sentences = []
                                for line_num, sentence in enumerate(open_file, 1):
                                        sentences.append(sentence.split())
                                model_w2v_skpg.build_vocab(sentences, update=True)
                                print("-- Running:", line)
                                start = time.time()
                                model_w2v_skpg.train(sentences=sentences, total_examples=line_num, epochs=15)
                                end = time.time()
                                print("\n-- Elapsed:", end - start)
                                execution_times[line] = end - start

                                with open("execution_times.csv", 'a+') as fp:
                                        fp.write("'{}',{}\n".format(line, end - start))

                with open("execution_times.json", 'w+') as fp:
                        json.dump(execution_times, fp)
                # trim memory
                model_w2v_skpg.init_sims(replace=True)

                # save model

                #save Word2Vec Skip-Gram
                model_w2v_skpg.save('word2vec_cbow_300d_48thr.vec')
                model_w2v_skpg.wv.save_word2vec_format("word2vec_cbow_300d_48thr.txt")

                input_texts.close()

