import csv
import statistics
import matplotlib.pyplot as plt


class Ogrenci:
    """Bir öğrenciyi ve notlarını temsil eden sınıf."""

    def __init__(self, isim, vize, final, odev):
        self.isim = isim
        self.vize = vize
        self.final = final
        self.odev = odev

    def notlar(self):
        return [self.vize, self.final, self.odev]

    def ortalama(self):
        return statistics.mean(self.notlar())

    def gecti_mi(self, gecme_notu=50):
        return self.ortalama() >= gecme_notu

    def __repr__(self):
        return f"{self.isim} (Ort: {self.ortalama():.1f})"


def veri_oku(dosya_yolu):
    ogrenciler = []
    try:
        with open(dosya_yolu, mode="r", encoding="utf-8") as f:
            okuyucu = csv.DictReader(f)

            gerekli_sutunlar = {"isim", "vize", "final", "odev"}
            if okuyucu.fieldnames is None or not gerekli_sutunlar.issubset(set(okuyucu.fieldnames)):
                raise ValueError(
                    f"csv dosyasında gerekli sütunlar eksik. "
                    f"Gerekli sütunlar: {gerekli_sutunlar}"
                )

            for satir in okuyucu:
                ogrenci = Ogrenci(
                    isim=satir["isim"],
                    vize=float(satir["vize"]),
                    final=float(satir["final"]),
                    odev=float(satir["odev"]),
                )
                ogrenciler.append(ogrenci)

        if not ogrenciler:
            raise ValueError("csv dosyası boş")

    except FileNotFoundError:
        print(f"hata: {dosya_yolu} bulunamadı")
        return []
    except ValueError as hata:
        print(f"hata: {hata}")
        return []
    except KeyError as hata:
        print(f"hata: gerekli sütun eksik ({hata})")
        return []
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
        return []

    return ogrenciler


def sinif_istatistikleri(ogrenciler):
    try:
        if not ogrenciler:
            raise ValueError("istatistik hesaplamak için öğrenci verisi yok")

        tum_ortalamalar = [o.ortalama() for o in ogrenciler]

        # stdev en az 2 veri noktası ister, tek öğrenci varsa 0 kabul edelim
        standart_sapma = statistics.stdev(tum_ortalamalar) if len(tum_ortalamalar) > 1 else 0.0

        return {
            "ogrenci_sayisi": len(ogrenciler),
            "sinif_ortalamasi": statistics.mean(tum_ortalamalar),
            "medyan": statistics.median(tum_ortalamalar),
            "standart_sapma": standart_sapma,
            "en_yuksek": max(tum_ortalamalar),
            "en_dusuk": min(tum_ortalamalar),
        }
    except ValueError as hata:
        print(f"hata: {hata}")
        return None
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
        return None


def istatistikleri_yazdir(istatistikler):
    print("----- Sınıf İstatistikleri -----")
    print(f"Öğrenci sayısı   : {istatistikler['ogrenci_sayisi']}")
    print(f"Sınıf ortalaması : {istatistikler['sinif_ortalamasi']:.2f}")
    print(f"Medyan           : {istatistikler['medyan']:.2f}")
    print(f"Standart sapma   : {istatistikler['standart_sapma']:.2f}")
    print(f"En yüksek not    : {istatistikler['en_yuksek']:.2f}")
    print(f"En düşük not     : {istatistikler['en_dusuk']:.2f}")
    print()


def gecenleri_filtrele(ogrenciler, gecme_notu=50):
    return [o for o in ogrenciler if o.gecti_mi(gecme_notu)]


def kalanlari_filtrele(ogrenciler, gecme_notu=50):
    return [o for o in ogrenciler if not o.gecti_mi(gecme_notu)]


def basarili_ogrencileri_filtrele(ogrenciler, sinir=85):
    return [o for o in ogrenciler if o.ortalama() >= sinir]


def grafik_ciz(ogrenciler, dosya_adi="ogrenci_ortalamalari.png"):
    try:
        if not ogrenciler:
            raise ValueError("grafik çizmek için öğrenci verisi yok")

        isimler = [o.isim for o in ogrenciler]
        ortalamalar = [o.ortalama() for o in ogrenciler]
        renkler = ["#4CAF50" if o.gecti_mi() else "#F44336" for o in ogrenciler]

        plt.figure(figsize=(9, 5))
        plt.bar(isimler, ortalamalar, color=renkler)
        plt.axhline(y=50, color="gray", linestyle="--", label="Geçme notu (50)")
        plt.title("Öğrenci Not Ortalamaları")
        plt.xlabel("Öğrenci")
        plt.ylabel("Ortalama Not")
        plt.ylim(0, 100)
        plt.legend()
        plt.tight_layout()
        plt.savefig(dosya_adi)
        plt.close()
        print(f"Grafik kaydedildi: {dosya_adi}")
    except ValueError as hata:
        print(f"hata: {hata}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")


def main():
    ogrenciler = veri_oku("ogrenci_notlari.csv")

    if not ogrenciler:
        print("analiz durduruldu: geçerli öğrenci verisi bulunamadı")
        return

    print(f"{len(ogrenciler)} öğrenci verisi okundu.\n")

    istatistikler = sinif_istatistikleri(ogrenciler)
    if istatistikler is None:
        print("analiz durduruldu: istatistikler hesaplanamadı")
        return

    istatistikleri_yazdir(istatistikler)

    gecenler = gecenleri_filtrele(ogrenciler)
    kalanlar = kalanlari_filtrele(ogrenciler)
    basarililar = basarili_ogrencileri_filtrele(ogrenciler)

    print("----- Geçen Öğrenciler -----")
    for o in gecenler:
        print(f"  {o}")

    print("\n----- Kalan Öğrenciler -----")
    for o in kalanlar:
        print(f"  {o}")

    print("\n----- 85 Üzeri Başarılı Öğrenciler -----")
    for o in basarililar:
        print(f"  {o}")

    print()
    grafik_ciz(ogrenciler)


if __name__ == "__main__":
    main()