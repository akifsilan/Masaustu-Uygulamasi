from ast import Index
import enum
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from market import *



uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()


import sqlite3
baglantı = sqlite3.connect("ürünler.db")
islem = baglantı.cursor()
baglantı.commit()

table = islem.execute("Create Table if Not Exists urun(UrunKodu int,UrunAdı text,BirimFiyatı int,StokMiktarı int,ÜrünAçıklaması text,Marka text,Kategori text)")
baglantı.commit()

ui.tbllist.setHorizontalHeaderLabels(("UrunKodu","UrunAdı","BirimFiyatı","StokMiktarı","ÜrünAçıklaması","Marka","Kategori"))

def kayit_ekle():
    UrunKodu = int(ui.lnekod.text())
    UrunAdı = ui.lnead.text()
    BirimFiyatı = int(ui.lnefiyat.text())
    StokMiktarı = int(ui.flnestok.text())
    ÜrünAçıklaması = ui.lnedesc.text()
    Marka = ui.lnemarka.text()
    Kategori = ui.cmbkategori.currentText()
    

    try:
        ekle = "insert into urun(UrunKodu,UrunAdı,BirimFiyatı,StokMiktarı,ÜrünAçıklaması,Marka,Kategori) values (?,?,?,?,?,?,?)"
        islem.execute(ekle,(UrunKodu,UrunAdı,BirimFiyatı,StokMiktarı,ÜrünAçıklaması,Marka,Kategori))
        baglantı.commit()
        ui.statusbar.showMessage("Kayıt Eklendi !",10000)
        kayit_listele()
    except:
        ui.statusbar.showMessage("Kayıt Eklenemedi",10000)
   

def kayit_listele():
    ui.tbllist.clear()
    ui.tbllist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    ui.tbllist.setHorizontalHeaderLabels(("UrunKodu","UrunAdı","BirimFiyatı","StokMiktarı","ÜrünAçıklaması","Marka","Kategori"))
    sorgu = "select * from Urun"
    islem.execute(sorgu)

    for indexSatir,kayitNumarasi in enumerate(islem):
        for IndexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tbllist.setItem(indexSatir,IndexSutun,QTableWidgetItem(str(kayitSutun)))


def kategoriye_göre_list():
    listelenecek_kategori = ui.cmblist.currentText()

    sorgu = "select * from Urun where kategori = ?"
    islem.execute(sorgu,(listelenecek_kategori,))
    ui.tbllist.clear()
    ui.tbllist.setHorizontalHeaderLabels(("UrunKodu","UrunAdı","BirimFiyatı","StokMiktarı","ÜrünAçıklaması","Marka","Kategori"))
    for indexSatir,kayitNumarasi in enumerate(islem):
        for IndexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tbllist.setItem(indexSatir,IndexSutun,QTableWidgetItem(str(kayitSutun)))    


def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere,"Silme Onayı","Silmek İstediğine Emin Misin ?")
    QMessageBox.Yes | QMessageBox.No

    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tbllist.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()

        sorgu = "delete from Urun where UrunKodu = ?"

        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglantı.commit()
            ui.statusbar.showMessage("Kayıt Silindi")
            kayit_listele()
        except:
             ui.statusbar.showMessage("Kayıt Silinemedi")

    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")




kayit_listele()


ui.btnekle.clicked.connect(kayit_ekle)
ui.btnlist.clicked.connect(kayit_listele)
ui.btnlistele.clicked.connect(kategoriye_göre_list)
ui.btnsil.clicked.connect(kayit_sil)



sys.exit(uygulama.exec_())

