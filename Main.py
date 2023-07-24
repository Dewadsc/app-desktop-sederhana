
import sqlite3
import sys, os, random, requests, sqlite3, qrcode
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QPushButton, QLabel
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from pytube import YouTube

db = sqlite3.connect('dewabuana.db')
dbcursor = db.cursor()

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        loadUi('start.ui',self)
        self.btn_mulai.clicked.connect(self.HalamanLogin)

    def sudahAdadihalaman(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Halaman Yang Sama")
        self.msg.setText("Anda sudah berada dihalaman yang dimaksud")
        self.msg.exec_()

    def showHidePassword1(self):
        if self.btn_show_hide_password1.isChecked():
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)

    def showHidePassword2(self):
        if self.btn_show_hide_password2.isChecked():
            self.lineEdit_confirm_pass.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_confirm_pass.setEchoMode(QtWidgets.QLineEdit.Password)

    def dataKosong(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Data Kosong")
        self.msg.setText("Tidak boleh ada data yang kosong, silahkan anda lengkapi lagi")
        self.msg.exec_()

    def HalamanLogin(self):
        loadUi('login.ui',self)
        self.btn_show_hide_password1.setCheckable(True)
        self.btn_show_hide_password1.clicked.connect(self.showHidePassword1)
        self.btn_registrasi.clicked.connect(self.HalamanRegistrasi)
        self.btn_lupapass.clicked.connect(self.HalamanLupaPassword)
        self.btn_login.clicked.connect(self.jalankanlogin)

    def jalankanlogin(self):
        try:
            email = self.lineEdit_email.text()
            password = self.lineEdit_password.text()

            if email == "":
                self.dataKosong()
            elif password == "":
                self.dataKosong()
            else:
                dbcursor.execute("select email, password from dataAkun where email like '"+email+"' and password like '"+password+"'")
                db.commit()
                result = dbcursor.fetchone()
                if result == None:
                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Gagal Log In")
                    self.msg.setText("Log In gagal, karna data tidak ditemukan dalam database kami")
                    self.msg.exec_()

                    self.lineEdit_email.setText("")
                    self.lineEdit_password.setText("")
                else:
                    dbcursor.execute("select * from dataakun where email = '"+email+"'")
                    db.commit()
                    result = dbcursor.fetchall()
                    if result:
                        for data in result:
                            self.iduser = str(data[0])
                            self.usernameuser = data[1]
                            self.emailuser = data[2]
                            self.passworduser = data[3]
                            self.jeniskelaminuser = data[4]
                            self.hobiuser = data[5]
                            self.nowauser = data[6]
                            self.HalamanBeranda()
        except Exception as e:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Terdapat Eror")
            self.msg.setText("Silahkan klik show detail untuk melihat eror tersebut")
            self.msg.setDetailedText(e.__str__())
            self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

    def HalamanRegistrasi(self):
        loadUi('registrasi.ui',self)
        self.btn_kembali.clicked.connect(self.HalamanLogin)
        self.btn_registrasi.clicked.connect(self.registrasinow)

        self.btn_show_hide_password1.setCheckable(True)
        self.btn_show_hide_password2.setCheckable(True)
        self.btn_show_hide_password1.clicked.connect(self.showHidePassword1)
        self.btn_show_hide_password2.clicked.connect(self.showHidePassword2)

        self.rb_lakilaki.toggled.connect(self.rblakiregistrasi)
        self.rb_perempuan.toggled.connect(self.rbperempuanregistrasi)

    def rblakiregistrasi(self):
        self.jeniskelamin = "laki laki"
    
    def rbperempuanregistrasi(self):
        self.jeniskelamin = "perempuan"

    def registrasinow(self):
        try:
            username = self.lineEdit_username.text()
            email = self.lineEdit_email.text()

            dbcursor.execute("select * from dataakun where username = '"+username+"'")
            db.commit()
            cekusername = dbcursor.fetchone()

            if cekusername == None:
                dbcursor.execute("select * from dataakun where email = '"+email+"'")
                db.commit()
                cekemail = dbcursor.fetchone()
                
                if cekemail == None:
                    iduser = str(random.randint(1, 9999))
                    password = self.lineEdit_password.text()
                    confirmpass = self.lineEdit_confirm_pass.text()
                    hobi = self.lineEdit_hobi.text()
                    nowa = self.lineEdit_nowa.text()

                    if username == "":
                        self.dataKosong()
                    elif email == "":
                        self.dataKosong()
                    elif password == "":
                        self.dataKosong()
                    elif confirmpass == "":
                        self.dataKosong()
                    elif self.jeniskelamin == "":
                        self.dataKosong()
                    elif hobi == "":
                        self.dataKosong()
                    elif nowa == "":
                        self.dataKosong()
                    elif password == confirmpass:
                        sql = "insert into dataAkun (iduser,username,email,password,jeniskelamin,hobi,nowa) values ('"+iduser+"','"+username+"','"+email+"','"+password+"','"+self.jeniskelamin+"','"+hobi+"','"+nowa+"')"
                        dbcursor.execute(sql)
                        db.commit()
                                                    
                        self.msg = QMessageBox()
                        self.msg.setWindowTitle("Berhasil")
                        self.msg.setText("Selamat anda berhasil membuat akun, silahkan anda login dengan menggunakan akun anda")
                        self.msg.exec_()

                        self.lineEdit_username.setText("")
                        self.lineEdit_email.setText("")
                        self.lineEdit_password.setText("")
                        self.lineEdit_confirm_pass.setText("")
                        self.lineEdit_hobi.setText("")
                        self.lineEdit_nowa.setText("")
                    else:
                        self.msg = QMessageBox()
                        self.msg.setWindowTitle("Password Tidak Sama")
                        self.msg.setText("Password dengan Confirmasi Password tidak sama, silahkan anda cocokan ulang")
                        self.msg.exec_()
                else:
                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Data Duplicate")
                    self.msg.setText("Maaf email yang anda gunakan sudah digunakan oleh user lain, silahkan anda ganti email lain")
                    self.msg.exec_()
            else:
                self.msg = QMessageBox()
                self.msg.setWindowTitle("Data Duplicate")
                self.msg.setText("Maaf username yang anda gunakan sudah digunakan oleh user lain, silahkan anda ganti username lain")
                self.msg.exec_()
        except Exception as e:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Terdapat Eror")
            self.msg.setText("Silahkan klik show detail untuk melihat eror tersebut")
            self.msg.setDetailedText(e.__str__())
            self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

    def HalamanLupaPassword(self):
        loadUi('lupapass.ui',self)
        self.btn_show_hide_password1.setCheckable(True)
        self.btn_show_hide_password2.setCheckable(True)
        self.btn_show_hide_password1.clicked.connect(self.showHidePassword1)
        self.btn_show_hide_password2.clicked.connect(self.showHidePassword2)

        self.btn_kembali.clicked.connect(self.HalamanLogin)
        self.btn_selesai.clicked.connect(self.selesailupaPassword)

    def selesailupaPassword(self):
        try:
            email = self.lineEdit_email.text()
            password = self.lineEdit_password.text()
            confirmpass = self.lineEdit_confirm_pass.text()

            if email == "":
                self.dataKosong()
            elif password == "":
                self.dataKosong()
            elif confirmpass == "":
                self.dataKosong()
            elif password == confirmpass:
                dbcursor.execute("select email from dataAkun where email like '"+email+"'")
                db.commit()
                result = dbcursor.fetchone()
                if result == None:
                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Gagal")
                    self.msg.setText("Data tidak ditemukan, mungkin anda salah dalam memasukkan email lama anda, silahkan anda coba lagi")
                    self.msg.exec_()

                    self.lineEdit_email.setText("")
                    self.lineEdit_password.setText("")
                    self.lineEdit_confirm_pass.setText("")
                else:
                    dbcursor.execute("update dataAkun set password = '"+password+"' where email = '"+email+"'")
                    db.commit()

                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Berhasil")
                    self.msg.setText("Selamat anda berhasil membuat password baru")
                    self.msg.exec_()

                    self.lineEdit_email.setText("")
                    self.lineEdit_password.setText("")
                    self.lineEdit_confirm_pass.setText("")
            else:
                self.msg = QMessageBox()
                self.msg.setWindowTitle("Password Tidak Sama")
                self.msg.setText("Password dengan Confirmasi Password tidak sama, silahkan anda cocokan ulang")
                self.msg.exec_()
        except Exception as e:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Terdapat Eror")
            self.msg.setText("Silahkan klik show detail untuk melihat eror tersebut")
            self.msg.setDetailedText(e.__str__())
            self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

    def HalamanBeranda(self):
        loadUi('beranda.ui',self)
        self.btn_linkweb.clicked.connect(self.webabout)

        self.actionBeranda.triggered.connect(self.sudahAdadihalaman)
        self.actionJoin_Forum_2.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan_2.triggered.connect(self.HalamanTanggapan)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.HalamanYoutubeDownloader)
        self.actionShort_Link.triggered.connect(self.HalamanShortLink)
        self.actionCreate_Qr_Code.triggered.connect(self.HalamanCreateQrCode)
        self.actionGunting_Batu_Kertas.triggered.connect(self.HalamanGuntingBatuKertas)
        self.actionSOS.triggered.connect(self.HalamanSOS)
        self.actionProfile_5.triggered.connect(self.HalamanProfile)

    def webabout(self):
        self.web = QWebEngineView()
        self.web.load(QUrl("https://dstartup.000webhostapp.com"))
        self.web.show()

    def HalamanJoinForum(self):
        self.web = QWebEngineView()
        self.web.load(QUrl("https://chat.whatsapp.com/JEFhyxT40Lx5YgeBdziM2C"))
        self.web.show()

    def HalamanTanggapan(self):
        loadUi('tanggapan.ui',self)
        self.btn_clear.clicked.connect(self.cleartanggapan)
        self.btn_kirim.clicked.connect(self.kirimtanggapan)

        self.actionBeranda_2.triggered.connect(self.HalamanBeranda)
        self.actionJoin_Forum_2.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan.triggered.connect(self.sudahAdadihalaman)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.HalamanYoutubeDownloader)
        self.actionShort_Link.triggered.connect(self.HalamanShortLink)
        self.actionCreate_Qr_Code.triggered.connect(self.HalamanCreateQrCode)
        self.actionGunting_Batu_Kertas.triggered.connect(self.HalamanGuntingBatuKertas)
        self.actionSOS.triggered.connect(self.HalamanSOS)
        self.actionProfile_4.triggered.connect(self.HalamanProfile)

    def cleartanggapan(self):
        self.lineEdit_nama.setText("")
        self.textEdit_tanggapan.setText("")

    def kirimtanggapan(self):
        try:
            nama = self.lineEdit_nama.text()
            tanggapan = self.textEdit_tanggapan.toPlainText()

            if nama == "":
                self.dataKosong()
            elif tanggapan == "":
                self.dataKosong()
            else:
                dbcursor.execute("insert into tanggapan(nama,tanggapan) values ('"+nama+"','"+tanggapan+"')")
                db.commit()

                self.msg = QMessageBox()
                self.msg.setWindowTitle("Berhasil")
                self.msg.setText("Terima kasih atas masukkannya kepada kami")
                self.msg.exec_()

                self.lineEdit_nama.setText("")
                self.textEdit_tanggapan.setPlainText("")
        except Exception as e:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Terdapat Eror")
            self.msg.setText("Silahkan klik show detail untuk melihat eror tersebut")
            self.msg.setDetailedText(e.__str__())
            self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

    def HalamanCekIP(self):
        perintah = "ipconfig"
        p = os.popen(perintah)
        if p:
                hasil = p.read()
                self.msg = QMessageBox()
                self.msg.setWindowTitle("Berhasil Cek IP")
                self.msg.setText("Selamat anda berhasil mengecek IP anda sendiri, silahkan anda klik show detail untuk melihat ip anda")
                self.msg.setDetailedText(hasil.__str__())
                self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
                self.msg.exec_()

    def HalamanYoutubeDownloader(self):
        loadUi('ytDownloader.ui',self)
        self.pushButton.clicked.connect(self.downloadvideoyt)

        self.actionBeranda.triggered.connect(self.HalamanBeranda)
        self.actionJoin_Forum.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan.triggered.connect(self.HalamanTanggapan)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.sudahAdadihalaman)
        self.actionShort_Link.triggered.connect(self.HalamanShortLink)
        self.actionCreate_Qr_Code.triggered.connect(self.HalamanCreateQrCode)
        self.actionGunting_Batu_Kertas.triggered.connect(self.HalamanGuntingBatuKertas)
        self.actionSOS.triggered.connect(self.HalamanSOS)
        self.actionProfile_3.triggered.connect(self.HalamanProfile)

    def downloadvideoyt(self):
        try:
            link = self.lineEdit.text()
            video = YouTube(link)
            stream = video.streams.get_highest_resolution()
            stream.download()

            if link == "":
                self.dataKosong()
            else:
                if stream:
                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Berhasil")
                    self.msg.setText("Selamat anda berhasil men download video dari YouTube")
                    self.msg.exec_()

                    self.lineEdit.setText("")
                else:
                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Gagal")
                    self.msg.setText("Anda gagal download video dari YouTube, silahkan anda periksa koneksi anda atau periksa link nya apakah sudah benar atau tidak")
                    self.msg.exec_()
        except Exception as e:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Terdapat Eror")
            self.msg.setText("Silahkan klik show detail untuk melihat eror tersebut")
            self.msg.setDetailedText(e.__str__())
            self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

    def HalamanShortLink(self):
        loadUi('shortlink.ui',self)
        self.pushButton.clicked.connect(self.eksekusishortlink)

        self.actionBeranda.triggered.connect(self.HalamanBeranda)
        self.actionJoin_Forum.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan.triggered.connect(self.HalamanTanggapan)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.HalamanYoutubeDownloader)
        self.actionShort_Link.triggered.connect(self.sudahAdadihalaman)
        self.actionCreate_Qr_Code.triggered.connect(self.HalamanCreateQrCode)
        self.actionGunting_Batu_Kertas.triggered.connect(self.HalamanGuntingBatuKertas)
        self.actionSOS.triggered.connect(self.HalamanSOS)
        self.actionProfile_3.triggered.connect(self.HalamanProfile)

    def eksekusishortlink(self):
        try:
            link = self.lineEdit.text()
            baseUrl = "http://tinyurl.com/api-create.php?url="
            url = baseUrl + link
            r = requests.get(url)
            hasil = r.text

            self.msg = QMessageBox()
            self.msg.setWindowTitle("Berhasil")
            self.msg.setText("Selamat anda berhasil membuat link anda menjadi lebih pendek, silahkan klik show detail untuk melihat hasil shortenernya")
            self.msg.setDetailedText(hasil.__str__())
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

            self.lineEdit.setText("")
        except Exception as apakek:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Terjadinya Eror")
            self.msg.setText("Telah terjadi eror pada program, klik detail show untuk melihat eror tersebut")
            self.msg.setDetailedText(apakek.__str__())
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

    def HalamanCreateQrCode(self):
        loadUi('qrcode.ui',self)
        self.btn_create.clicked.connect(self.fungsiCreateQrCode)

        self.actionBeranda.triggered.connect(self.HalamanBeranda)
        self.actionJoin_Forum.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan.triggered.connect(self.HalamanTanggapan)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.HalamanYoutubeDownloader)
        self.actionShort_Link.triggered.connect(self.HalamanShortLink)
        self.actionCreate_Qr_Code.triggered.connect(self.sudahAdadihalaman)
        self.actionGunting_Batu_Kertas.triggered.connect(self.HalamanGuntingBatuKertas)
        self.actionSOS.triggered.connect(self.HalamanSOS)
        self.actionProfile_3.triggered.connect(self.HalamanProfile)

    def fungsiCreateQrCode(self):
        input = self.lineEdit.text()
        eksekusi = qrcode.make(input)
        num = str(random.randint(1, 9999))
        eksekusi.save(num + ".png")

        self.msg = QMessageBox()
        self.msg.setWindowTitle("Berhasil")
        self.msg.setText("Selamat anda berhasil membuat " + input + " menjadi Qr Code")
        self.msg.exec_()

        self.lineEdit.setText("")

    def HalamanGuntingBatuKertas(self):
        loadUi('guntingbatukertas.ui',self)

        self.actionBeranda.triggered.connect(self.HalamanBeranda)
        self.actionJoin_Forum.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan.triggered.connect(self.HalamanTanggapan)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.HalamanYoutubeDownloader)
        self.actionShort_Link.triggered.connect(self.HalamanShortLink)
        self.actionCreate_Qr_Code.triggered.connect(self.HalamanCreateQrCode)
        self.actionGunting_Batu_Kertas.triggered.connect(self.sudahAdadihalaman)
        self.actionSOS.triggered.connect(self.HalamanSOS)
        self.actionProfile_2.triggered.connect(self.HalamanProfile)

        self.btn_gunting.clicked.connect(self.usrgunting)
        self.btn_batu.clicked.connect(self.usrbatu)
        self.btn_kertas.clicked.connect(self.usrkertas)

    def usrgunting(self):
        bot = ['gunting','batu','kertas']
        x = random.choice(bot)
        user = "gunting"

        if user and x == "gunting":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda seri")
        elif user and x == "batu":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda Kalah")
        elif user and x == "kertas":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda menang")

    def usrbatu(self):
        bot = ['gunting','batu','kertas']
        x = random.choice(bot)
        user = "batu"

        if user and x == "gunting":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda menang")
        elif user and x == "batu":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda seri")
        elif user and x == "kertas":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda kalah")
    
    def usrkertas(self):
        bot = ['gunting','batu','kertas']
        x = random.choice(bot)
        user = "kertas"

        if user and x == "gunting":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda kalah")
        elif user and x == "batu":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda menang")
        elif user and x == "kertas":
            self.label_4.setText(x)
            self.label_5.setText(user)
            self.label_6.setText("Hasilnya adalah anda seri")

    def HalamanSOS(self):
        loadUi('sos.ui',self)

        self.actionBeranda.triggered.connect(self.HalamanBeranda)
        self.actionJoin_Forum.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan.triggered.connect(self.HalamanTanggapan)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.HalamanYoutubeDownloader)
        self.actionShort_Link.triggered.connect(self.HalamanShortLink)
        self.actionCreate_Qr_Code.triggered.connect(self.HalamanCreateQrCode)
        self.actionGunting_Batu_Kertas.triggered.connect(self.HalamanGuntingBatuKertas)
        self.actionSOS.triggered.connect(self.sudahAdadihalaman)
        self.actionProfile_2.triggered.connect(self.HalamanProfile)

        self.hitung = 0

        self.sos1 = self.findChild(QPushButton, "btn_sos1")
        self.sos2 = self.findChild(QPushButton, "btn_sos2")
        self.sos3 = self.findChild(QPushButton, "btn_sos3")
        self.sos4 = self.findChild(QPushButton, "btn_sos4")
        self.sos5 = self.findChild(QPushButton, "btn_sos5")
        self.sos6 = self.findChild(QPushButton, "btn_sos6")
        self.sos7 = self.findChild(QPushButton, "btn_sos7")
        self.sos8 = self.findChild(QPushButton, "btn_sos8")
        self.sos9 = self.findChild(QPushButton, "btn_sos9")

        self.btn_sos1.clicked.connect(lambda: self.jalan(self.sos1))
        self.btn_sos2.clicked.connect(lambda: self.jalan(self.sos2))
        self.btn_sos3.clicked.connect(lambda: self.jalan(self.sos3))
        self.btn_sos4.clicked.connect(lambda: self.jalan(self.sos4))
        self.btn_sos5.clicked.connect(lambda: self.jalan(self.sos5))
        self.btn_sos6.clicked.connect(lambda: self.jalan(self.sos6))
        self.btn_sos7.clicked.connect(lambda: self.jalan(self.sos7))
        self.btn_sos8.clicked.connect(lambda: self.jalan(self.sos8))
        self.btn_sos9.clicked.connect(lambda: self.jalan(self.sos9))
        self.btn_reset.clicked.connect(self.reset)

    def menang(self):
        if self.btn_sos1.text() == "X" and self.btn_sos2.text() == "X" and self.btn_sos3.text() == "X":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos3.text() == "X" and self.btn_sos6.text() == "X" and self.btn_sos9.text() == "X":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos7.text() == "X" and self.btn_sos8.text() == "X" and self.btn_sos9.text() == "X":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos1.text() == "X" and self.btn_sos4.text() == "X" and self.btn_sos7.text() == "X":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos1.text() == "X" and self.btn_sos5.text() == "X" and self.btn_sos9.text() == "X":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos3.text() == "X" and self.btn_sos5.text() == "X" and self.btn_sos7.text() == "X":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos2.text() == "X" and self.btn_sos5.text() == "X" and self.btn_sos8.text() == "X":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos4.text() == "X" and self.btn_sos5.text() == "X" and self.btn_sos6.text() == "X":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos1.text() == "O" and self.btn_sos2.text() == "O" and self.btn_sos3.text() == "O":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos3.text() == "O" and self.btn_sos6.text() == "O" and self.btn_sos9.text() == "O":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos7.text() == "O" and self.btn_sos8.text() == "O" and self.btn_sos9.text() == "O":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos1.text() == "O" and self.btn_sos4.text() == "O" and self.btn_sos7.text() == "O":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos1.text() == "O" and self.btn_sos5.text() == "O" and self.btn_sos9.text() == "O":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos3.text() == "O" and self.btn_sos5.text() == "O" and self.btn_sos7.text() == "O":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos2.text() == "O" and self.btn_sos5.text() == "O" and self.btn_sos8.text() == "O":
            self.label_7.setText(self.player)
            self.enabletombol()
        elif self.btn_sos4.text() == "O" and self.btn_sos5.text() == "O" and self.btn_sos6.text() == "O":
            self.label_7.setText(self.player)
            self.enabletombol()
        
    def jalan(self, b):
        if self.hitung % 2 == 0:
            p = "X"
            self.label_9.setText("Player 2")
            self.player = "Player 1"
        else:
            p = "O"
            self.label_9.setText("Player 1")
            self.player = "Player 2"

        b.setText(p)
        b.setEnabled(False)

        self.hitung += 1

        self.menang()

    def enabletombol(self):
        p = [self.sos1,self.sos2,self.sos3,self.sos4,self.sos5,self.sos6,self.sos7,self.sos8,self.sos9]

        for a in p:
            a.setEnabled(False)
            self.label_9.setText(".............")

    def reset(self):
        p = [self.sos1,self.sos2,self.sos3,self.sos4,self.sos5,self.sos6,self.sos7,self.sos8,self.sos9]
        for a in p:
            a.setText("")
            self.label_9.setText(".............")
            self.label_7.setText("...")
            a.setEnabled(True)

    def HalamanProfile(self):
        loadUi('profile.ui',self)

        self.label_username.setText(self.usernameuser)
        self.label_email.setText(self.emailuser)
        self.label_password.setText(self.passworduser)
        self.label_jeniskelamin.setText(self.jeniskelaminuser)
        self.label_hobi.setText(self.hobiuser)
        self.label_nowa.setText(self.nowauser)

        self.label_username.setEnabled(False)
        self.label_email.setEnabled(False)
        self.label_password.setEnabled(False)
        self.label_jeniskelamin.setEnabled(False)
        self.label_hobi.setEnabled(False)
        self.label_nowa.setEnabled(False)

        self.btn_logout.clicked.connect(self.inginlogout)
        self.btn_hapusakun.clicked.connect(self.hapusakun)
        self.btn_edit.clicked.connect(self.HalamanEditProfile)

        self.btn_show_hide_password.setCheckable(True)
        self.btn_show_hide_password.clicked.connect(self.showhideprofile)

        self.actionBeranda.triggered.connect(self.HalamanBeranda)
        self.actionJoin_Forum.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan.triggered.connect(self.HalamanTanggapan)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.HalamanYoutubeDownloader)
        self.actionShort_Link.triggered.connect(self.HalamanShortLink)
        self.actionCreate_Qr_Code.triggered.connect(self.HalamanCreateQrCode)
        self.actionGunting_Batu_Kertas.triggered.connect(self.HalamanGuntingBatuKertas)
        self.actionSOS.triggered.connect(self.HalamanSOS)
        self.actionProfile.triggered.connect(self.sudahAdadihalaman)

    def showhideprofile(self):
        if self.btn_show_hide_password.isChecked():
            self.label_password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.label_password.setEchoMode(QtWidgets.QLineEdit.Password)

    def inginlogout(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Ingin Log Out")
        self.msg.setText("Apakah anda yakin ingin log out ?")
        self.msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.penentulogout)
        self.msg.exec_()

    def penentulogout(self, i):
        p = i.text()
        if p == "OK":
            self.HalamanLogin()
        else:
            self.HalamanProfile()

    def hapusakun(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Hapus Akun")
        self.msg.setText("Yakin anda ingin hapus akun ? ")
        self.msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.inginhapusakun)
        self.msg.exec_()
    
    def inginhapusakun(self, i):
        try:
            p = i.text()
            if p == "OK":
                dbcursor.execute("delete from dataakun where iduser = '"+self.iduser+"'")
                db.commit()

                self.msg = QMessageBox()
                self.msg.setWindowTitle("Berhasil")
                self.msg.setText("Selamat anda berhasil hapus akun anda yang lama, anda akan diarahkan ke halaman login")
                self.msg.exec_()

                self.HalamanLogin()
            else:
                self.HalamanProfile()
        except Exception as e:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Terdapat Eror")
            self.msg.setText("Silahkan klik show detail untuk melihat eror tersebut")
            self.msg.setDetailedText(e.__str__())
            self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

    def HalamanEditProfile(self):
        loadUi('editprofile.ui',self)

        self.lineEdit_username.setText(self.usernameuser)
        self.lineEdit_email.setText(self.emailuser)
        self.lineEdit_password.setText(self.passworduser)
        self.lineEdit_hobi.setText(self.hobiuser)
        self.lineEdit_nowa.setText(self.nowauser)

        self.btn_selesai.clicked.connect(self.penyortirandata)
        self.btn_kembali.clicked.connect(self.HalamanProfile)

        self.usrnamelama = self.lineEdit_username.text()
        self.emaillama = self.lineEdit_email.text()

        self.rb_lakilaki.toggled.connect(self.rblakiregistrasi)
        self.rb_perempuan.toggled.connect(self.rbperempuanregistrasi)

        self.actionBeranda.triggered.connect(self.HalamanBeranda)
        self.actionJoin_Forum.triggered.connect(self.HalamanJoinForum)
        self.actionBeri_Tanggapan.triggered.connect(self.HalamanTanggapan)
        self.actionCek_IP.triggered.connect(self.HalamanCekIP)
        self.actionYouTube_Downloader.triggered.connect(self.HalamanYoutubeDownloader)
        self.actionShort_Link.triggered.connect(self.HalamanShortLink)
        self.actionCreate_Qr_Code.triggered.connect(self.HalamanCreateQrCode)
        self.actionGunting_Batu_Kertas.triggered.connect(self.HalamanGuntingBatuKertas)
        self.actionSOS.triggered.connect(self.HalamanSOS)
        self.actionProfile.triggered.connect(self.sudahAdadihalaman)

    def penyortirandata(self):
        try:
            username = self.lineEdit_username.text()
            email = self.lineEdit_email.text()

            if not self.usrnamelama == username:
                dbcursor.execute("select * from dataakun where username = '"+username+"'")
                db.commit()
                cekusername = dbcursor.fetchone()

                if cekusername == None:
                    if not self.emaillama == email:
                        dbcursor.execute("select * from dataakun where email = '"+email+"'")
                        db.commit()
                        cekemail = dbcursor.fetchone()

                        if cekemail == None:
                            self.eksekusiupdateprofile()
                        else:
                            self.msg = QMessageBox()
                            self.msg.setWindowTitle("Data Duplicate")
                            self.msg.setText("Maaf email yang anda gunakan sudah digunakan oleh user lain, silahkan anda ganti email lain")
                            self.msg.exec_()
                    else:
                        self.eksekusiupdateprofile()
                else:
                    self.msg = QMessageBox()
                    self.msg.setWindowTitle("Data Duplicate")
                    self.msg.setText("Maaf username yang anda gunakan sudah digunakan oleh user lain, silahkan anda ganti username lain")
                    self.msg.exec_()
            else:
                if not self.emaillama == email:
                    dbcursor.execute("select * from dataakun where email = '"+email+"'")
                    db.commit()
                    cekemail = dbcursor.fetchone()

                    if cekemail == None:
                        self.eksekusiupdateprofile()
                    else:
                        self.msg = QMessageBox()
                        self.msg.setWindowTitle("Data Duplicate")
                        self.msg.setText("Maaf email yang anda gunakan sudah digunakan oleh user lain, silahkan anda ganti email lain")
                        self.msg.exec_()
                else:
                    self.eksekusiupdateprofile()
        except Exception as e:
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Terdapat Eror")
            self.msg.setText("Silahkan klik show detail untuk melihat eror tersebut")
            self.msg.setDetailedText(e.__str__())
            self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()

    def eksekusiupdateprofile(self):
        username = self.lineEdit_username.text()
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()
        hobi = self.lineEdit_hobi.text()
        nowa = self.lineEdit_nowa.text()

        if username == "":
            self.dataKosong()
        elif email == "":
            self.dataKosong()
        elif password == "":
            self.dataKosong()
        elif hobi == "":
            self.dataKosong()
        elif nowa == "":
            self.dataKosong()
        else:
            dbcursor.execute("update dataakun set username = '"+username+"', email = '"+email+"', password = '"+password+"', jeniskelamin = '"+self.jeniskelamin+"', hobi = '"+hobi+"', nowa = '"+nowa+"' where iduser = '"+self.iduser+"' ")
            db.commit()
            
            self.msg = QMessageBox()
            self.msg.setWindowTitle("Berhasil")
            self.msg.setText("Selamat anda berhasil mengubah data")
            self.msg.exec_()

            self.usernameuser = username
            self.emailuser = email
            self.passworduser = password
            self.jeniskelaminuser = self.jeniskelamin
            self.hobiuser = hobi
            self.nowauser = nowa

            self.HalamanProfile()

application = QApplication(sys.argv)
form = MyApp()
form.show()
try:
    sys.exit(application.exec_())
except Exception as e:
    print("Program berhenti")