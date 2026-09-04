"""
geometri.py — CAD bağımsız yerleşim veri tipleri.

`Yerlestirme` ve `Boru` burada durur ki `dolap.py` / `gardirop.py`
build123d ve ezdxf KURULU OLMADAN da çalışsın: BOM, rapor, kontroller ve
testler saf Python'da koşar. `cizim.py` bu tipleri alıp katı modele çevirir.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Yerlestirme:
    """Bir parçanın 3B'deki konumu.

    İKİ eksen birden verilir — tek eksen belirsizdir ve parçayı 90° döndürür.

    konum      : parçanın MIN köşesinin (x, y, z) dünya koordinatı, mm
    eksen      : KALINLIĞIN oturduğu dünya ekseni — "x" | "y" | "z"
                 x = dikey yan panel · y = ön/arka panel · z = yatay tabla
    boy_ekseni : parçanın BOY (= desen yönü) ölçüsünün oturduğu eksen.
                 Kalan eksene otomatik olarak "en" gider.

    Örnekler:
      yan panel   eksen="x", boy_ekseni="z"   (boy = yükseklik, en = derinlik)
      raf/tabla   eksen="z", boy_ekseni="x"   (boy = genişlik, en = derinlik)
      kapak       eksen="y", boy_ekseni="z"   (boy = yükseklik, en = genişlik)
      arkalık     eksen="y", boy_ekseni="z"
    """
    kod: str
    konum: tuple[float, float, float]
    eksen: str = "z"
    boy_ekseni: str = "x"
    donus_x: float = 0.0        # derece — eğimli raf (arkaya doğru aşağı)
    donus_z: float = 0.0        # derece — devrilir kapak vb. için
    renk: str | None = None


@dataclass
class Boru:
    """Askı borusu / küpeşte gibi silindirik donanım.

    Levha parçası DEĞİLDİR — kesim listesine girmez, donanım listesine girer.

    eksen : borunun uzadığı dünya ekseni
            "y" = önden arkaya (SIĞ dolapta askı bu yönde olur)
            "x" = soldan sağa (normal derin gardırop askısı)
    konum : borunun BAŞLANGIÇ ucunun merkez koordinatı
    """
    kod: str
    ad: str
    cap: float                       # mm
    boy: float                       # mm
    konum: tuple[float, float, float]
    eksen: str = "x"
    renk: str = "#B8BCC0"            # krom
