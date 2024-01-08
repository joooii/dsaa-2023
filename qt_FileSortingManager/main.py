import sys
import os
import random
import string
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QFileDialog


class FileSorterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.file_list=[]


    def initUI(self):
        self.setGeometry(400,400,500,600)
        self.setWindowTitle('File Sorting Manager')

        # 폴더명 라벨
        self.folderLabel = QLabel('선택된 폴더: 없음')
        
        # 폴더 선택 버튼
        self.folderButton = QPushButton('폴더 선택')
        self.folderButton.clicked.connect(self.folder_select)

        # 정렬 알고리즘 선택 버튼
        bubbleSort = QPushButton('버블 정렬', self)
        bubbleSort.clicked.connect(self.bubble_sort)

        selectSort = QPushButton('선택 정렬', self)
        selectSort.clicked.connect(self.selection_sort)

        insertSort = QPushButton('삽입 정렬', self)
        insertSort.clicked.connect(self.insertion_sort)

        mergeSort = QPushButton('머지 정렬', self)
        mergeSort.clicked.connect(self.merge_sort)

        quickSort = QPushButton('퀵 정렬', self)
        quickSort.clicked.connect(self.quick_sort)

        allSort = QPushButton('전체 선택', self)
        allSort.clicked.connect(self.all_sort)

        # 정렬 기준 선택 드롭다운 메뉴
        self.sortCriteriaCombo = QComboBox()
        self.sortCriteriaCombo.addItem("파일 이름")
        self.sortCriteriaCombo.addItem("파일 크기")
        self.sortCriteriaCombo.addItem("생성 날짜")

        # 오름차순/내림차순 선택 드롭다운 메뉴
        self.sortOrderCombo = QComboBox()
        self.sortOrderCombo.addItem("오름차순")
        self.sortOrderCombo.addItem("내림차순")

        # 상태 창
        self.statusLabel = QLabel('Status')


        # 레이아웃 설정
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.folderLabel)
        topLayout.addWidget(self.folderButton)

        # 레이아웃에 정렬 옵션 추가
        sortOptionsLayout = QHBoxLayout()
        sortOptionsLayout.addWidget(QLabel("정렬 기준:"))
        sortOptionsLayout.addWidget(self.sortCriteriaCombo)
        sortOptionsLayout.addWidget(QLabel("정렬 순서:"))
        sortOptionsLayout.addWidget(self.sortOrderCombo)

        sortLayout = QHBoxLayout()
        sortLayout.addWidget(bubbleSort)
        sortLayout.addWidget(selectSort)
        sortLayout.addWidget(insertSort)
        sortLayout.addWidget(mergeSort)
        sortLayout.addWidget(quickSort)
        sortLayout.addWidget(allSort)


        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.statusLabel)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(sortOptionsLayout)
        mainLayout.addLayout(sortLayout)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)


## 함수
    def bubble_sort(self):  # 버블정렬
        if not self.file_list:
            print("정렬할 파일 목록이 없습니다.")
            return

        total_count = 0
        start_time = time.time()

        # 선택한 정렬 기준, 순서 가져옴
        sort_criteria = self.sortCriteriaCombo.currentText()
        sort_order = self.sortOrderCombo.currentText()

        # 정렬 기준에 따라 인덱스 설정
        criteria_index = {'파일 이름': 0, '파일 크기': 1, '생성 날짜': 2}[sort_criteria]


        n = len(self.file_list)
        for i in range(n):
            for j in range(0, n-i-1):
                if (sort_order == "오름차순" and self.file_list[j][criteria_index] > self.file_list[j+1][criteria_index]) or \
                   (sort_order == "내림차순" and self.file_list[j][criteria_index] < self.file_list[j+1][criteria_index]):
                    self.file_list[j], self.file_list[j+1] = self.file_list[j+1], self.file_list[j]

            print(f"{i+1}단계: ", self.file_list,"\n")
            total_count += 1

        print("\n버블 정렬 결과:")
        for file, size, creation_date in self.file_list:
            print(f"파일명: {file}, 크기: {size} 바이트, 생성 날짜: {time.ctime(creation_date)}")
        print('------------------------------------------------------------------------\n')
        end_time = time.time()
        total_time = end_time - start_time
        self.update_status(f'버블 정렬 완료 (총 시간: {total_time:.2f}초)')
        print(f"토탈 횟수: {total_count}")
        print(f"토탈 시간: {total_time}\n")



    def selection_sort(self):  # 선택정렬
        if not self.file_list:
            print("정렬할 파일 목록이 없습니다.")
            return

        total_count = 0
        start_time = time.time()

        sort_criteria = self.sortCriteriaCombo.currentText()
        sort_order = self.sortOrderCombo.currentText()
        criteria_index = {'파일 이름': 0, '파일 크기': 1, '생성 날짜': 2}[sort_criteria]

        n = len(self.file_list)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if (sort_order == "오름차순" and self.file_list[min_idx][criteria_index] > self.file_list[j][criteria_index]) or \
                   (sort_order == "내림차순" and self.file_list[min_idx][criteria_index] < self.file_list[j][criteria_index]):
                    min_idx = j
                    self.file_list[i], self.file_list[min_idx] = self.file_list[min_idx], self.file_list[i]

            print(f"{i+1}단계: ", self.file_list,"\n")
            total_count += 1

        print("\n선택 정렬 결과:")
        for file, size, creation_date in self.file_list:
            print(f"파일명: {file}, 크기: {size} 바이트, 생성 날짜: {time.ctime(creation_date)}")
        print('------------------------------------------------------------------------\n')
        end_time = time.time()
        total_time = end_time - start_time
        self.update_status(f'선택 정렬 완료 (총 시간: {total_time:.2f}초)')
        print(f"토탈 횟수: {total_count}")
        print(f"토탈 시간: {total_time}\n")



    def insertion_sort(self):   # 삽입정렬
        if not self.file_list:
            print("정렬할 목록이 없습니다.")
            return

        total_count = 0
        start_time = time.time()

        sort_criteria = self.sortCriteriaCombo.currentText()
        sort_order = self.sortOrderCombo.currentText()
        criteria_index = {'파일 이름': 0, '파일 크기': 1, '생성 날짜': 2}[sort_criteria]

        n = len(self.file_list)
        for i in range(1, n):
            key = self.file_list[i]
            j = i-1

            while j >= 0 and ((sort_order == "오름차순" and key[criteria_index] < self.file_list[j][criteria_index]) or \
                            (sort_order == "내림차순" and key[criteria_index] > self.file_list[j][criteria_index])):
                self.file_list[j+1] = self.file_list[j]
                j -= 1

            self.file_list[j + 1] = key
            print(f"{i}단계: ", self.file_list,"\n")
            total_count += 1

        print("\n삽입 정렬 결과:")
        for file, size, creation_date in self.file_list:
            print(f"파일명: {file}, 크기: {size} 바이트, 생성 날짜: {time.ctime(creation_date)}")
        print('------------------------------------------------------------------------\n')
        end_time = time.time()
        total_time = end_time - start_time
        self.update_status(f'삽입 정렬 완료 (총 시간: {total_time:.2f}초)')
        print(f"토탈 횟수: {total_count}")
        print(f"토탈 시간: {total_time}\n")



    def merge_sort(self):   # 병합정렬
        if not self.file_list:
            print("정렬할 목록이 없습니다.")
            return

        total_count = 0
        start_time = time.time()

        sort_criteria = self.sortCriteriaCombo.currentText()
        sort_order = self.sortOrderCombo.currentText()
        criteria_index = {'파일 이름': 0, '파일 크기': 1, '생성 날짜': 2}[sort_criteria]

        def sort_and_merge(file_list, sort_order, criteria_index, depth):
            if len(file_list) <= 1:
                return file_list, 0

            mid = len(file_list) // 2
            left, left_count = sort_and_merge(file_list[:mid], sort_order, criteria_index, depth + 1)
            right, right_count = sort_and_merge(file_list[mid:], sort_order, criteria_index, depth + 1)

            merged = []
            i = j = 0
            merge_count = 0

            while i < len(left) and j < len(right):
                if (sort_order == "오름차순" and left[i][criteria_index] < right[j][criteria_index]) or \
                (sort_order == "내림차순" and left[i][criteria_index] > right[j][criteria_index]):
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
                merge_count += 1

            while i < len(left):
                merged.append(left[i])
                i += 1
                merge_count += 1

            while j < len(right):
                merged.append(right[j])
                j += 1
                merge_count += 1

            print(f"단계 {depth}: {merged} \n")
            return merged, merge_count + left_count + right_count

        self.file_list, total_count = sort_and_merge(self.file_list, sort_order, criteria_index, 0)

        print("\n병합 정렬 결과:")
        for file, size, creation_date in self.file_list:
            print(f"파일명: {file}, 크기: {size} 바이트, 생성 날짜: {time.ctime(creation_date)}")
        print('------------------------------------------------------------------------\n')
        end_time = time.time()
        total_time = end_time - start_time
        self.update_status(f'병합 정렬 완료 (총 시간: {total_time:.2f}초)')
        print(f"토탈 횟수: {total_count}")
        print(f"토탈 시간: {total_time}\n")



    def quick_sort(self):  # 퀵 정렬 실행
        if not self.file_list:
            print("정렬할 파일 목록이 없습니다.")
            return
        
        total_count = 0
        start_time = time.time()

        sort_criteria = self.sortCriteriaCombo.currentText()
        sort_order = self.sortOrderCombo.currentText()
        criteria_index = {'파일 이름': 0, '파일 크기': 1, '생성 날짜': 2}[sort_criteria]

        def partition(arr, low, high):
            i = (low - 1)
            pivot = arr[high][criteria_index]
            print(f"\npivot : {pivot}")
            print(arr[low:high])

            for j in range(low, high):
                if (sort_order == "오름차순" and arr[j][criteria_index] <= pivot) or \
                (sort_order == "내림차순" and arr[j][criteria_index] >= pivot):
                    
                    i = i+1
                    arr[i], arr[j] = arr[j], arr[i]
                    print("swap ->", arr)
                else:
                    print("no swap ->", arr)

            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            print("--->", arr)
            return i + 1

        def quickSort(arr, low, high):
            if len(arr) == 1:
                return arr
            
            if low < high:
                pi = partition(arr, low, high)

                print(f"low: {low}, mid: {pi}")
                quickSort(arr, low, pi - 1)
                print(f"mid: {pi}, high: {high}")
                quickSort(arr, pi + 1, high)

        quickSort(self.file_list, 0, len(self.file_list) - 1)

        print("\n퀵 정렬 결과:")
        for file, size, creation_date in self.file_list:
            print(f"파일명: {file}, 크기: {size} 바이트, 생성 날짜: {time.ctime(creation_date)}")
        print('------------------------------------------------------------------------\n')
        end_time = time.time()
        total_time = end_time - start_time
        self.update_status(f'퀵 정렬 완료 (총 시간: {total_time:.2f}초)')
        print(f"토탈 횟수: {total_count}")
        print(f"토탈 시간: {total_time}\n")



    def all_sort(self):
        if not self.file_list:

            print("정렬할 파일 목록이 없습니다.")
            return

        original_file_list = self.file_list.copy()
        
        print("All Sort 시작\n")

        print("버블 정렬 실행")
        self.file_list = original_file_list.copy()
        self.bubble_sort()

        print("선택 정렬 실행")
        self.file_list = original_file_list.copy()
        self.selection_sort()

        print("삽입 정렬 실행")
        self.file_list = original_file_list.copy()
        self.insertion_sort()

        print("병합 정렬 실행")
        self.file_list = original_file_list.copy()
        self.merge_sort()

        print("퀵 정렬 실행")
        self.file_list = original_file_list.copy()
        self.quick_sort()

        print("모든 정렬 완료\n")



    def folder_select(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folderLabel.setText(f'선택된 폴더: {folder_path}')
            print(f"'{folder_path}' 폴더 선택 \n")
            self.file_list = self.get_file_list(folder_path)

        else:
            self.create_random_files(100)
            self.folderLabel.setText('선택된 폴더: 없음')
            print(f"선택된 폴더 없음")


    def get_file_list(self, folder_path):
        file_list = []
        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path):
                creation_time = os.path.getctime(full_path)
                size = os.path.getsize(full_path)
                file_list.append((f, size, creation_time))
        return file_list


    def create_random_files(self, num_files):   # 랜덤 파일 생성
        current_path = os.getcwd()
        for _ in range(num_files):
            filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.txt'
            file_path = os.path.join(current_path, filename)
            with open(file_path, 'w') as file:
                file.write("랜덤 파일")

    def update_status(self, message):
        self.statusLabel.setText(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileSorterApp()
    ex.show()
    sys.exit(app.exec_())