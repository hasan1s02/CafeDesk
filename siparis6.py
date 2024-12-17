import tkinter as tk
from PIL import Image, ImageTk
import pyodbc
import uuid
from tkinter import messagebox,PhotoImage
import os
import time
from datetime import datetime
import threading
mac_address = uuid.getnode()
mac_address_hex = '-'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0, 8 * 6, 8)][::-1])

# Veritabanı bağlantısı oluştur
server = '192.168.1.1'
database = 'zzzzz'
username = 'ssssss'
password = 'ssssssd'

try:
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
except pyodbc.Error as err:
    print(f"Veritabanı hatası: {err}")
    exit(1)

# Menü kategorilerini ve kategori resimlerini tanımla
menu_kategori = {
    "Hamburgerler": {"resim": "hamburger.jpg", "aciklama": "Lezzetli hamburgerlerimizi deneyin.", "tip": "H"},
    "Dürümler": {"resim": "durum.jpg", "aciklama": "Taze ve lezzetli dürümler.", "tip": "D"},
    "İçecekler": {"resim": "icecek.jpg", "aciklama": "Serinletici içecekler.", "tip": "İ"},
    "Ekmek Arası": {"resim": "ekmek.jpg", "aciklama": "Lezzetli ekmek arası atıştırmalıklar.", "tip": "E"},
    "Tatlılar": {"resim": "tatli.jpg", "aciklama": "Tatlı krizlerinizi giderin.", "tip": "T"},
    "Salatalar": {"resim": "salata.jpg", "aciklama": "Sağlıklı ve lezzetli salatalar.", "tip": "S"},
    "Sandviçler": {"resim": "sandvic.jpg", "aciklama": "Lezzetli sandviçler.", "tip": "S"},
    "Çorbalar": {"resim": "corba.jpg", "aciklama": "Sıcak çorbalar.", "tip": "Ç"},
    "Pizzalar": {"resim": "pizza.jpg", "aciklama": "Pizza çeşitlerimizle lezzet şöleni.", "tip": "P"},
    "Makarnalar": {"resim": "makarna.jpg", "aciklama": "Makarna çeşitlerimiz.", "tip": "M"},
}
# Mutfak hesabı ve internet ücreti hesabını temsil eden değişkenler
mutfak_hesabi = 0
internet_ucreti_hesabi = 0

# Ana pencere oluştur
root = tk.Tk()
root.title("ZOCCO'S MENÜ")
# Arka plan resmini yükle

arka_plan_resmi = PhotoImage(file="arka_plan_resmi.png")

# Arka plan resmini gösteren bir etiket oluşturun
arka_plan_etiket = tk.Label(root, image=arka_plan_resmi)
arka_plan_etiket.place(x=0, y=0, relwidth=1, relheight=1)  # Etiketi pencere boyutuna uydurun




# Üst çerçeve (frame) oluşturun
ust_cerceve = tk.Frame(root)
ust_cerceve.pack(side=tk.TOP, fill=tk.X)  # X ekseni boyunca genişletin, y ekseni boyunca sadece üst kısmı kaplasın
toplam_hesap = internet_ucreti_hesabi + mutfak_hesabi
# Toplam hesabı güncellemek için bir etiket oluşturun
toplam_hesap_label = tk.Label(ust_cerceve, text=f"Toplam Ücret: {toplam_hesap} TL", fg="white",  font=("Arial", 14))
toplam_hesap_label.pack(side=tk.RIGHT, padx=10, pady=3)

# Sağ üst köşede mutfak ve internet ücreti hesaplarını yazdırmak için etiketler oluştur
mutfak_label = tk.Label(ust_cerceve, text=f"Mutfak Ücreti: {mutfak_hesabi} TL", fg="white", font=("Arial", 14))
mutfak_label.pack(side=tk.RIGHT, padx=10, pady=3)

internet_ucreti_label = tk.Label(ust_cerceve, text=f"İnternet Ücreti: {internet_ucreti_hesabi} TL", fg="white",  font=("Arial", 14))
internet_ucreti_label.pack(side=tk.RIGHT, padx=10, pady=3)



# Ekranı tam ekran yap
root.attributes("-fullscreen", True)

# Arka plan rengini siyah yap


# Ürünleri göstermek için çerçeve
urunler_frame = None

# Geri Dön düğmesi
geri_button = None
geri_button2 = None
sepet_temizleme = None
# Sayfanın üstünden ve altından boşluklar ekleyin
top_space = tk.Frame(root, height=50)
top_space.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

bottom_space = tk.Frame(root, height=50)
bottom_space.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Başlık için etiket
baslik_label = tk.Label(root, text="ZOCCO'S MENÜ", font=("Arial", 36), fg="red")
baslik_label.pack()

# Kategori düğmelerini içeren çerçeve
kategori_frame = tk.Frame(root)
kategori_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Her bir düğme için boyut ayarları
button_width = int(root.winfo_screenwidth() / 6)
button_height = int(root.winfo_screenheight() / 4)
button_color = "dark red"

# Kategori düğmelerini oluştur
kategori_buttons = {}

def on_category_button_enter(event, button):
    button.configure(bg="red")  # Fare butonun üstüne geldiğinde rengi değiştirin

def on_category_button_leave(event, button):
    button.configure(bg=button_color)
def on_category_image_enter(event, label):
    label.configure(bg="red")  # Fare resmin üstüne geldiğinde rengi değiştirin
    # Resmi büyütmek veya başka bir işlevi burada ekleyebilirsiniz

def on_category_image_leave(event, label):
    label.configure(bg="black")  # Fare resmin üstünden çekildiğinde rengi eski haline getirin

def on_category_image_click(category):
    global kategori_frame, urunler_frame, geri_button
    kategori_frame.destroy()
    urunleri_goster(category)


def kategori_dugmeleri_olustur():
    for i, (category, data) in enumerate(menu_kategori.items()):
        # Kategori resmi
        category_image = Image.open(data["resim"])
        category_image = category_image.resize((button_width, button_height), Image.LANCZOS)

        # Resmin üst kısmına açıklamayı ekleyin

        category_text = data["aciklama"]
        category_image = ImageTk.PhotoImage(category_image)
        label = tk.Label(kategori_frame, text=category_text, image=category_image, compound=tk.TOP,
                         fg="white")
        label.image = category_image
        label.grid(row=(i // 5) * 2, column=i % 5, padx=20, pady= 15, sticky="n")
        label.bind("<Button-1>", lambda event, category=category: on_category_image_click(category))
        label.bind("<Enter>", lambda event, label=label: on_category_image_enter(event, label))
        label.bind("<Leave>", lambda event, label=label: on_category_image_leave(event, label))

        # Kategori düğmesi
        button = tk.Button(kategori_frame, text=category,
                           command=lambda category=category: on_category_button_click(category), fg="white",
                           bg=button_color, font=("Arial", 18))
        button.grid(row=((i // 5) * 2) + 1, column=i % 5, padx=20, pady=15, sticky="s")
        kategori_buttons[category] = button  # Kategori düğmesini sözlüğe ekleyin
        # Fare olaylarını bağlayın
        button.bind("<Enter>", lambda event, button=button: on_category_button_enter(event, button))
        button.bind("<Leave>", lambda event, button=button: on_category_button_leave(event, button))


kategori_dugmeleri_olustur()
# Sepeti temsil edecek liste
sepet = []
sepet_frame = tk.Frame(root)
# Sepet düğmesi işlevi
def sepeti_goster():
    global urunler_frame, kategori_frame,sepet_frame,geri_button2,sepet_temizleme
    # Eğer urunler_frame açıksa kapat
    if urunler_frame:
        urunler_frame.destroy()
    # Eğer kategori_frame açıksa kapat
    if kategori_frame:
        kategori_frame.destroy()
    sepeti_gizle()

        # Geri Dön düğmesini oluştur
    geri_button2 = tk.Button(root, text="Geri Dön", command=ana_sayfaya_don, fg="white", bg="dark red",
                            font=("Arial", 16))
    geri_button2.pack(side=tk.TOP, padx=10, pady=10)

    # Sepet çerçevesini güncelle
    guncelle_sepet()
    # Sepet çerçevesini paketle ve ekranda göster
    sepet_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Sepet düğmesi
sepet_button = tk.Button(top_space, text="Sepet", command=sepeti_goster, fg="white", bg="dark red", font=("Arial", 16))
sepet_button.pack(side=tk.LEFT, padx=10, pady=10)
def sepet_aktif():
    sepet_button.pack(side=tk.LEFT, padx=10, pady=10)
def sepeti_gizle():
    sepet_button.pack_forget()
def ana_sayfaya_don():
    global kategori_frame, sepet_frame,geri_button2,sepet_temizleme
    # Eğer sepet_frame açıksa kapat
    if sepet_temizleme:
        sepet_temizleme.destroy()
    if geri_button2:
        geri_button2.destroy()
    if sepet_frame:
        print("sdfasdgfgfdsdf")
        sepet_frame.destroy()
    sepet_aktif()
    # Kategori çerçevesini yeniden oluştur ve göster
    kategori_frame = tk.Frame(root)
    kategori_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    kategori_dugmeleri_olustur()
    sepet_frame = tk.Frame(root)
def guncelle_sepet():
    # Sepet çerçevesi henüz oluşturulmamışsa, önce sepet çerçevesini oluşturun
    global sepet_frame  # Sepet çerçevesini global olarak tanımla
    print("asd123")
    # Sepet çerçevesi henüz oluşturulmamışsa, önce sepet çerçevesini oluşturun
    if not sepet_frame:
        print("asd1243253")
        return
    print("asd")
    print(sepet_frame)
    # Sepet çerçevesini temizle
    for widget in sepet_frame.winfo_children():
        widget.destroy()

    # Sepet ürünlerini listele
    for i, urun in enumerate(sepet):
        label = tk.Label(sepet_frame, text=f"{urun['ad']} - {urun['fiyat']} TL", font=("Arial", 16), fg="white", bg="black")
        label.pack(padx=20, pady=20, anchor="w")

    # Toplam fiyatı hesapla
    toplam_fiyat = sum([urun['fiyat'] for urun in sepet])
    toplam_label = tk.Label(sepet_frame, text=f"Toplam Fiyat: {toplam_fiyat} TL", font=("Arial", 16), fg="white", bg="black")
    toplam_label.pack(padx=20, pady=20, anchor="w")

    # Siparişi Onayla düğmesi
    onayla_button = tk.Button(sepet_frame, text="Siparişi Onayla", command=siparisi_onayla, fg="white", bg="dark red", font=("Arial", 16))
    onayla_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    # Temizle düğmesi
    temizle_button = tk.Button(sepet_frame, text="Sepeti Temizle", command=sepeti_temizle, fg="white", bg="dark blue", font=("Arial", 16))
    temizle_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Sepete eklemek için işlev
def sepete_ekle(urun_adı, urun_fiyatı):
    sepet.append({"ad": urun_adı, "fiyat": urun_fiyatı})
    print(urun_adı)


def adisyon_acilsi():
    cursor.execute("SELECT * FROM masa WHERE mac = ?", mac_address_hex)
    veri = cursor.fetchall()
    print(veri)
    # print(veri)
    # Adisyon numarasını alma
    adisyon_no = veri[0][7]

    acilis_zaman = veri[0][10]

    return adisyon_no,acilis_zaman
def mutfak_sip(adisyon_no):
    cursor.execute("SELECT * FROM detay WHERE adisyon_no = ?", adisyon_no)
    veri = cursor.fetchall()
    return veri
def guncelle_hesap():
    while True:
        adisyon_no, acilis_zamani = adisyon_acilsi()
        if adisyon_no == 0:
            time.sleep(10)
        else:

            suanki_tarih = datetime.now()
            gecen_sure = suanki_tarih - acilis_zamani
            print(gecen_sure)
            # Toplam saniyeleri al
            toplam_saniyeler = gecen_sure.total_seconds()

            # Dakikaya çevir
            gecen_dakika = int(toplam_saniyeler / 60)

            if gecen_dakika < 5:
                internet_ucreti = 0
            elif 5 < gecen_dakika < 15:
                internet_ucreti = 15
            elif 15 < gecen_dakika < 30:
                internet_ucreti = 15
            else:
                internet_ucreti = int(gecen_dakika * 0.5)
            mutfak_hesap = 0
            mutfak_siparisleri = mutfak_sip(adisyon_no)
            if mutfak_siparisleri:
                mutfak_hesap = 0
                for i in mutfak_siparisleri:
                    iptal_control = i[10]
                    if iptal_control:
                        print("silinmis")
                    else:
                        mutfak_hesap += i[8]


            # Sürteş fiyatını güncelle
            mutfak_label.config(text=f"Mutfak Ücreti: {mutfak_hesap} TL")
            internet_ucreti_label.config(text=f"İnternet Ücreti: {internet_ucreti} TL")
            toplam_hesap_label.config( text=f"Toplam Hesap: {mutfak_hesap + internet_ucreti}")
            time.sleep(10)
threading.Thread(target=guncelle_hesap).start()
def adisyon():
    cursor.execute("SELECT * FROM masa WHERE mac = ?", mac_address_hex)
    veri = cursor.fetchall()
    print(veri)
    # print(veri)
    # Adisyon numarasını alma
    adisyon_no = veri[0][7]
    # print(adisyon_no)
    return adisyon_no
def urun_kod(isim):
    cursor.execute("SELECT kod FROM urun WHERE ad = ?", (isim,))
    urun_veri = cursor.fetchone()  # Tek bir sonuç bekliyorsanız fetchone kullanabilirsiniz.
    if urun_veri:
        return urun_veri[0]
    else:
        return None  # Ürün bulunamadıysa None dönebilirsiniz.
def detay(adisyon_no2,siparisid3, urun_kod2, Urun_isim,Urun_fiyat):
    detay_tablosu = "INSERT INTO detay(adisyon_no,siparis_no,urun_kod,urun_ad,miktar,birim,fiyat,tutar,durum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(detay_tablosu, (adisyon_no2, siparisid3, urun_kod2, Urun_isim, '1', '', Urun_fiyat, Urun_fiyat, ''))
    cursor.commit()
def siparis_gonder(siparisid3,adisyon_no2):
    # siparis tablosu
    siparisi_tablosu = "INSERT INTO siparis(siparis_no,adisyon_no,aciklama,durum)VALUES (?,?,?,?)"
    cursor.execute(siparisi_tablosu, (siparisid3, adisyon_no2, 'Musteri', '0',))
    cursor.commit()
def update_siparis_no():
    update_siparis_No = "UPDATE id SET id = id+1 WHERE ad = 'siparis'"
    cursor.execute(update_siparis_No)
    cursor.commit()

def siparisi_onayla():
    global sepet
    adisyon_no2 = adisyon()
    print(adisyon_no2)
    print("324453245")
    if adisyon_no2 == 0:
        messagebox.showinfo("adisyon hatasi","Masaniz acık degil")
    else:
        toplam_fiyat = 0
        print(sepet)
        siparis_id2 = "select id from id where ad = 'siparis'"
        cursor.execute(siparis_id2)
        siparis_id = cursor.fetchone()
        siparis_no = siparis_id[0] + 1
        if sepet:
            for i in sepet:
                print(i)
                Urun_isim = i['ad']
                Urun_fiyat2 = i['fiyat']
                Urun_fiyat = float(Urun_fiyat2)
                toplam_fiyat = toplam_fiyat + Urun_fiyat
                siparisid3 = 0

                urun_kod2 = urun_kod(Urun_isim)
                # detay tablosu
                detay(adisyon_no2, siparis_no, urun_kod2, Urun_isim, Urun_fiyat)

            siparis_gonder(siparis_no, adisyon_no2)

            update_siparis_no()

            messagebox.showinfo("Sipariş Onayı", f"Siparişiniz alındı. Toplam Fiyat: {toplam_fiyat} TL")
        else:
            messagebox.showinfo("sipariş hatası","siparişiniz gözükmüyor")
            return
    # Sepeti temizle
    sepet.clear()

    ana_sayfaya_don()

def sepeti_temizle():
    global sepet
    sepet = []
    guncelle_sepet()
# Kategoriye tıklanıldığında ürünleri gösteren fonksiyon
def on_category_button_click(category):
    global kategori_frame, urunler_frame, geri_button
    kategori_frame.destroy()

    urunleri_goster(category)

def on_sepet_button_enter(event, button):
    button.configure(bg="green")  # Fare butonun üstüne geldiğinde rengi değiştirin

def on_sepet_button_leave(event, button):
    button.configure(bg= "dark green")
# Ürünleri gösteren fonksiyon
def urunleri_goster(kategori):
    global urunler_frame, geri_button
    sepeti_gizle()

    def geri_don():
        global kategori_frame, urunler_frame, geri_button
        if urunler_frame:
            urunler_frame.destroy()  # Ürünler çerçevesini yok et
        if geri_button:
            geri_button.destroy()  # Geri dön düğmesini yok et

        # Yeni bir kategori çerçevesi oluşturun
        kategori_frame = tk.Frame(root, bg="black")
        kategori_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        kategori_dugmeleri_olustur()  # Yeni kategori düğmelerini oluşturun
        sepet_aktif()

    urun_sayaci = 0
    kategori_kodu = None
    print(kategori)

    if kategori == "Hamburgerler":
        kategori_kodu = "H-%"
    if kategori == "Dürümler":
        kategori_kodu = "D-%"
    if kategori == "İçecekler":
        kategori_kodu = "İ-%"
    if kategori == "Ekmek Arası":
        kategori_kodu = "Y-%"
    if kategori == "Makarnalar":
        kategori_kodu = "M-%"
    if kategori == "Pizzalar":
        kategori_kodu = "M-%"
    if kategori_kodu:
        cursor.execute(f"SELECT * FROM urun WHERE aktif = '1' and tip = '1' and kod LIKE ?",
                       (kategori_kodu,))
    else:
        # Kategori kodu belirlenmemişse tüm ürünleri çek
        cursor.execute(f"SELECT * FROM urun WHERE aktif = '1' and tip = '1'")
    urunler_veri = cursor.fetchall()

    # Geri Dön düğmesi
    geri_button = tk.Button(root, text="Geri dön", command=geri_don, fg="white", bg="dark red", font=("Arial", 16))
    geri_button.pack(side=tk.TOP, padx=10, pady=10)

    def mouse_wheel(event):
        # Mouse tekerleği olayını işle
        if event.delta:
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

    urunler_frame = tk.Frame(root, bg="black")
    urunler_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar'ı oluşturun ve urunler_frame'e bağlayın
    scrollbar = tk.Scrollbar(urunler_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas = tk.Canvas(urunler_frame, bg="black", yscrollcommand=scrollbar.set, highlightthickness=0,
                       highlightbackground="black")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=canvas.yview)
    # Mouse tekerleği olayını canvas'a bağlayın
    canvas.bind_all("<MouseWheel>", mouse_wheel)

    urunler_inner_frame = tk.Frame(canvas, bg="black")
    canvas.create_window((0, 0), window=urunler_inner_frame, anchor=tk.NW)

    page_width = 0  # Sayfa genişliği için sıfırdan başlayın
    max_row_height = 800  # Satırın maksimum yüksekliği

    # Satırın maksimum ürün sayısı
    maksimum_urun_sayisi = 5
    scrollbar.pack_forget()
    for i, urun in enumerate(urunler_veri):
        if i % maksimum_urun_sayisi == 0:
            # Her maksimum_urun_sayisi kadar ürün eklediğinizde yeni bir satıra geçin
            urun_frame = tk.Frame(urunler_inner_frame, bg="black")
            urun_frame.pack(side=tk.TOP, padx=20, pady=20)

        # Ürünleri yan yana sıralamak için pack yöntemini kullanıyoruz
        urun_satir_frame = tk.Frame(urun_frame, bg="black")
        urun_satir_frame.pack(side=tk.LEFT,pady=10,padx=20)

        # Ürünün resim dosyasının adını oluşturun
        resim_adi = f"{urun[1]}.jpg"
        resim_yolu = os.path.join(os.path.dirname(__file__), resim_adi)

        # Eğer resim dosyası mevcutsa, resmi yükle ve görüntüle
        if os.path.exists(resim_yolu):
            img = Image.open(resim_yolu)
            img = ImageTk.PhotoImage(img)
            resim_label = tk.Label(urun_satir_frame, image=img)
            resim_label.image = img
            resim_label.pack(padx=20, pady=20)
        else:
            # Resim dosyası bulunamazsa, varsayılan bir resmi kullanın
            varsayilan_resim = Image.open("zoccos.jpg")
            img = ImageTk.PhotoImage(varsayilan_resim)
            resim_label = tk.Label(urun_satir_frame, image=img)
            resim_label.image = img
            resim_label.pack(padx=20, pady=20)

        label = tk.Label(urun_satir_frame, text=f"{urun[1]} - {urun[4]} TL", font=("Arial", 16), fg="white", bg="black")
        label.pack()



        # "Sepete Ekle" düğmesi
        ekle_button = tk.Button(urun_satir_frame, text="Sepete Ekle",
                                command=lambda urun=urun: sepete_ekle(urun[1], urun[4]), fg="white", bg="dark green",
                                font=("Arial", 12))
        ekle_button.pack(pady=10)
        ekle_button.bind("<Enter>", lambda event, button=ekle_button: on_sepet_button_enter(event, button))
        ekle_button.bind("<Leave>", lambda event, button=ekle_button: on_sepet_button_leave(event, button))
    # Canvas'ın boyutlarını ayarlayın
    urunler_inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"), width=page_width, height=max_row_height)

root.mainloop()