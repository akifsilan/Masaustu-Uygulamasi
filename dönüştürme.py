from PyQt5 import uic

with open("market.py","w",encoding="utf-8") as fout:
    uic.compileUi("urun_ekle.ui",fout)
