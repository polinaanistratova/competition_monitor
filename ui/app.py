import sys
import os
import json
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
                             QPushButton, QFileDialog, QListWidget)
from PyQt6.QtCore import Qt

API_URL = "http://127.0.0.1:8001"


class CompetitionMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-анализатор конкурентов")
        self.setGeometry(100, 100, 900, 700)
        
        tabs = QTabWidget()
        tabs.addTab(self.create_text_tab(), "Анализ текста")
        tabs.addTab(self.create_image_tab(), "Анализ изображения")
        tabs.addTab(self.create_parse_tab(), "Парсинг сайтов")
        
        self.setCentralWidget(tabs)
    
    def create_text_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Текст для анализа (описание конкурента, лендинг и т.п.):"))
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)
        
        btn = QPushButton("Анализировать")
        btn.clicked.connect(self.analyze_text)
        layout.addWidget(btn)
        
        layout.addWidget(QLabel("Результат анализа:"))
        self.text_result = QTextEdit()
        self.text_result.setReadOnly(True)
        layout.addWidget(self.text_result)
        
        widget.setLayout(layout)
        return widget
    
    def create_image_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Скриншот или изображение лендинга конкурента:"))
        btn_file = QPushButton("Выбрать файл")
        btn_file.clicked.connect(self.select_image)
        layout.addWidget(btn_file)
        self.image_path_label = QLabel("Файл не выбран")
        layout.addWidget(self.image_path_label)
        self.selected_image = None
        
        btn = QPushButton("Анализировать изображение")
        btn.clicked.connect(self.analyze_image)
        layout.addWidget(btn)
        
        layout.addWidget(QLabel("Результат анализа:"))
        self.image_result = QTextEdit()
        self.image_result.setReadOnly(True)
        layout.addWidget(self.image_result)
        
        widget.setLayout(layout)
        return widget
    
    def create_parse_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Автоматический парсинг сайтов конкурентов из config.py"))
        btn = QPushButton("Запустить парсинг (/parsedemo)")
        btn.clicked.connect(self.run_parsing)
        layout.addWidget(btn)
        
        layout.addWidget(QLabel("Результаты:"))
        self.parse_results = QListWidget()
        layout.addWidget(self.parse_results)
        
        btn_history = QPushButton("Показать историю")
        btn_history.clicked.connect(self.show_history)
        layout.addWidget(btn_history)
        
        widget.setLayout(layout)
        return widget
    
    def analyze_text(self):
        try:
            text = self.text_input.toPlainText()
            resp = requests.post(f"{API_URL}/analyzetext", data={"text": text})
            self.text_result.setText(json.dumps(resp.json(), ensure_ascii=False, indent=2))
        except Exception as e:
            self.text_result.setText(f"Ошибка: {e}")
    
    def select_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if filename:
            self.selected_image = filename
            self.image_path_label.setText(filename)
    
    def analyze_image(self):
        try:
            if not self.selected_image:
                self.image_result.setText("Ошибка: выберите файл")
                return
            with open(self.selected_image, 'rb') as f:
                files = {'file': f}
                resp = requests.post(f"{API_URL}/analyzeimage", files=files)
            self.image_result.setText(json.dumps(resp.json(), ensure_ascii=False, indent=2))
        except Exception as e:
            self.image_result.setText(f"Ошибка: {e}")
    
    def run_parsing(self):
        try:
            resp = requests.get(f"{API_URL}/parsedemo")
            data = resp.json()
            self.parse_results.clear()
            for item in data.get("results", []):
                self.parse_results.addItem(f"{item.get('url')} - {item.get('status')}")
        except Exception as e:
            self.parse_results.clear()
            self.parse_results.addItem(f"Ошибка: {e}")
    
    def show_history(self):
        try:
            resp = requests.get(f"{API_URL}/history")
            data = resp.json()
            self.parse_results.clear()
            self.parse_results.addItem(f"Всего батчей: {len(data)}")
            for batch in data[-3:]:
                self.parse_results.addItem(f"Батч от {batch.get('timestamp')}")
        except Exception as e:
            self.parse_results.clear()
            self.parse_results.addItem(f"Ошибка: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CompetitionMonitorApp()
    window.show()
    sys.exit(app.exec())
