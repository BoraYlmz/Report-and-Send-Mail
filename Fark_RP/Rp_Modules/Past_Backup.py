from Parts.db_connect import db_con
from plyer import notification
import pandas as pd

class backup():
    def __init__(self):
        pass
    def new_backup(self):
        try:
            PAST_SQL ="""SELECT 
                dsu.id as "Sınıf Ürün İd",
                doo.isim as "Okul Adı",
                ds.okul_id,
                ds.isim as "Sınıf Adı",
                ds.sinif_seviyesi,
                ds.kampus_adi,
                ds.mevcut,
                dd.isim as "Ders Adı",
                du.barkod,
                du.isim as "Ürün Adı",
                dm.isim as "Marka",
                CASE WHEN dkad.ust_kategori_id IS NULL THEN dkad.isim ELSE dka.isim END as Anakategori,
                dka.isim  as birincikategori ,
                dk.isim  as ikincikategori ,
                du.fiyat,
                dsu.adet,
                dsu.olusturma_tarihi,
                dsu.guncelleme_tarihi,
                dsu.urun_id as "Ürün Site İd",
                dsu.ders_id,
                dsu.sinif_id,
                dsu.min_adet,
                du.aktif,
                dsu.sinif_liste_notu,
                doz.fiyat as "Özel Fiyat",
                du.kdv_yuzde as "KDV",
                ds.sezon_id,
                du.okul_indirimi as "İndirim Uygulansın Mı?",
                du.kargo_muafiyeti,
                doo.kargo,
                du.kod as "Stok İd",
                du.kisa_aciklama,
                du.kitap_kaplama,
                dub.deger as "Tc Gerektiren Ürün",
                du.dinamik_koli_siparis_aktarma
            FROM 
                dukkan_sinifurunu dsu
                INNER JOIN dukkan_sinif ds ON ds.id = dsu.sinif_id
                INNER JOIN dukkan_okul doo ON doo.id = ds.okul_id
                INNER JOIN dukkan_urun du ON du.id = dsu.urun_id
                INNER JOIN dukkan_ders dd ON dd.id = dsu.ders_id
                LEFT JOIN dukkan_urunokulozelfiyat doz ON doz.okul_id = ds.okul_id AND doz.urun_id = dsu.urun_id
                LEFT JOIN dukkan_marka dm ON dm.id = du.marka_id
                LEFT JOIN dukkan_kategori dk ON dk.id = du.kategori_id
                LEFT JOIN dukkan_kategori dka ON dka.id = dk.ust_kategori_id 
                LEFT JOIN dukkan_urunbilgi dub ON dub.urun_id = du.id AND dub.isim = 'TC Gerektiren Ürün' and dub.deger = 'True' 
                LEFT JOIN dukkan_kategori dkad ON dkad.id = CASE WHEN dka.ust_kategori_id IS NULL THEN dk.ust_kategori_id ELSE dka.ust_kategori_id
            END
            ORDER BY 
                doo.isim, ds.isim;"""
            
            data =pd.read_sql(PAST_SQL,db_con.conn)
            writer = pd.ExcelWriter("Reports/Past_Backup.xlsx", engine ='xlsxwriter',engine_kwargs={'options':{'strings_to_urls': False}})
            data.to_excel(writer,index=False)
            writer.close()  
        except Exception as e:
            print(f'Error: {e}')
            notification.notify(
                title='Rapor HATA Bildirimi',
                message=f'Sınıf Listelerindeki Fark Raporu {e} hatasından dolayı hazırlanamadı ve ilgili kişilere mail gönderilemedi.',
                app_name='OS Oto Rapor Gönderimi',
            )