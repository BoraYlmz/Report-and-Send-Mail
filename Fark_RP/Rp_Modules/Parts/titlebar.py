import sys
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton,QFrame,QSizePolicy,QSpacerItem
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os

class CustomTitleBar(QWidget):
    def __init__(self,bar_color:str,font_color:str,border_color:str,hover_btn:str,title:str, parent=None,):
        super().__init__(parent)
        # self.setStyleSheet(f"border-left: 1px solid {border_color};border-right: 1px solid {border_color};border-bottom: none;border-top:1px solid {border_color}")


        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)

        frame = QFrame()
        frame.setStyleSheet(f"border-left: 1px solid {border_color};border-right: none;border-bottom: none;border-top:1px solid {border_color};border-bottom-right-radius:0px;border-bottom-left-radius:0px;")
        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(0,0,0,0)
        frame_layout.setSpacing(0)
        # frame_layout.addStretch()

        osicon = QLabel()
        logo_path = os.path.join(os.getcwd(), r"Rp_Modules\icons", "ui_logo.png")
        pixmap = QPixmap(logo_path)  # Resmin yolu
        osicon.setPixmap(pixmap)
        osicon.setStyleSheet("padding-left:10px;border:0;")
    
        title_text=QLabel(title)
        title_text.setStyleSheet(f"padding-left:10px;border:0;margin:0;color:{font_color};font-weight: bold;font-family:Arial; font-size:13px")


        # Kapatma butonu
        close_button = QPushButton("X")
        close_button.setObjectName("closebtn")
        close_button.setStyleSheet(f"""QPushButton#closebtn{{
                                        color: {font_color};
                                        font-weight:bold; 
                                        border-left:1px solid {border_color};
                                        border-top:none;
                                        border-right:1px solid {border_color};
                                        border-bottom:none;border-radius:0px;
                                        border-top-right-radius:5px;
                                    }}
                                    QPushButton#closebtn:hover {{
                                        background-color:{hover_btn};
                                        color:white
                                   }}""")

        close_button.setFixedSize(35,35)
        close_button.clicked.connect(self.close_window)

        # Küçültme butonu
        minimize_button = QPushButton("_")
        minimize_button.setObjectName("minibtn")
        minimize_button.setStyleSheet(f"""QPushButton#minibtn{{
                                            color: {font_color};
                                            font-weight:bold; 
                                            border-left:1px solid {border_color};
                                            border-top:none;border-right:none;
                                            border-bottom:none;
                                            border-radius:0px
                                      }}
                                      QPushButton#minibtn:hover{{
                                            background-color:{hover_btn};
                                            color:white
                                      }}""")
        minimize_button.setFixedSize(35,35)
        minimize_button.clicked.connect(self.minimize_window)
        
        frame_layout.addWidget(osicon,0,QtCore.Qt.AlignLeft)
        frame_layout.addWidget(title_text)
        spacer = QSpacerItem(800, 35, QSizePolicy.Minimum, QSizePolicy.Minimum)
        frame_layout.addItem(spacer)
        frame_layout.addWidget(minimize_button,0,QtCore.Qt.AlignRight)
        frame_layout.addWidget(close_button)
        
        
        main_layout.addWidget(frame)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.startPos = None  # Sürükleme başlangıç pozisyonu

    def close_window(self):
        self.parent().close()

    def minimize_window(self):
        self.parent().showMinimized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPosition().toPoint()  # Sürükleme başlangıç noktası

    def mouseMoveEvent(self, event):
        if self.startPos is not None:
            # Pencereyi sürükle
            delta = event.globalPosition().toPoint() - self.startPos
            self.parent().move(self.parent().pos() + delta)  # QPoint kullanarak
            self.startPos = event.globalPosition().toPoint()  # Güncelle

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = None  # Sürükleme durduruldu
