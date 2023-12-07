from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QHBoxLayout, QPushButton, QWidget, 
                             QFileDialog, QSizePolicy, QLabel)
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt
import fitz  # PyMuPDF

class PdfViewer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setGeometry(100, 100, 600, 400)
        self.setMaximumSize(600, 850)
        self.setMinimumSize(600, 850)
        self.setWindowTitle("Pdf viewer")
        
        # Основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("QWidget {background-color: #e8e8e8;}")

        # Основной вертикальный макет
        self.main_layout = QVBoxLayout(self.central_widget)

        # Горизонтальный макет для кнопок
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Кнопка выбора файла
        self.choose_file_button = QPushButton("Выбрать файл")
        self.choose_file_button.setStyleSheet("QPushButton {background-color: white; border: 1px solid gray; border-radius: 3px; padding: 2px; font-size: 15px}")
        self.choose_file_button.clicked.connect(self.choose_file)
        
        # Кнопки навигации по файлу
        self.previous_page_btn = QPushButton("<")
        self.previous_page_btn.setStyleSheet("QPushButton {background-color: white; border: 1px solid gray; border-radius: 3px; padding: 2px 30px; font-size: 15px}")
        self.previous_page_btn.clicked.connect(self.previous_page)
        self.next_page_btn = QPushButton(">")
        self.next_page_btn.setStyleSheet("QPushButton {background-color: white; border: 1px solid gray; border-radius: 3px; padding: 2px 30px; font-size: 15px}")
        self.next_page_btn.clicked.connect(self.next_page)

        # Создаем разделитель для кнопок
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Expanding)

        # Добавляем кнопки и разделитель в макет с кнопками
        self.buttons_layout.addWidget(self.choose_file_button)
        self.buttons_layout.addWidget(self.spacer)
        self.buttons_layout.addWidget(self.previous_page_btn)
        self.buttons_layout.addWidget(self.next_page_btn)

        # Вставляем горизонтальный макет перед QLabel
        self.main_layout.insertLayout(0, self.buttons_layout)
        self.main_layout.addStretch(1)  # Растягиваем верхнюю область

        # QLabel для отображения страницы PDF
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

        # Изображение для рендера страницы PDF
        self.image = QPixmap(800, 600)
        self.image.fill(Qt.GlobalColor.white)

        # Текущая страница
        self.current_page = 0

    def choose_file(self):
        """
        Функция отвечает за открытие окна для выбора pdf файла впроводнике
        """
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            self.selected_file = file_dialog.selectedFiles()[0]
            self.current_page = 0
            self.render_pdf(self.selected_file)
            self.label.setStyleSheet("QLabel {border: 1px solid black;}")

    def render_pdf(self, pdf_file):
        """
        Функция отвечает за отображение текущей страницы pdf файла 
        """
        doc = fitz.open(pdf_file)
        if 0 <= self.current_page < doc.page_count:
            page = doc[self.current_page]
            img = page.get_pixmap()
            qt_image = QImage(img.samples, img.width, img.height, img.stride, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)

    def previous_page(self):
        """
        Функция отвечает за переключение текущей страницы pdf файла на предыдущую
        """
        if self.current_page > 0:
            self.current_page -= 1
            self.render_pdf(self.selected_file)

    def next_page(self):
        """
        Функция отвечает за переключение текущей страницы pdf файла на следующую
        """
        doc = fitz.open(self.selected_file)
        if self.current_page < doc.page_count - 1:
            self.current_page += 1
            self.render_pdf(self.selected_file)

if __name__ == "__main__":
    app = QApplication([])
    window = PdfViewer()
    if QIcon('./icon/icon.png'):
        window.setWindowIcon(QIcon('./icon/icon.ico'))
    window.show()
    app.exec()
