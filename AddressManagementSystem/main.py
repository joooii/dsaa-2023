from tkinter import *
import tkinter as tkinter
import tkinter.ttk
from tkinter import filedialog
import csv


## AVL 트리 코드
class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 0

def get_height(node):
    if node is None:
        return -1
    left_height = node.left.height if node.left else -1
    right_height = node.right.height if node.right else -1
    return 1 + max(left_height, right_height)

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

def right_rotate(z):
    if z is None or z.left is None:
        return z
    
    y = z.left
    T3 = y.right

    y.right = z
    z.left = T3

    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))

    return y

def left_rotate(z):
    if z is None or z.right is None:
        return z
    
    y = z.right
    T2 = y.left

    y.left = z
    z.right = T2

    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))

    return y


## 데이터 삽입, 제거

def insert(node, key, data):
    if not node:
        return AVLNode(key, data)
    elif key < node.key:
        node.left = insert(node.left, key, data)
    else:
        node.right = insert(node.right, key, data)

    node.height = 1 + max(get_height(node.left), get_height(node.right))

    balance = get_balance(node)
    if balance > 1:
        if key < node.left.key:
            return right_rotate(node)
        else:
            node.left = left_rotate(node.left)
            return right_rotate(node)
    if balance < -1:
        if key > node.right.key:
            return left_rotate(node)
        else:
            node.right = right_rotate(node.right)
            return left_rotate(node)

    return node

avl_tree_root = None


def delete(node, key):
    if not node:
        return node

    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:
        if not node.left:
            return node.right
        elif not node.right:
            return node.left

        temp = get_min_value_node(node.right)
        node.key = temp.key
        node.data = temp.data
        node.right = delete(node.right, temp.key)

    if not node:
        return node

    node.height = 1 + max(get_height(node.left), get_height(node.right))
    balance = get_balance(node)

    # AVL 트리 균형 조정
    if balance > 1:
        if key < node.left.key:
            return right_rotate(node)
        else:
            node.left = left_rotate(node.left)
            return right_rotate(node)

    if balance < -1:
        if key > node.right.key:
            return left_rotate(node)
        else:
            node.right = right_rotate(node.right)
            return left_rotate(node)

    return node


def get_min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current



# 정보 입력 (GUI)
def insert_data():
    global avl_tree_root
    name = entry1.get()
    number = entry2.get()
    email = entry3.get()

    key = name 
    data = (name, number, email)

    # 데이터를 트리뷰에 삽입
    treeview.insert('', 'end', values=(name, number, email))

    # 입력 필드 초기화
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')

    # AVL 트리에 데이터 추가
    avl_tree_root = insert(avl_tree_root, key, data)
    
    # AVL 트리 상태 출력
    print_avl_tree(avl_tree_root)


# 데이터 검색 (GUI)
def search_data():
    query = entry4.get().strip().lower()
    if query == "":
        return 
    
    for item in treeview.get_children():
        treeview.item(item, tag='')

    treeview.tag_configure('found', background='yellow')

    for item in treeview.get_children():
        if query in treeview.item(item, 'values'):
            treeview.item(item, tags=('found',))

# 데이터 삭제 (GUI)
def delete_data():
    global avl_tree_root
    selected_items = treeview.selection()
    for item in selected_items:
        item_data = treeview.item(item, 'values')
        key = item_data[0] 
        avl_tree_root = delete(avl_tree_root, key)
        treeview.delete(item)

    print_avl_tree(avl_tree_root)


def load_csv_data():
    global avl_tree_root
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                name, number, email = row
                key = name
                data = (name, number, email)
                avl_tree_root = insert(avl_tree_root, key, data) 
                treeview.insert('', 'end', values=row)

        print_avl_tree(avl_tree_root)


# AVL 트리를 순회하고 출력하는 함수
def print_avl_tree(node, level=0, prefix="Root: "):
    if node is not None:
        print(" " * (level * 4) + prefix + node.key)
        if node.left:
            print_avl_tree(node.left, level + 1, "L--- ")
        if node.right:
            print_avl_tree(node.right, level + 1, "R--- ")


# csv 파일로 저장
def save_csv_data():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for item in treeview.get_children():
                row = treeview.item(item, 'values')
                writer.writerow(row)



## GUI
window = tkinter.Tk()

menubar = Menu(window)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="파일 불러오기", command=load_csv_data)
filemenu.add_command(label="CSV 저장하기", command=save_csv_data)
menubar.add_cascade(label="File", menu=filemenu)

window.config(menu=menubar)

top_frame = Frame(window)
top_frame.pack(side=TOP, fill=X)

middle_frame = Frame(window)
middle_frame.pack(fill=X)

bottom_frame = Frame(window)
bottom_frame.pack(side=BOTTOM, fill=X)

# 입력 필드와 버튼 생성
label1 = Label(top_frame, text="이름")
entry1 = Entry(top_frame)
label2 = Label(top_frame, text="전화번호")
entry2 = Entry(top_frame)
label3 = Label(top_frame, text="이메일")
entry3 = Entry(top_frame)
inputBtn = Button(top_frame, text="입력", command=insert_data)

entry4 = Entry(middle_frame)
searchBtn = Button(middle_frame, text="검색", command=search_data)

label1.pack(side=LEFT)
entry1.pack(side=LEFT, padx=5, pady=5)
label2.pack(side=LEFT)
entry2.pack(side=LEFT, padx=5, pady=5)
label3.pack(side=LEFT)
entry3.pack(side=LEFT, padx=5, pady=5)
inputBtn.pack(side=LEFT)

entry4.pack(side=TOP, fill=X, padx=5, pady=5)
searchBtn.pack(side=TOP)

columns = ('name', 'number', 'email')
treeview = tkinter.ttk.Treeview(bottom_frame, columns=columns, show='headings')
treeview.heading('name', text='이름')
treeview.heading('number', text='전화번호')
treeview.heading('email', text='이메일')
treeview.pack(side=TOP, fill=BOTH, expand=True)

submit_button = Button(bottom_frame, text="삭제", command=delete_data)
submit_button.pack(side=RIGHT, pady=5)

window.title("Address Management System")
window.geometry("640x400+100+100")
window.resizable(True, True)
window.mainloop()