import json
from random import random
import numpy as np
from PIL import Image
from shutil import copyfile
import os

USERS_NUM = 10000
ARTICLES_NUM = 200000
READS_NUM = 1000000

uid_region = {}
aid_lang = {}


# Beijing:60%   Hong Kong:40%
# en:20%    zh:80%
# 20 depts
# 3 roles
# 50 tags
# 0~99 credits

def gen_an_user(i):
    timeBegin = 1506328859000
    user = {}
    user["timestamp"] = str(timeBegin + i)
    user["id"] = 'u' + str(i)
    user["uid"] = str(i)
    user["name"] = "user%d" % i
    user["gender"] = "male" if random() > 0.33 else "female"
    user["email"] = "email%d" % i
    user["phone"] = "phone%d" % i
    user["dept"] = "dept%d" % int(random() * 20)
    user["grade"] = "grade%d" % int(random() * 4 + 1)
    user["language"] = "en" if random() > 0.8 else "zh"
    user["region"] = "Beijing" if random() > 0.4 else "Hong Kong"
    user["role"] = "role%d" % int(random() * 3)
    user["preferTags"] = "tags%d" % int(random() * 50)
    user["obtainedCredits"] = str(int(random() * 100))

    uid_region[user["uid"]] = user["region"]
    return "(" + \
           "\"" + user["timestamp"] + "\", " + \
           "\"" + user["id"] + "\", " + \
           "\"" + user["uid"] + "\", " + \
           "\"" + user["name"] + "\", " + \
           "\"" + user["gender"] + "\", " + \
           "\"" + user["email"] + "\", " + \
           "\"" + user["phone"] + "\", " + \
           "\"" + user["dept"] + "\", " + \
           "\"" + user["grade"] + "\", " + \
           "\"" + user["language"] + "\", " + \
           "\"" + user["region"] + "\", " + \
           "\"" + user["role"] + "\", " + \
           "\"" + user["preferTags"] + "\", " + \
           "\"" + user["obtainedCredits"] + "\")";


# science:45%   technology:55%
# en:50%    zh:50%
# 50 tags
# 2000 authors
def gen_an_article(i):
    timeBegin = 1506000000000
    article = {}
    article["id"] = 'a' + str(i)
    article["timestamp"] = str(timeBegin + i)
    article["aid"] = str(i)
    article["title"] = "title%d" % i
    article["category"] = "science" if random() > 0.55 else "technology"
    article["abstract"] = "abstract of article %d" % i
    article["articleTags"] = "tags%d" % int(random() * 50)
    article["authors"] = "author%d" % int(random() * 2000)
    article["language"] = "en" if random() > 0.5 else "zh"
    # create text
    article["text"] = "text_a" + str(i) + '.txt'
    path = './articles/article' + str(i)
    if not os.path.exists(path):
        os.makedirs(path)
    num = int(random() * 1000)
    text = ['Tsinghua'] * num
    f = open(path + "/text_a" + str(i) + '.txt', 'w+', encoding="utf8")
    f.write("".join(text))
    f.close()

    # create images
    image_num = int(random() * 5) + 1
    image_str = ""
    for j in range(image_num):
        image_str += 'image_a' + str(i) + '_' + str(j) + '.jpg,'
    article["image"] = image_str
    num_image = int(random() * 5) + 1
    for j in range(num_image):
        a = np.random.randint(0, 255, (360, 480, 3))
        img = Image.fromarray(a.astype('uint8')).convert('RGB')
        img.save(path + '/image_a' + str(i) + '_' + str(j) + '.jpg')

    # create video
    if random() < 0.05:
        # has one video
        article["video"] = "video_a" + str(i) + '_video.flv'
        if random() < 0.5:
            copyfile('./video/video1.flv', path + "/video_a" + str(i) + '_video.flv')
        else:
            copyfile('./video/video2.flv', path + "/video_a" + str(i) + '_video.flv')
    else:
        article["video"] = ""

    aid_lang[article["aid"]] = article["language"]
    return "(" + \
           "\"" + article["timestamp"] + "\", " + \
           "\"" + article["id"] + "\", " + \
           "\"" + article["aid"] + "\", " + \
           "\"" + article["title"] + "\", " + \
           "\"" + article["category"] + "\", " + \
           "\"" + article["abstract"] + "\", " + \
           "\"" + article["articleTags"] + "\", " + \
           "\"" + article["authors"] + "\", " + \
           "\"" + article["language"] + "\", " + \
           "\"" + article["text"] + "\", " + \
           "\"" + article["image"] + "\", " + \
           "\"" + article["video"] + "\")";


# user in Beijing read/agree/comment/share an english article with the probability 0.6/0.2/0.2/0.1
# user in Hong Kong read/agree/comment/share an Chinese article with the probability 0.8/0.2/0.2/0.1
p = {}
p["Beijing" + "en"] = [0.6, 0.2, 0.2, 0.1]
p["Beijing" + "zh"] = [1, 0.3, 0.3, 0.2]
p["Hong Kong" + "en"] = [1, 0.3, 0.3, 0.2]
p["Hong Kong" + "zh"] = [0.8, 0.2, 0.2, 0.1]


def gen_an_read(i):
    timeBegin = 1506332297000
    read = {}
    read["timestamp"] = str(timeBegin + i * 10000)
    read["id"] = 'r' + str(i)
    read["uid"] = str(int(random() * USERS_NUM))
    read["aid"] = str(int(random() * ARTICLES_NUM))

    region = uid_region[read["uid"]]
    lang = aid_lang[read["aid"]]
    ps = p[region + lang]

    if (random() > ps[0]):
        # read["readOrNot"] = "0";
        return gen_an_read(i)
    else:
        read["readOrNot"] = "1"
        read["readTimeLength"] = str(int(random() * 100))
        read["readSequence"] = str(int(random() * 4))
        read["agreeOrNot"] = "1" if random() < ps[1] else "0"
        read["commentOrNot"] = "1" if random() < ps[2] else "0"
        read["shareOrNot"] = "1" if random() < ps[3] else "0"
        read["commentDetail"] = "comments to this article: (" + read["uid"] + "," + read["aid"] + ")"
    return "(" + \
           "\"" + read["timestamp"] + "\", " + \
           "\"" + read["id"] + "\", " + \
           "\"" + read["uid"] + "\", " + \
           "\"" + read["aid"] + "\", " + \
           "\"" + read["readOrNot"] + "\", " + \
           "\"" + read["readTimeLength"] + "\", " + \
           "\"" + read["readSequence"] + "\", " + \
           "\"" + read["agreeOrNot"] + "\", " + \
           "\"" + read["commentOrNot"] + "\", " + \
           "\"" + read["shareOrNot"] + "\", " + \
           "\"" + read["commentDetail"] + "\")"


with open("user.sql", "w+") as f:
    f.write("DROP TABLE IF EXISTS `user`;\n")
    f.write("CREATE TABLE `user` (\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `id` char(5) DEFAULT NULL,\n" + \
            "  `uid` char(5) DEFAULT NULL,\n" + \
            "  `name` char(9) DEFAULT NULL,\n" + \
            "  `gender` char(7) DEFAULT NULL,\n" + \
            "  `email` char(10) DEFAULT NULL,\n" + \
            "  `phone` char(10) DEFAULT NULL,\n" + \
            "  `dept` char(9) DEFAULT NULL,\n" + \
            "  `grade` char(7) DEFAULT NULL,\n" + \
            "  `language` char(3) DEFAULT NULL,\n" + \
            "  `region` char(10) DEFAULT NULL,\n" + \
            "  `role` char(6) DEFAULT NULL,\n" + \
            "  `preferTags` char(7) DEFAULT NULL,\n" + \
            "  `obtainedCredits` char(3) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")
    f.write("LOCK TABLES `user` WRITE;\n")
    f.write("INSERT INTO `user` VALUES\n")
    for i in range(USERS_NUM - 1):
        f.write("  " + gen_an_user(i) + ",\n")
    f.write("  " + gen_an_user(USERS_NUM - 1) + ";\n")
    f.write("UNLOCK TABLES;\n\n\n")

with open("article.sql", "w+") as f:
    f.write("DROP TABLE IF EXISTS `article`;\n")
    f.write("CREATE TABLE `article` (\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `id` char(7) DEFAULT NULL,\n" + \
            "  `aid` char(7) DEFAULT NULL,\n" + \
            "  `title` char(15) DEFAULT NULL,\n" + \
            "  `category` char(11) DEFAULT NULL,\n" + \
            "  `abstract` char(30) DEFAULT NULL,\n" + \
            "  `articleTags` char(14) DEFAULT NULL,\n" + \
            "  `authors` char(13) DEFAULT NULL,\n" + \
            "  `language` char(3) DEFAULT NULL,\n" + \
            "  `text` char(31) DEFAULT NULL,\n" + \
            "  `image` char(32) DEFAULT NULL,\n" + \
            "  `video` char(32) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")
    f.write("LOCK TABLES `article` WRITE;\n")
    f.write("INSERT INTO `article` VALUES\n")
    for i in range(ARTICLES_NUM - 1):
        f.write("  " + gen_an_article(i) + ",\n")
    f.write("  " + gen_an_article(ARTICLES_NUM - 1) + ";\n")
    f.write("UNLOCK TABLES;\n\n\n")

with open("user_read.sql", "w+") as f:
    f.write("DROP TABLE IF EXISTS `user_read`;\n")
    f.write("CREATE TABLE `user_read` (\n" + \
            "  `timestamp` char(14) DEFAULT NULL,\n" + \
            "  `id` char(7) DEFAULT NULL,\n" + \
            "  `uid` char(5) DEFAULT NULL,\n" + \
            "  `aid` char(7) DEFAULT NULL,\n" + \
            "  `readOrNot` char(2) DEFAULT NULL,\n" + \
            "  `readTimeLength` char(3) DEFAULT NULL,\n" + \
            "  `readSequence` char(2) DEFAULT NULL,\n" + \
            "  `agreeOrNot` char(2) DEFAULT NULL,\n" + \
            "  `commentOrNot` char(2) DEFAULT NULL,\n" + \
            "  `shareOrNot` char(2) DEFAULT NULL,\n" + \
            "  `commentDetail` char(100) DEFAULT NULL\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;\n\n")

    f.write("LOCK TABLES `user_read` WRITE;\n")
    f.write("INSERT INTO `user_read` VALUES\n")
    for i in range(READS_NUM - 1):
        f.write("  " + gen_an_read(i) + ",\n")
    f.write("  " + gen_an_read(READS_NUM - 1) + ";\n")
    f.write("UNLOCK TABLES;\n\n\n")

