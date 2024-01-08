import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap

class ImageNode:
    def __init__(self, image_data):
        self.image_data = image_data
        self.next_node = None
        self.prev_node = None

    def set_next(self, next_node):
        self.next_node = next_node

    def set_prev(self, prev_node):
        self.prev_node = prev_node

    def get_image(self):
        return self.image_data


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, new_node: 'ImageNode'): 
        if self.head is not None:
            cur_node = self.head
            while cur_node.next_node:
                cur_node = cur_node.next_node
            cur_node.next_node = new_node
            new_node.prev_node = cur_node
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = new_node


    def remove(self, node):
        if node.prev_node:
            node.prev_node.next_node = node.next_node
        if node.next_node:
            node.next_node.prev_node = node.prev_node
        if node == self.head:
            self.head = node.next_node
        if node == self.tail:
            self.tail = node.prev_node

        if node.next_node is not None:
            return node.next_node
        else:
            return node.prev_node


    def merge(self, other_list: 'DoublyLinkedList'):
        if other_list.head is None:
            return  # 다른 리스트가 비어 있으면 병합할 필요 X

        if self.head is None:
            self.head = other_list.head
            self.tail = other_list.tail
            return
        
        self.tail.next_node = other_list.head
        other_list.head.prev_node = self.tail
        self.tail = other_list.tail

        # 원형 연결 리스트
        self.head.prev_node = self.tail
        self.tail.next_node = self.head


# PyQt5 코드
class ImageSlider(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()

        self.dllist = DoublyLinkedList()    # 병합된 llinked list
        self.dllist1 = DoublyLinkedList()   # image1의 linked list
        self.dllist2 = DoublyLinkedList()   # image2의 linked list

        self.current_node = None
        self.current_list = self.dllist1 

    def initUI(self):
        self.setGeometry(400,400,500,600)
        self.setWindowTitle('Image Slide Show')
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget) 
        self.image_label = QLabel(central_widget)
        self.image_label.setFixedSize(350,400)


        # 상단 메뉴바
        menu = self.menuBar()
        menu_top = menu.addMenu('메뉴')
        menu_delete = QAction('사진 제거', self)
        menu_prev = QAction('이전', self)
        menu_next = QAction('다음', self)
        menu_merge = QAction('병합', self)
        menu_display = QAction('보기', self)
        
        menu_top.addAction(menu_delete)
        menu_top.addAction(menu_prev)
        menu_top.addAction(menu_next)
        menu_top.addAction(menu_merge)
        menu_top.addAction(menu_display)

        menu_delete.triggered.connect(self.delete_image)
        menu_prev.triggered.connect(self.prev_image)  
        menu_next.triggered.connect(self.next_image)
        menu_merge.triggered.connect(self.merge_linked_list)
        menu_display.triggered.connect(self.view_merged_list)


        # 하단 버튼들
        folder_btn = QPushButton('폴더', central_widget)
        folder_btn.clicked.connect(self.folder_select)
        add_btn = QPushButton('사진 추가',central_widget)
        add_btn.clicked.connect(self.add_image)
        prev_btn = QPushButton('<', central_widget)
        prev_btn.clicked.connect(self.prev_image)
        next_btn = QPushButton('>', central_widget)
        next_btn.clicked.connect(self.next_image)

        # 레이아웃 정렬
        button_layout = QHBoxLayout() # 가로
        button_layout.addWidget(folder_btn)
        button_layout.addWidget(add_btn)

        image_layout = QHBoxLayout()
        image_layout.addWidget(prev_btn)
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(next_btn)

        layout = QVBoxLayout() # 세로
        layout.addLayout(button_layout)
        layout.addLayout(image_layout)

        central_widget.setLayout(layout)


## 함수 ##
    # 폴더 선택
    def folder_select(self):
        folder_dir = 'C:/Users/3098k/OneDrive - 부경대학교/workspace/qt_linkedlist/resources'
        # folder_dir = '.../qt_linkedlist/resources'
        folder_path = QFileDialog.getExistingDirectory(self, '폴더 선택', folder_dir)

        if folder_path:
            folder_name = os.path.basename(folder_path)
            print(f"{folder_name} 폴더 내 이미지 목록")
            if folder_name:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                            print(file)


    # 이미지 추가
    def add_image(self):  
        image_dir = 'C:/Users/3098k/OneDrive - 부경대학교/workspace/qt_linkedlist/resources'
        file_name, _ = QFileDialog.getOpenFileName(self, '이미지 파일 선택', image_dir)

        if file_name:
            folder_name = os.path.basename(os.path.dirname(file_name))
            print(f"\n{folder_name} 폴더에서 이미지 추가:")

            new_node = ImageNode(file_name)

            if folder_name == 'image1': # image1 -> dllist1에 저장
                self.dllist1.append(new_node)
                self.current_list = self.dllist1

            else:                       # image2 -> dllist2에 저장
                self.dllist2.append(new_node)
                self.current_list = self.dllist2
            
            self.current_node = self.current_list.tail
            
            try:    # 올바른 파일 등록시 성공 처리 후 이미지 생성
                pixmap = QPixmap(file_name)
                if pixmap.isNull():
                    raise ValueError("Invalid image file")
                self.image_label.setPixmap(pixmap.scaled(400, 500))
                QMessageBox.information(self, "Success", "이미지 추가 성공")
                print(file_name)

            except ValueError:  # 잘못된 파일 등록시 에러 처리
                QMessageBox.warning(self, "Error", "이미지 로드 실패. 잘못된 이미지 파일입니다.")
                print("Error")
            

    # 현재 표시되고 있는 이미지 삭제
    def delete_image(self):
        if self.current_node:
            deleted_image_path = self.current_node.get_image()
            self.current_node = self.current_list.remove(self.current_node)

            # 삭제된 이미지의 이름 출력
            print(f"\n이미지 삭제: \n{deleted_image_path}")
            
            if self.current_node:
                pixmap = QPixmap(self.current_node.get_image())
                self.image_label.setPixmap(pixmap.scaled(400, 500))
            else: 
                self.image_label.clear()
                
            QMessageBox.information(self, "Success", "이미지 삭제 성공")


    # 이전 이미지 보기
    def prev_image(self):
        if not self.current_node:
            return

        if self.current_node.prev_node:
            self.current_node = self.current_node.prev_node
        else:
            self.current_node = self.current_list.tail
        pixmap = QPixmap(self.current_node.get_image())
        self.image_label.setPixmap(pixmap.scaled(400, 500))


    # 다음 이미지 보기
    def next_image(self):
        if not self.current_node:
            return
        if self.current_node.next_node:
            self.current_node = self.current_node.next_node
        else: 
            self.current_node = self.current_list.head
        pixmap = QPixmap(self.current_node.get_image())
        self.image_label.setPixmap(pixmap.scaled(400, 500))


    # 병합하기
    def merge_linked_list(self):
        self.dllist = DoublyLinkedList()
        self.dllist.merge(self.dllist1)
        self.dllist.merge(self.dllist2)

        self.current_list = self.dllist
        if self.dllist.head:
            self.current_node = self.dllist.head

        # 병합된 리스트의 이미지 목록 출력
        print("\n병합된 이미지 목록:")
        current_node = self.dllist.head
        while current_node:
            print(current_node.get_image())
            current_node = current_node.next_node 
        QMessageBox.information(self, "Success", "병합 성공")


    # 병합된 이미지 리스트 목록 보기
    def view_merged_list(self):
        current_node = self.dllist.head
        image_list = []
        
        while current_node:
            image_list.append(current_node.get_image())
            current_node = current_node.next_node
        
        if image_list:
            images_str = '\n'.join(image_list)
            QMessageBox.information(self, "병합된 이미지 목록", images_str)
            print("\n병합된 이미지 목록:\n",images_str)
        else:
            QMessageBox.information(self, "알림", "병합된 이미지가 없습니다.")
            print("\n병합된 이미지가 없습니다.")



if __name__ == '__main__':
    app = QApplication(sys.argv) 
    slider = ImageSlider()
    slider.show()
    sys.exit(app.exec_())