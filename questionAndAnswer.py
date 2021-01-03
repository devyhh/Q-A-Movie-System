from nb_div import QuestionPrediction
from query import Query
import itchat


@itchat.msg_register("Text", isFriendChat=True)
def text_reply(msg):
    if not msg['FromUserName'] == myUserName:
        # while (i < 1000):
        #     i = i + 1
        que = msg['Text']
        name = question_model.getName(que)
        number = question_model.predict(que)  # 0:评分 1：上映时间 2：风格 3：内容 4：演员 5：演员作品
        print(name)
        print(number)
        answer = query1.search(name, number)
        print(answer)
        # 回复信息
        return answer


if __name__ == '__main__':
    itchat.auto_login()
    question_model = QuestionPrediction()
    query1 = Query()
    print("您好，欢迎使用电影问答系统！有什么可以帮助您")
    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()
    # itchat.logout
    # question_model = QuestionPrediction()
    # query1 = Query()
    # i=1
    # print("您好，欢迎使用电影问答系统！有什么可以帮助您")
    # while (i<1000):
    #     i = i+1
    #     que = input()
    #     name = question_model.getName(que)
    #     number = question_model.predict(que) # 0:评分 1：上映时间 2：风格 3：内容 4：演员 5：演员作品
    #     print(name)
    #     print(number)
    #     answer = query1.search(name,number)
    #     print(answer)
