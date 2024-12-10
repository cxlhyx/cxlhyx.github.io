from py2neo import Graph, Node, Relationship
import pandas as pd
from tqdm import trange


class KgNeo4j:
    def __init__(
        self,
        url="bolt://localhost:7687",
        username="neo4j",
        password="neo4jneo4j",
        database="neo4j",
        clear=False,
    ):
        # build connection
        self.graph = Graph(
            profile=url,
            auth=(username, password),
            name=database,
        )
        if clear:
            self.graph.delete_all()  # 清除所有数据

    # 建立实体结点
    def createNode(self, file):
        tmp = file.split(".")
        if tmp[-1] == "csv":
            Vertexes = pd.read_csv(file, encoding="gbk")
        elif tmp[-1] == "xlsx":
            Vertexes = pd.read_excel(file, sheet_name="Vertexes")
        # print(Vertexes)
        for i in trange(Vertexes.shape[0]):
            node = Node(str(Vertexes.iloc[i]["label"]))
            for j in range(1, Vertexes.shape[1]):
                node[str(Vertexes.columns[j])] = str(Vertexes.iloc[i][j])
            self.graph.create(node)

    # 建立关系边
    def createRelationship(self, file):
        tmp = file.split(".")
        if tmp[-1] == "csv":
            Edges = pd.read_csv(file, encoding="gbk")
        elif tmp[-1] == "xlsx":
            Edges = pd.read_excel(file, sheet_name="Edges")
        # print(Edges)
        for i in trange(Edges.shape[0]):
            source = (
                self.graph.nodes.match()
                .where("_.ID='{}'".format(str(int(Edges.iloc[i]["source entity ID"]))))
                .first()
            )
            target = (
                self.graph.nodes.match()
                .where("_.ID='{}'".format(str(int(Edges.iloc[i]["target entity ID"]))))
                .first()
            )
            relationship = Relationship(
                source, str(Edges.iloc[i]["relationship type"]), target
            )
            self.graph.create(relationship)

    # 建立知识图谱
    def createKG(self, *file):
        if len(file) == 1:  # excel
            self.createNode(file[0])
            self.createRelationship(file[0])
        elif len(file) == 2:  # csv
            self.createNode(file[0])
            self.createRelationship(file[1])


if __name__ == "__main__":
    kg = KgNeo4j(clear=True)
    # kg.createKG(r"data/KGdata template.xlsx")
    # kg.createKG(r"data/KGdata template Vertexes.csv", r"data/KGdata template Edges.csv")
    kg.createKG("D:\college\Project\paper1\APOS\APOS_3W2.xlsx")
