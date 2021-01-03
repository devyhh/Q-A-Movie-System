#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jieba
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba.posseg as pseg

jieba.load_userdict('douban_film0003.txt')


class QuestionPrediction():
    """
    问题预测: 采用NB进行多分类
    数据集：template_train.csv
    """

    def __init__(self):
        # 训练模板数据
        self.train_file = "template_train.csv"
        # 读取训练数据
        self.train_x, self.train_y = self.read_train_data(self.train_file)
        # 训练模型
        self.model = self.train_model_NB()

    # 获取训练数据
    def read_train_data(self, template_train_file):
        """
        可改写为读取一个文件
        """
        train_x = []
        train_y = []
        train_data = pd.read_csv(template_train_file, encoding="gbk")
        train_x = train_data["text"].apply(lambda x: " ".join(list(jieba.cut(str(x))))).tolist()
        train_y = train_data["label"].tolist()
        return train_x, train_y

    def train_model_NB(self):
        """
        采用NB训练模板数据，用于问题分类到某个模板
        """
        X_train, y_train = self.train_x, self.train_y
        self.tv = TfidfVectorizer()

        train_data = self.tv.fit_transform(X_train).toarray()
        clf = MultinomialNB(alpha=0.01)
        clf.fit(train_data, y_train)
        return clf

    def predict(self, question):
        """
        问题预测，返回结果为label
        """
        question = [" ".join(list(jieba.cut(question)))]
        # print("question:", question)
        test_data = self.tv.transform(question).toarray()
        y_pred = self.model.predict(test_data)[0]
        return y_pred

    def getName(self,question):
        words = pseg.cut(question)
        for w in words:
            # print(w.word, w.flag)
            if w.flag=="nm" or w.flag=="nr":
                name = w.word
        return name


