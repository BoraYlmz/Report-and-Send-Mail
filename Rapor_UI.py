from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QFrame,QHBoxLayout,QLineEdit,QPushButton,QSizePolicy,QSpacerItem,QListWidget,QListWidgetItem
from PySide6.QtCore import Qt
from PySide6 import QtCore
from Rp_Modules.Parts.titlebar import CustomTitleBar
import sys
from tinydb import TinyDB
from Rp_Modules.Parts.db_connect import db_con
import os
from plyer import notification
from dotenv import load_dotenv
import ast

class PersonelMenuWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 800)
        self.WIN_COLOR= "#181818"
        self.FONT_COLOR= "white"
        self.PANEL_COLOR= "#1f1f1f"
        self.BORDER_COLOR= "#353535"
        self.OS_RED= "#a60c26"
        self.ON_HOVER_OS_RED = "#850a1e"
        self.contentpanel = None
        db_path = os.path.join(os.getcwd(), "Rp_Modules", "reports.json")
        self.db = TinyDB(db_path)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f"background-color:{self.WIN_COLOR};border-radius:10px")
        self.setAttribute(Qt.WA_TranslucentBackground)
        title_bar = CustomTitleBar(self.WIN_COLOR,self.FONT_COLOR,self.BORDER_COLOR,self.OS_RED,"Raporlayıcı Arayüzü",self)
        self.setMenuWidget(title_bar)

        central_widget = QWidget()
        central_widget.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.PANEL_COLOR};border-top-right-radius:0px;border-top-left-radius:0px")
        self.setCentralWidget(central_widget)

        self.layout = QHBoxLayout(central_widget)
        self.layout.setContentsMargins(0,0,0,0)
        
        MenuPanel = QFrame()
        MenuPanel.setFixedSize(200, self.frameGeometry().height()-60)
        MenuPanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:25px;border-bottom-left-radius:0px;border-top-left-radius:0px")

        Menu_layout = QVBoxLayout(MenuPanel)
        Menu_layout.setContentsMargins(0,0,0,0)

        spacer = QSpacerItem(1, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)  # Yatay, Dikey
        Menu_layout.addItem(spacer) 

        self.listbox_style=f"""
            QListWidget {{
                border: 1px solid {self.BORDER_COLOR};
                background-color:{self.WIN_COLOR};
                border-radius: 5px;
                color:{self.FONT_COLOR};
            }}
            QScrollBar:vertical {{
                width: 2px;                 /* Kaydırma çubuğunun genişliği */
                margin: 0px 0px 0px 0px; 
                border: 0;
                background-color:white;
            }}

            QScrollBar::handle:vertical {{
                background-color: {self.OS_RED};         /* Kaydırıcı (handle) rengi */
                min-height: 20px;            /* Kaydırıcının minimum yüksekliği */
                border: 0 ;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: none;            /* Ok işaretlerinin görünmemesi için */
            }}

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                background: none;            /* Ok işaretlerinin görünmemesi için */
            }}
        """

        self.btnstyle = f"""QPushButton{{
                                 background-color:{self.PANEL_COLOR};
                                 font-weight: bold;
                                 font-family:Arial;
                                 border: 1px solid {self.BORDER_COLOR};
                                 border-left:0;
                                 border:0;
                                 color:{self.FONT_COLOR};
                                 font-size:18px;
                                 text-align:left;}}
                                 QPushButton:hover{{
                                 background-color:{self.BORDER_COLOR};
                                 }}"""
        
        self.clicked_btnstyle = f"""QPushButton{{
                                 background-color:{self.OS_RED};
                                 font-weight: bold;
                                 font-family:Arial;
                                 border: 1px solid {self.BORDER_COLOR};
                                 border-left:0;
                                 border:0;
                                 color:{self.FONT_COLOR};
                                 font-size:18px;
                                 text-align:left;}}
                                 QPushButton:hover{{
                                 background-color:{self.ON_HOVER_OS_RED};
                                 }}"""

        self.sinif_liste_fark = QPushButton(" Liste Fark Raporu")
        self.sinif_liste_fark.setStyleSheet(self.btnstyle)
        self.sinif_liste_fark.setFixedSize(MenuPanel.width()-5,50)
        self.sinif_liste_fark.clicked.connect(self.sinif_liste_fark_click) 

        self.max_satilabilir = QPushButton(" Max Satılabilir Adet")
        self.max_satilabilir.setStyleSheet(self.btnstyle)
        self.max_satilabilir.setFixedSize(MenuPanel.width()-5,50)
        self.max_satilabilir.clicked.connect(self.max_satilabilir_adet_click) 

        self.aktif_rp_list = QPushButton(" Aktif Raporlar")
        self.aktif_rp_list.setStyleSheet(self.btnstyle)
        self.aktif_rp_list.setFixedSize(MenuPanel.width()-5,50)
        self.aktif_rp_list.clicked.connect(self.aktif_rp_list_click)
        
        Menu_layout.addWidget(self.sinif_liste_fark)
        Menu_layout.addWidget(self.max_satilabilir,0,Qt.AlignTop)
        Menu_layout.addWidget(self.aktif_rp_list,0,Qt.AlignBottom)

        spacer = QSpacerItem(1, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)  # Yatay, Dikey
        Menu_layout.addItem(spacer) 

        self.layout.addWidget(MenuPanel,0,QtCore.Qt.AlignLeft)

    def reset_btn_color(self):
        self.sinif_liste_fark.setStyleSheet(self.btnstyle)
        self.max_satilabilir.setStyleSheet(self.btnstyle)
#-------------------------------------------------------------------------------- Aktif Raporlar -------------------------------------------------------------------------------
    def aktif_rp_list_click(self):
        self.reset_btn_color()
        self.aktif_rp_list.setStyleSheet(self.clicked_btnstyle)
        if self.contentpanel is not None:
            self.contentpanel.deleteLater()

        self.contentpanel = QFrame()
        self.contentpanel.setFixedSize(self.frameGeometry().width()-205, self.frameGeometry().height()-60)
        self.contentpanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:25px;border-bottom-right-radius:0px;border-top-right-radius:0px")
        
        
        self.layout.addWidget(self.contentpanel,0,QtCore.Qt.AlignRight)
#-------------------------------------------------------------------------------- Aktif Raporlar -------------------------------------------------------------------------------
#---------------------------------------------------------------------Max Satılabilir Adet Rapor Ayarlaması  -------------------------------------------------------------------
    def max_satilabilir_adet_click(self):
        self.reset_btn_color()
        self.max_satilabilir.setStyleSheet(self.clicked_btnstyle)
        if self.contentpanel is not None:
            self.contentpanel.deleteLater()

        self.contentpanel = QFrame()
        self.contentpanel.setFixedSize(self.frameGeometry().width()-205, self.frameGeometry().height()-60)
        self.contentpanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:25px;border-bottom-right-radius:0px;border-top-right-radius:0px")
        
        self.to_fullname = QLineEdit(self.contentpanel)
        self.to_fullname.setFixedSize(200,30)
        self.to_fullname.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        self.to_fullname.setPlaceholderText("Enter To FullName..")
        self.to_fullname.move(200,20)

        self.rp_sbj = QLineEdit(self.contentpanel)
        self.rp_sbj.setFixedSize(300,30)
        self.rp_sbj.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        self.rp_sbj.setPlaceholderText("Enter Subject..")
        self.rp_sbj.move(150,60)

        self.to_mail_text = QLineEdit(self.contentpanel)
        self.to_mail_text.setFixedSize(400,30)
        self.to_mail_text.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        self.to_mail_text.setPlaceholderText("Enter To Mail..")
        self.to_mail_text.move(100,100)

        

        week_days=[(1,"Pazartesi"),(2,"Salı"),(3,"Çarşamba"),(4,"Perşembe"),(5,"Cuma"),(6,"Cumartesi"),(7,"Pazar")]
        self.Day_listbox = QListWidget(self.contentpanel)
        self.Day_listbox.setFixedSize(195,130)
        self.Day_listbox.move(100,140)
        self.Day_listbox.setStyleSheet(self.listbox_style)
        self.Day_listbox.itemDoubleClicked.connect(self.select_days)
        self.Day_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for row in week_days:
            newItem = QListWidgetItem(row[1])
            newItem.setData(Qt.UserRole,row[0])
            self.Day_listbox.addItem(newItem) 

        self.Select_Day_listbox = QListWidget(self.contentpanel)
        self.Select_Day_listbox.setFixedSize(195,130)
        self.Select_Day_listbox.move(305,140)
        self.Select_Day_listbox.setStyleSheet(self.listbox_style)
        self.Select_Day_listbox.itemDoubleClicked.connect(self.unselect_days)
        self.Select_Day_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        ktgr_list=[("Kırtasiye","Kırtasiye"),("Özel Ürünler","Özel Ürünler"),("Türkçe Kitap","Türkçe Kitap"),("Yabancı Dil","Yabancı Dil"),("","Boş Kategori")]
        self.kategori_listbox = QListWidget(self.contentpanel)
        self.kategori_listbox.setFixedSize(195,130)
        self.kategori_listbox.move(100,280)
        self.kategori_listbox.setStyleSheet(self.listbox_style)
        self.kategori_listbox.itemDoubleClicked.connect(self.select_kategori)
        self.kategori_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for row in ktgr_list:
            newItem = QListWidgetItem(row[1])
            newItem.setData(Qt.UserRole,row[0])
            self.kategori_listbox.addItem(newItem) 

        self.selected_kategori_listbox = QListWidget(self.contentpanel)
        self.selected_kategori_listbox.setFixedSize(195,130)
        self.selected_kategori_listbox.move(305,280)
        self.selected_kategori_listbox.setStyleSheet(self.listbox_style)
        self.selected_kategori_listbox.itemDoubleClicked.connect(self.unselect_kategori)
        self.selected_kategori_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.descript = QLineEdit(self.contentpanel)
        self.descript.setFixedSize(300,30)
        self.descript.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        self.descript.setPlaceholderText("Special explanation for you")
        self.descript.move(100,420)

        self.create_btn = QPushButton(self.contentpanel)
        self.create_btn.setFixedSize(95,30)
        self.create_btn.setStyleSheet(f"""QPushButton{{
                                 background-color:{self.OS_RED};
                                 font-weight: bold;
                                 font-family:Arial;
                                 border-radius: 5px;
                                 border: 1px solid {self.BORDER_COLOR};
                                 color:{self.FONT_COLOR};
                                 font-size:11px;}}
                                 QPushButton:hover{{
                                 background-color:{self.ON_HOVER_OS_RED};
                                 }}""")
        self.create_btn.setText("Rapor Ekle")
        self.create_btn.move(405,420)
        self.create_btn.clicked.connect(self.create_max_satilabilir_rp)


        self.layout.addWidget(self.contentpanel,0,QtCore.Qt.AlignRight)
    
    def create_max_satilabilir_rp(self):
        if (self.to_fullname.text().count(" ") == len(self.to_fullname.text())) or (self.rp_sbj.text().count(" ") == len(self.rp_sbj.text()))or (self.to_mail_text.text().count(" ") > 0):
            print("hata")
        else:
            table_object = self.db.table('max_satilabilir')
            sql_kategori = []
            sql_days = []

            if self.Select_Day_listbox.count() != 0:
                for day in range(self.Select_Day_listbox.count()):
                    sql_days.append(int(self.Select_Day_listbox.item(day).data(Qt.UserRole)))
            else:
               for day in range(self.Day_listbox.count()):
                    sql_days.append(int(self.Day_listbox.item(day).data(Qt.UserRole))) 
            
            if self.selected_kategori_listbox.count() != 0:
                for ktgr in range(self.selected_kategori_listbox.count()):
                    sql_kategori.append(self.selected_kategori_listbox.item(ktgr).data(Qt.UserRole))
            else:
               for ktgr in range(self.kategori_listbox.count()):
                    sql_kategori.append(self.kategori_listbox.item(ktgr).data(Qt.UserRole))
            
            table_object.insert({
            'Full_Name': self.to_fullname.text(),
            'Subject': self.rp_sbj.text(),
            'Mail': self.to_mail_text.text(),
            'Desc': self.descript.text(),
            'kategori':sql_kategori,
            'rp_send_days': sql_days
            })
            notification.notify(
                title='Rapor Zamanlama Bildirimi',
                message=f'{self.to_fullname.text()} adlı kişiye {self.rp_sbj.text()} konulu mail otomatik rapor gönderim listesine eklenmiştir.',
                app_name='OS Oto Rapor Gönderimi',
            )
            self.to_fullname.setText("")
            self.rp_sbj.setText("")
            self.to_mail_text.setText("")
            self.descript.setText("")
            for i in range(self.selected_kategori_listbox.count()):
                item = self.selected_kategori_listbox.item(i)
                newItem = QListWidgetItem(item.text())
                newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
                self.kategori_listbox.addItem(newItem)

            self.selected_kategori_listbox.clear()          

            for i in range(self.Select_Day_listbox.count()):
                item = self.Select_Day_listbox.item(i)
                newItem = QListWidgetItem(item.text())
                newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
                self.Day_listbox.addItem(newItem)

            self.Select_Day_listbox.clear() 
            
#---------------------------------------------------------------------Max Satılabilir Adet Rapor Ayarlaması  -------------------------------------------------------------------

#---------------------------------------------------------------------Sınıf Listelerindeki Fark Rapor Ayarlaması ---------------------------------------------------------------
    def sinif_liste_fark_click(self):
        self.reset_btn_color()
        load_dotenv(dotenv_path='Rp_Modules/Parts/private_data.env')
        self.sinif_liste_fark.setStyleSheet(self.clicked_btnstyle)
        if self.contentpanel is not None:
            self.contentpanel.deleteLater()

        self.contentpanel = QFrame()
        self.contentpanel.setFixedSize(self.frameGeometry().width()-205, self.frameGeometry().height()-60)
        self.contentpanel.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius:25px;border-bottom-right-radius:0px;border-top-right-radius:0px")

        self.to_fullname = QLineEdit(self.contentpanel)
        self.to_fullname.setFixedSize(200,30)
        self.to_fullname.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        self.to_fullname.setPlaceholderText("Enter To FullName..")
        self.to_fullname.move(200,20)

        self.rp_sbj = QLineEdit(self.contentpanel)
        self.rp_sbj.setFixedSize(300,30)
        self.rp_sbj.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        self.rp_sbj.setPlaceholderText("Enter Subject..")
        self.rp_sbj.move(150,60)

        self.to_mail_text = QLineEdit(self.contentpanel)
        self.to_mail_text.setFixedSize(400,30)
        self.to_mail_text.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        self.to_mail_text.setPlaceholderText("Enter To Mail..")
        self.to_mail_text.move(100,100)

        self.school_listbox = QListWidget(self.contentpanel)
        self.school_listbox.setFixedSize(195,250)
        self.school_listbox.move(100,140)
        self.school_listbox.setStyleSheet(self.listbox_style)
        self.school_listbox.itemDoubleClicked.connect(self.select_school)
        self.school_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        cursor = db_con.conn.cursor()
        cursor.execute(os.getenv('UI_SQL_1'))
        for row in cursor.fetchall():
            newItem = QListWidgetItem(row[1])
            newItem.setData(Qt.UserRole,int(row[0]))
            self.school_listbox.addItem(newItem)    
        
        self.selected_school_listbox = QListWidget(self.contentpanel)
        self.selected_school_listbox.setFixedSize(195,250)
        self.selected_school_listbox.move(305,140)
        self.selected_school_listbox.setStyleSheet(self.listbox_style)
        self.selected_school_listbox.itemDoubleClicked.connect(self.unselect_school)
        self.selected_school_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        
        sql_col_name = os.getenv('SQL_COL_NAME')
        sql_col_name = ast.literal_eval(sql_col_name)
        
        self.sql_col_listbox = QListWidget(self.contentpanel)
        self.sql_col_listbox.setFixedSize(195,125)
        self.sql_col_listbox.move(100,400)
        self.sql_col_listbox.setStyleSheet(self.listbox_style)
        self.sql_col_listbox.itemDoubleClicked.connect(self.select_sql_cols)
        self.sql_col_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for row in sql_col_name:
            newItem = QListWidgetItem(row[1])
            newItem.setData(Qt.UserRole,row[0])
            self.sql_col_listbox.addItem(newItem)  

        self.select_sql_col_listbox = QListWidget(self.contentpanel)
        self.select_sql_col_listbox.setFixedSize(195,125)
        self.select_sql_col_listbox.move(305,400)
        self.select_sql_col_listbox.setStyleSheet(self.listbox_style)
        self.select_sql_col_listbox.itemDoubleClicked.connect(self.unselect_sql_cols)
        self.select_sql_col_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        week_days=[(1,"Pazartesi"),(2,"Salı"),(3,"Çarşamba"),(4,"Perşembe"),(5,"Cuma"),(6,"Cumartesi"),(7,"Pazar")]
        self.Day_listbox = QListWidget(self.contentpanel)
        self.Day_listbox.setFixedSize(195,130)
        self.Day_listbox.move(100,535)
        self.Day_listbox.setStyleSheet(self.listbox_style)
        self.Day_listbox.itemDoubleClicked.connect(self.select_days)
        self.Day_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for row in week_days:
            newItem = QListWidgetItem(row[1])
            newItem.setData(Qt.UserRole,row[0])
            self.Day_listbox.addItem(newItem) 

        self.Select_Day_listbox = QListWidget(self.contentpanel)
        self.Select_Day_listbox.setFixedSize(195,130)
        self.Select_Day_listbox.move(305,535)
        self.Select_Day_listbox.setStyleSheet(self.listbox_style)
        self.Select_Day_listbox.itemDoubleClicked.connect(self.unselect_days)
        self.Select_Day_listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.descript = QLineEdit(self.contentpanel)
        self.descript.setFixedSize(300,30)
        self.descript.setStyleSheet(f"border: 1px solid {self.BORDER_COLOR};background-color:{self.WIN_COLOR};border-radius: 5px;color:{self.FONT_COLOR};")
        self.descript.setPlaceholderText("Special explanation for you")
        self.descript.move(100,675)

        self.create_btn = QPushButton(self.contentpanel)
        self.create_btn.setFixedSize(95,30)
        self.create_btn.setStyleSheet(f"""QPushButton{{
                                 background-color:{self.OS_RED};
                                 font-weight: bold;
                                 font-family:Arial;
                                 border-radius: 5px;
                                 border: 1px solid {self.BORDER_COLOR};
                                 color:{self.FONT_COLOR};
                                 font-size:11px;}}
                                 QPushButton:hover{{
                                 background-color:{self.ON_HOVER_OS_RED};
                                 }}""")
        self.create_btn.setText("Rapor Programla")
        self.create_btn.move(405,675)
        self.create_btn.clicked.connect(self.create_fark_rp)

        self.layout.addWidget(self.contentpanel,0,QtCore.Qt.AlignRight)
    
    def create_fark_rp(self):
        if (self.to_fullname.text().count(" ") == len(self.to_fullname.text())) or (self.rp_sbj.text().count(" ") == len(self.rp_sbj.text()))or (self.to_mail_text.text().count(" ") > 0):
            print("hata")
        else:
            table_object = self.db.table('sinif_liste_fark')
            sql_school_id=[]
            sql_col_index=[]
            sql_days=[]
            if self.selected_school_listbox.count() != 0:
                for school in range(self.selected_school_listbox.count()):
                    sql_school_id.append(int(self.selected_school_listbox.item(school).data(Qt.UserRole)))
            else:
               for school in range(self.school_listbox.count()):
                    sql_school_id.append(int(self.school_listbox.item(school).data(Qt.UserRole))) 

            if self.select_sql_col_listbox.count() != 0:
                for col in range(self.select_sql_col_listbox.count()):
                    sql_col_index.append(int(self.select_sql_col_listbox.item(col).data(Qt.UserRole)))
            else:
               for col in range(self.sql_col_listbox.count()):
                    sql_col_index.append(int(self.sql_col_listbox.item(col).data(Qt.UserRole))) 

            if self.Select_Day_listbox.count() != 0:
                for day in range(self.Select_Day_listbox.count()):
                    sql_days.append(int(self.Select_Day_listbox.item(day).data(Qt.UserRole)))
            else:
               for day in range(self.Day_listbox.count()):
                    sql_days.append(int(self.Day_listbox.item(day).data(Qt.UserRole))) 
            table_object.insert({
            'Full_Name': self.to_fullname.text(),
            'Subject': self.rp_sbj.text(),
            'Mail': self.to_mail_text.text(),
            'Desc': self.descript.text(),
            'school_filter': sql_school_id,
            'col_filter': sql_col_index,
            'rp_send_days': sql_days
            })
            notification.notify(
                title='Rapor Zamanlama Bildirimi',
                message=f'{self.to_fullname.text()} adlı kişiye {self.rp_sbj.text()} konulu mail otomatik rapor gönderim listesine eklenmiştir.',
                app_name='OS Oto Rapor Gönderimi',
            )
            self.to_fullname.setText("")
            self.rp_sbj.setText("")
            self.to_mail_text.setText("")
            self.descript.setText("")
            for i in range(self.selected_school_listbox.count()):
                item = self.selected_school_listbox.item(i)
                newItem = QListWidgetItem(item.text())
                newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
                self.school_listbox.addItem(newItem)

            self.selected_school_listbox.clear() 

            for i in range(self.select_sql_col_listbox.count()):
                item = self.select_sql_col_listbox.item(i)
                newItem = QListWidgetItem(item.text())
                newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
                self.sql_col_listbox.addItem(newItem)

            self.select_sql_col_listbox.clear()          

            for i in range(self.Select_Day_listbox.count()):
                item = self.Select_Day_listbox.item(i)
                newItem = QListWidgetItem(item.text())
                newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
                self.Day_listbox.addItem(newItem)

            self.Select_Day_listbox.clear() 

    def select_school(self,item):
        listitems = self.school_listbox.selectedItems()
        newItem = QListWidgetItem(item.text())
        newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
        self.selected_school_listbox.addItem(newItem)

        for listitem in listitems:
            if item.data(Qt.UserRole) == listitem.data(Qt.UserRole):
                self.school_listbox.takeItem(self.school_listbox.row(listitem))
    
    def unselect_school(self,item):
        listitems = self.selected_school_listbox.selectedItems()
        newItem = QListWidgetItem(item.text())
        newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
        self.school_listbox.addItem(newItem)

        for listitem in listitems:
            if item.data(Qt.UserRole) == listitem.data(Qt.UserRole):
                self.selected_school_listbox.takeItem(self.selected_school_listbox.row(listitem))

    def select_sql_cols(self,item):
        listitems = self.sql_col_listbox.selectedItems()
        newItem = QListWidgetItem(item.text())
        newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
        self.select_sql_col_listbox.addItem(newItem)

        for listitem in listitems:
            if item.data(Qt.UserRole) == listitem.data(Qt.UserRole):
                self.sql_col_listbox.takeItem(self.sql_col_listbox.row(listitem))
    
    def unselect_sql_cols(self,item):
        listitems = self.select_sql_col_listbox.selectedItems()
        newItem = QListWidgetItem(item.text())
        newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
        self.sql_col_listbox.addItem(newItem)

        for listitem in listitems:
            if item.data(Qt.UserRole) == listitem.data(Qt.UserRole):
                self.select_sql_col_listbox.takeItem(self.select_sql_col_listbox.row(listitem))
#---------------------------------------------------------------------Sınıf Listelerindeki Fark Rapor Ayarlaması ---------------------------------------------------------------

#---------------------------------------------------------------------Tüm Raporlarda Kullanılan Fonksiyonlar     ---------------------------------------------------------------
    def select_days(self,item):
        listitems = self.Day_listbox.selectedItems()
        newItem = QListWidgetItem(item.text())
        newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
        self.Select_Day_listbox.addItem(newItem)

        for listitem in listitems:
            if item.data(Qt.UserRole) == listitem.data(Qt.UserRole):
                self.Day_listbox.takeItem(self.Day_listbox.row(listitem))

    def unselect_days(self,item):
        listitems = self.Select_Day_listbox.selectedItems()
        newItem = QListWidgetItem(item.text())
        newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
        self.Day_listbox.addItem(newItem)

        for listitem in listitems:
            if item.data(Qt.UserRole) == listitem.data(Qt.UserRole):
                self.Select_Day_listbox.takeItem(self.Select_Day_listbox.row(listitem))

    def select_kategori(self,item):
        listitems = self.kategori_listbox.selectedItems()
        print(len(self.kategori_listbox))
        newItem = QListWidgetItem(item.text())
        newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
        self.selected_kategori_listbox.addItem(newItem)

        for listitem in listitems:
            if item.data(Qt.UserRole) == listitem.data(Qt.UserRole):
                self.kategori_listbox.takeItem(self.kategori_listbox.row(listitem))
    
    def unselect_kategori(self,item):
        listitems = self.selected_kategori_listbox.selectedItems()
        newItem = QListWidgetItem(item.text())
        newItem.setData(Qt.UserRole,item.data(Qt.UserRole))
        self.kategori_listbox.addItem(newItem)

        for listitem in listitems:
            if item.data(Qt.UserRole) == listitem.data(Qt.UserRole):
                self.selected_kategori_listbox.takeItem(self.selected_kategori_listbox.row(listitem))
#---------------------------------------------------------------------Tüm Raporlarda Kullanılan Fonksiyonlar     ---------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonelMenuWin()
    window.show()
    sys.exit(app.exec())