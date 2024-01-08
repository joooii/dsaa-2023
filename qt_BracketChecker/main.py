import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap

class BracketChecker(QMainWindow):
    class Stack():
        def __init__(self):
            self.items = []

        def push(self, item):
            self.items.append(item)

        def pop(self):
            return self.items.pop() if self.items else None

        def peek(self):
            return self.items[-1] if self.items else None

        def is_empty(self):
            return len(self.items) == 0
        
        def __str__(self):
            return '->'.join(self.items)


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('괄호 검사기')
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 입력창
        self.input_label = QLineEdit(self)
        self.input_label.setFixedSize(450,60)
        # 체크 버튼
        self.check_btn = QPushButton(self) 
        self.check_btn.setIcon(QIcon('./check_icon.png'))
        self.check_btn.clicked.connect(self.check_brackets)
        self.check_btn.setFixedSize(60,60)

        # 결과 창
        self.result_label = QLabel('맞는지 아닌지 확인하는 창', central_widget)
        self.result_label.setFixedSize(500,600)

        # 레이아웃 설정
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.input_label)
        top_layout.addWidget(self.check_btn)

        valid_layout = QHBoxLayout()
        valid_layout.addWidget(self.result_label)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(valid_layout)

        central_widget.setLayout(layout)



## 함수
    def check_brackets(self):
        stack = self.Stack()
        input_data = self.input_label.text().strip()

        print(f"입력한 수식: {input_data}\n")

        opening_brackets = "({["
        closing_brackets = ")}]"
        operators = "+-"
        valid_chars = "0123456789(){}[]+-*/ "
        matches = {')': '(', '}': '{', ']': '['}
        

        # 특수문자 확인
        special_chars = [char for char in input_data if char not in valid_chars]
        if special_chars:
            print("\n괄호 외의 다른 특수문자가 포함되어 있습니다.")
            print("특수문자 제외하고 괄호 검사를 시작합니다. \n")

        # 특수문자 제외
        input_data = ''.join([char for char in input_data if char in valid_chars])


        if not input_data:
            self.result_label.setText("빈칸입니다")
            print("빈칸입니다\n")
            return
        

        for char in input_data:
            if char not in opening_brackets and char not in closing_brackets and char not in operators:
                continue
            print(f"입력값 : {char}") # 숫자는 걍 넘김


            if char in opening_brackets:
                stack.push(char)
                print(f"stack 상태 : {stack}")
            
            elif char in closing_brackets:
                if stack.peek() == matches[char]:
                    stack.pop()
                    print(f"stack 상태 : {stack}")
                else:
                    print(f"stack 상태 : {stack}    # 오류: 짝이 맞지 않는 '{char}'가 있습니다.")
                    print("Invalid expression \n")
                    pixmap = QPixmap('./땡.jpg')
                    self.result_label.setPixmap(pixmap)
                    return

            elif char in operators:
                print(f"stack 상태 : {stack}    # 연산자는 무시")
                continue


        # 모든 괄호가 올바르게 닫혔는지 확인
        if stack.is_empty():
            print("EMPTY    # 모든 괄호가 올바르게 닫힘")
            print("Valid expression \n")
            pixmap = QPixmap('./정답.jpg')
            self.result_label.setPixmap(pixmap)
        else:
            print(f"# 오류: 짝이 맞지 않는 '{char}'가 있습니다.")
            print("Invalid expression \n")
            pixmap = QPixmap('./땡.jpg')
            self.result_label.setPixmap(pixmap)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    checker = BracketChecker()
    checker.show()
    sys.exit(app.exec_())
