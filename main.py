import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
import platform
import json
import os
import collections
from duckduckgo_search import DDGS  # DuckDuckGo için gerekli kütüphane

# --- VERİ SİSTEMİ ---
GECHMIS_DOSYASI = "zurna_data.json"


def verileri_yukle():
    if os.path.exists(GECHMIS_DOSYASI):
        with open(GECHMIS_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"gecmis": []}


def arama_kaydet(kelime):
    veri = verileri_yukle()
    veri["gecmis"].append(kelime)
    with open(GECHMIS_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False)
    trendleri_tazele()


def gecmisi_tamamen_sil():
    if os.path.exists(GECHMIS_DOSYASI):
        os.remove(GECHMIS_DOSYASI)
    trend_liste.delete(0, tk.END)
    messagebox.showinfo("Zurna Search", "Geçmiş ve trendler temizlendi!")


# --- AYARLAR PENCERESİ (SİYAH) ---
def ayarlar_penceresi_ac():
    ayarlar_p = tk.Toplevel(pencere)
    ayarlar_p.title("Zurna Ayarlar")
    ayarlar_p.geometry("350x250")
    ayarlar_p.configure(bg="#000000")

    tk.Label(ayarlar_p, text="⚙️ DÜRÜM AYARLARI", font=("Impact", 15), bg="#000000", fg="#e67e22").pack(pady=15)
    model_etiket = tk.Label(ayarlar_p, text="Cihaz Durumu: Bekleniyor...", fg="#555555", bg="#000000",
                            font=("Arial", 9))
    model_etiket.pack(pady=10)

    def cihaz_algila():
        model_etiket.config(text="🔍 Analiz ediliyor...", fg="#2980b9")
        ayarlar_p.update()
        ayarlar_p.after(1000)
        cihaz = f"{platform.system()} {platform.machine()}"
        model_etiket.config(text=f"✅ Cihaz: {cihaz}", fg="#27ae60", font=("Arial", 9, "bold"))

    tk.Button(ayarlar_p, text="CIHAZ MODELİNİ ALGILA", command=cihaz_algila,
              bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=15).pack(pady=10)

    tk.Button(ayarlar_p, text="GEÇMİŞİ SİL", command=gecmisi_tamamen_sil,
              bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=20).pack(pady=10)


# --- DUCKDUCKGO ARAMA MOTORU (ENGEL TANIMAZ) ---
link_listesi = []


def arama_yap():
    global link_listesi
    k = entry_arama.get()
    if not k: return

    arama_kaydet(k)
    text_alani.delete(1.0, tk.END)
    link_listesi = []
    text_alani.insert(tk.END, f"🌯ARANIYOR...\n\n", "baslik")

    try:
        # DuckDuckGo üzerinden bot engeline takılmadan arama yapıyoruz
        with DDGS() as ddgs:
            results = ddgs.text(k, region='tr-tr', safesearch='off', timelimit='y')
            count = 0
            for r in results:
                if count >= 10: break
                title = r.get('title')
                link = r.get('href')
                if title and link:
                    link_listesi.append(link)
                    text_alani.insert(tk.END, f"🔗 {title}\n", "link")
                    text_alani.insert(tk.END, f"{link[:60]}...\n\n", "adres")
                    count += 1
    except Exception as e:
        messagebox.showerror("Hata", "Arama yapılamadı, internetini kontrol et!")


# --- OYUN, LİNK VE TREND FONKSİYONLARI ---
def linki_ac(e):
    try:
        idx = text_alani.index(tk.CURRENT)
        line = int(idx.split('.')[0])
        # Başlık ve adres satırlarını hesaba katarak linki buluyoruz
        ln = (line - 3) // 3
        if 0 <= ln < len(link_listesi):
            webbrowser.open(link_listesi[ln])
    except:
        pass


def trendleri_tazele():
    veri = verileri_yukle()
    gecmis = veri.get("gecmis", [])
    en_coklar = collections.Counter(gecmis).most_common(5)
    trend_liste.delete(0, tk.END)
    for kelime, adet in en_coklar:
        trend_liste.insert(tk.END, f"🌯 {kelime} ({adet})")


# --- GÜLEN DÜRÜM OYUNU ---
def dino_oyunu_ac():
    oyun_p = tk.Toplevel(pencere)
    oyun_p.title("Zurna Koşu")
    oyun_p.geometry("600x300")
    canvas = tk.Canvas(oyun_p, width=600, height=220, bg="#111111", highlightthickness=0)
    canvas.pack()
    govde = canvas.create_rectangle(50, 140, 85, 185, fill="#f1c40f", outline="#e67e22", width=2)
    goz1 = canvas.create_oval(58, 148, 62, 154, fill="black");
    goz2 = canvas.create_oval(73, 148, 77, 154, fill="black")
    agiz = canvas.create_arc(58, 155, 77, 175, start=0, extent=-180, style="arc", width=2, outline="black")
    sol_kol = canvas.create_line(50, 160, 35, 170, width=2, fill="white");
    sag_kol = canvas.create_line(85, 160, 100, 170, width=2, fill="white")
    sol_bacak = canvas.create_line(60, 185, 60, 200, width=3, fill="white");
    sag_bacak = canvas.create_line(75, 185, 75, 200, width=3, fill="white")
    parcalar = [govde, goz1, goz2, agiz, sol_kol, sag_kol, sol_bacak, sag_bacak]
    engel = canvas.create_rectangle(600, 160, 630, 190, fill="#ff4d4d")
    v = {"zipliyor": False, "aktif": True, "adim": 0}

    def zipla(e):
        if not v["zipliyor"] and v["aktif"]:
            v["zipliyor"] = True
            for _ in range(12):
                for p in parcalar: canvas.move(p, 0, -10)
                oyun_p.update();
                oyun_p.after(10)
            for _ in range(12):
                for p in parcalar: canvas.move(p, 0, 10)
                oyun_p.update();
                oyun_p.after(10)
            v["zipliyor"] = False

    def hareket():
        if not v["aktif"]: return
        v["adim"] += 1
        if not v["zipliyor"]:
            if v["adim"] % 8 < 4:
                canvas.coords(sol_bacak, 60, 185, 60, 205);
                canvas.coords(sag_bacak, 75, 185, 75, 190)
            else:
                canvas.coords(sol_bacak, 60, 185, 60, 190);
                canvas.coords(sag_bacak, 75, 185, 75, 205)
        canvas.move(engel, -10, 0)
        if canvas.coords(engel)[2] < 0: canvas.coords(engel, 600, 160, 630, 190)
        if canvas.find_overlapping(*canvas.coords(govde)):
            if engel in canvas.find_overlapping(*canvas.coords(govde)):
                v["aktif"] = False;
                oyun_p.destroy()
        oyun_p.after(25, hareket)

    oyun_p.bind("<space>", zipla);
    hareket()


# --- ANA PENCERE ---
pencere = tk.Tk()
pencere.title("Zurna Search: Ghost Edition")
pencere.geometry("1000x750")
pencere.configure(bg="#000000")

sag_frame = tk.Frame(pencere, bg="#000000", width=250, highlightthickness=1, highlightbackground="#333333")
sag_frame.pack(side="right", fill="y", padx=5)
tk.Label(sag_frame, text="ESKİ DÜRÜMLER", fg="#f1c40f", bg="#000000", font=("Impact", 12)).pack(pady=15)
trend_liste = tk.Listbox(sag_frame, bg="#000000", fg="#ffffff", bd=0, font=("Arial", 9, "bold"),
                         selectbackground="#e67e22", highlightthickness=0)
trend_liste.pack(fill="both", expand=True, padx=10, pady=10)
tk.Button(sag_frame, text="⚙️ DÜRÜM AYARLARI", command=ayarlar_penceresi_ac, bg="#333333", fg="white",
          font=("Arial", 10, "bold"), relief="flat").pack(fill="x", pady=15, padx=10)

sol_frame = tk.Frame(pencere, bg="#000000")
sol_frame.pack(side="left", fill="both", expand=True)
baslik_f = tk.Frame(sol_frame, bg="#000000")
baslik_f.pack(pady=25)
tk.Label(baslik_f, text="🌯 ZURNA SEARCH 🌯", font=("Impact", 45), fg="#e67e22", bg="#000000").pack(side="left")
tk.Button(baslik_f, text="z", command=dino_oyunu_ac, bg="#000000", fg="#111111", relief="flat", bd=0).pack(side="left",
                                                                                                           padx=5)

entry_arama = tk.Entry(sol_frame, width=35, font=("Arial", 18), justify="center", bg="#1a1a1a", fg="white",
                       insertbackground="white", bd=0)
entry_arama.pack(pady=15)
entry_arama.bind('<Return>', lambda e: arama_yap())
tk.Button(sol_frame, text="KANKİ DÜRÜM NEYLİ OLSUN", command=arama_yap, bg="#e67e22", fg="white", font=("Arial", 11, "bold"),
          relief="flat", padx=25).pack(pady=10)

text_alani = scrolledtext.ScrolledText(sol_frame, width=65, height=20, bg="#0a0a0a", fg="#ffffff", font=("Arial", 10),
                                       bd=0, highlightthickness=1, highlightbackground="#333333")
text_alani.pack(pady=20)
text_alani.tag_config("baslik", foreground="#f1c40f", font=("Arial", 12, "bold"))
text_alani.tag_config("link", foreground="#3498db", underline=True, font=("Arial", 10, "bold"))
#test hihihih
text_alani.tag_config("adres", foreground="#555555", font=("Arial", 8))
text_alani.tag_bind("link", "<Button-1>", linki_ac)

trendleri_tazele()

pencere.mainloop()
