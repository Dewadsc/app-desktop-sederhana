import sqlite3

db = sqlite3.connect('dewabuana.db')
dbcursor = db.cursor()

dbcursor.execute("create table if not exists dataakun (iduser int(255) NOT NULL,username varchar(255) NOT NULL,email varchar(255) NOT NULL,password varchar(255) NOT NULL,jeniskelamin varchar(255) NOT NULL,hobi varchar(255) NOT NULL,nowa varchar(255) NOT NULL,PRIMARY KEY(iduser))")
db.commit()

dbcursor.execute("create table if not exists tanggapan (nama varchar(255) NOT NULL,tanggapan varchar(4000) NOT NULL,PRIMARY KEY(nama))")
db.commit()