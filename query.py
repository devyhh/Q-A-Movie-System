
from py2neo import Graph,Node,Relationship


class Query():
    # 初始化数据库
    def __init__(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="123456")

        # 查找数据库
    def run(self, cql):
        result = []
        find_rela = self.graph.run(cql)
        for i in find_rela:
            result.append(i.items()[0][1])
        return result

        # 查找类别判断
    def search(self,name,number):
            if number == 0:
                cql = f"match (m:Movie)-[]->() where m.title='{name}' return m.rating"
                answer = self.run(cql)[0]
                answer = round(answer, 2)
                final_answer = name + "电影评分为" + str(answer) + "分！"
                return final_answer
            elif number == 1:
                cql = f"match(m:Movie)-[]->() where m.title='{name}' return m.releasedate"
                answer = self.run(cql)[0]
                final_answer = name + "的上映时间是" + str(answer) + "！"
                return final_answer
            elif number == 2:
                cql = f"match(m:Movie)-[r:is]->(b) where m.title='{name}' return b.name"
                answer = self.run(cql)
                answer_set = set(answer)
                answer_list = list(answer_set)
                answer = "、".join(answer_list)
                final_answer = name + "是" + str(answer) + "等类型的电影！"
                return final_answer
            elif number == 3:
                cql = f"match(m:Movie)-[]->() where m.title='{name}' return m.introduction"
                answer = self.run(cql)[0]
                final_answer = name + "主要讲述了" + str(answer) + "！"
                return final_answer
            elif number == 4:
                cql = f"match(n:Person)-[r:actedin]->(m:Movie) where m.title='{name}' return n.name"
                answer = self.run(cql)
                answer_set = set(answer)
                answer_list = list(answer_set)
                answer = "、".join(answer_list)
                final_answer =name + "由" + str(answer) + "等演员主演！"
                return final_answer
            elif number == 5:
                cql = f"match(n:Person)-[]->() where n.name='{name}' return n.biography"
                answer = self.run(cql)[0]
                final_answer = answer
                return final_answer
            elif number == 6:
                cql = f"match(n:Person)-[]->(m:Movie) where n.name='{name}' return m.title"
                answer = self.run(cql)
                answer_set = set(answer)
                answer_list = list(answer_set)
                answer = "、".join(answer_list)
                final_answer = name + "演过" + str(answer) + "等电影！"
                return final_answer




