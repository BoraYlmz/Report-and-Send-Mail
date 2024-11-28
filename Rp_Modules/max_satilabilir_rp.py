import pandas as pd
import os.path
import pyodbc
import datetime
from openpyxl import load_workbook
from tinydb import TinyDB
from openpyxl.utils.dataframe import dataframe_to_rows
from send_mail import Send_Mail
from io import BytesIO
from plyer import notification
from Parts.db_connect import db_con
from Past_Backup import backup
from dotenv import load_dotenv
try:
    load_dotenv(dotenv_path='Parts/private_data.env')

    PAST_SQL =os.getenv('MAX_RP_SQL')
    col1 = os.getenv('MAX_IMP_COL_1')
    col2 = os.getenv('MAX_IMP_COL_2')
    table_col_1 = os.getenv('MAX_TABLE_COL_1')
    table_col_2 = os.getenv('MAX_TABLE_COL_2')
    table_col_3 = os.getenv('MAX_TABLE_COL_3')
    table_col_4 = os.getenv('MAX_TABLE_COL_4')

    sezon_id = 11
    file = os.path.join(os.getcwd(), r"Rp_Modules\Reports", "Past_Backup.xlsx")
    Rp_File_Path = os.path.join(os.getcwd(), r"Rp_Modules\Reports", "Max_Satilabilir_Rapor.xlsx")
    if os.path.isfile(file) == True:
        past_backup_data = pd.read_excel(file)
        past_backup_data = past_backup_data[past_backup_data['sezon_id'] == sezon_id]
        past_backup_data['Max_Satilabilir_Adet'] = past_backup_data[col1]*past_backup_data[col2]
        past_backup_data = past_backup_data.pivot_table(index=[table_col_1,table_col_2,table_col_3,table_col_4],values=['Max_Satilabilir_Adet'],aggfunc='sum')
        past_backup_data = past_backup_data.reset_index()
        
        new_pd =pd.read_sql(PAST_SQL,db_con.conn,index_col=None)
        new_pd['Max_Satilabilir_Adet'] = new_pd[col1]*new_pd[col2]
        new_pd = new_pd.pivot_table(index=[table_col_1,table_col_2,table_col_3,table_col_4],values=['Max_Satilabilir_Adet'],aggfunc='sum')
        new_pd = new_pd.reset_index()

        past_backup_data[table_col_1] = past_backup_data[table_col_1].astype(int)
        new_pd[table_col_1] = new_pd[table_col_1].astype(int)
        
        deleted_prd = past_backup_data[~past_backup_data[table_col_1].isin(new_pd[table_col_1])]
        added_prd = new_pd[~new_pd[table_col_1].isin(past_backup_data[table_col_1])]

        merge_pd = pd.merge(past_backup_data, new_pd, on=table_col_1, how='outer', indicator=True)
        merge_pd = merge_pd[merge_pd['_merge'] == 'both']
        merge_pd = merge_pd[(merge_pd['Max_Satilabilir_Adet_x'] != merge_pd['Max_Satilabilir_Adet_y'])]                           
        changing_data = pd.DataFrame(columns=new_pd.columns)
        for i in range(len(merge_pd)):
            item=merge_pd.iloc[i]
            changing_data = pd.concat([changing_data, past_backup_data[(past_backup_data[table_col_1] == item[table_col_1])]], ignore_index = True)
            changing_data = pd.concat([changing_data, new_pd[(new_pd[table_col_1] == item[table_col_1])]], ignore_index = True)
        writer = pd.ExcelWriter(Rp_File_Path, engine ='xlsxwriter',engine_kwargs={'options':{'strings_to_urls': False}})
        past_backup_data.to_excel(writer,index=False,sheet_name="Eski Tüm Max Satılabilir")
        new_pd.to_excel(writer,index=False,sheet_name="Güncel Tüm Max Satılabilir")
        deleted_prd.to_excel(writer,index=False,sheet_name="Listeden Çıkan Ürünler")
        changing_data.to_excel(writer,index=False,sheet_name="Adet Değişen Ürünler")
        added_prd.to_excel(writer,index=False,sheet_name="Yeni Eklenen Ürünler")
        writer.close() 

    else:
        x= backup()
        x.new_backup()

except Exception as e:
    print(f'Error: {e}')
    notification.notify(
        title='Rapor HATA Bildirimi',
        message=f'Sınıf Listelerindeki Fark Raporu {e} hatasından dolayı hazırlanamadı ve ilgili kişilere mail gönderilemedi.',
        app_name='OS Oto Rapor Gönderimi',
    )