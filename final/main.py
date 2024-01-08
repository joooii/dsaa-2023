import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox
import json

def load_graph_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        first_element = data[0]

        inList = first_element['inList']
        outList = first_element['outList']
        usernameList = first_element['usernameList']

        # 각 유저 이름을 노드로 갖는 빈 그래프 생성
        graph = {username: {"in": set(), "out": set()} for username in usernameList}

        # outList를 사용하여 각 노드에서 나가는 엣지 추가
        for i, outs in enumerate(outList):
            for out in outs:
                graph[usernameList[i]]["out"].add(usernameList[out])

        # inList를 사용하여 각 노드로 들어오는 엣지 추가 (선택적)
        for i, ins in enumerate(inList):
            for in_node in ins:
                graph[usernameList[i]]["in"].add(usernameList[in_node])

        return graph


class GraphWindow(QMainWindow):
    def __init__(self, graph):
        super().__init__()

        # 그래프 데이터 로드
        self.graph = graph

        # 윈도우 설정
        self.setWindowTitle("DFS & BFS Visualization")
        self.setGeometry(100, 100, 800, 600)

        # 중앙 위젯과 레이아웃 설정
        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # 시작 및 종료 노드 선택
        self.nodes = list(self.graph.keys())
        self.start_node_selector = QComboBox()
        self.start_node_selector.addItems(self.nodes)
        self.layout.addWidget(self.start_node_selector)

        self.end_node_selector = QComboBox()
        self.end_node_selector.addItems(self.nodes)
        self.layout.addWidget(self.end_node_selector)

        # 탐색 시작 버튼
        self.dfs_button = QPushButton("DFS 시작", self)
        self.dfs_button.clicked.connect(self.start_dfs)
        self.layout.addWidget(self.dfs_button)

        self.bfs_button = QPushButton("BFS 시작", self)
        self.bfs_button.clicked.connect(self.start_bfs)
        self.layout.addWidget(self.bfs_button)

        # 결과창
        self.result_label = QLabel(central_widget)
        self.result_label.setFixedSize(500,600)
        self.layout.addWidget(self.result_label)

    def start_dfs(self):
        start_node = self.start_node_selector.currentText()
        end_node = self.end_node_selector.currentText()
        path = dfs(self.graph, start_node, end_node)
        print("DFS 최종 경로!!! :", path)


    def start_bfs(self):
        start_node = self.start_node_selector.currentText()
        end_node = self.end_node_selector.currentText()
        shortest_path = bfs(self.graph, start_node, end_node)
        print("BFS 최단 경로!!! :", shortest_path)
        


# BFS 구현
def bfs(graph, start, end):
    visited = set()
    queue = [(start, [start])]
    shortest_path = None  # 최단 경로 저장

    while queue:
        node, path = queue.pop(0)
        print("BFS 탐색 경로:", path, "\n")  # 단계별 경로 출력

        if node == end:
            if shortest_path is None:
                shortest_path = path  # 최단 경로 저장
            continue

        if node not in visited:
            visited.add(node)
            for neighbour in graph[node]["out"]:
                if neighbour not in visited:
                    queue.append((neighbour, path + [neighbour]))

    return shortest_path

# DFS 구현
def dfs(graph, start, end, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()

    visited.add(start)
    print("DFS 탐색 경로:", path, "\n")  # 현재 경로 출력


    if start == end:
        return path

    for neighbour in graph[start]["out"]:
        if neighbour not in visited:
            result = dfs(graph, neighbour, end, path + [neighbour], visited)
            if result:
                return result

    return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph = load_graph_data('congress_network_data.json')
    window = GraphWindow(graph)
    window.show()
    sys.exit(app.exec_())