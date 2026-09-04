"""
render.py — Blender 5.2 LTS içinde çalışan render/materyal/texture katmanı.

Çalıştırma (headless):
    /Applications/Blender.app/Contents/MacOS/Blender -b \
        --python render.py -- --glb cikti/AYK-01.glb --out cikti/render

Bu dosya Blender'ın KENDİ python'unda çalışır (3.13) — mobilya-venv ile
alakası yoktur, build123d/ezdxf import ETMEZ.

BLENDER 5.x TUZAKLARI (hepsi 5.2.0 binary'sinde denendi):
  • 'BLENDER_EEVEE_NEXT' YOK — doğru ad 'BLENDER_EEVEE'.
  • scene.cycles.feature_set KALDIRILDI (5.2).
  • scene.node_tree KALDIRILDI -> scene.compositing_node_group.
  • ShaderNodeTexMusgrave KALDIRILDI -> TexNoise.noise_type.
  • Tüm 'Fac' soketleri 'Factor' oldu.
  • Material.use_nodes DEPRECATED — node_tree zaten hazır gelir, dokunma.
  • image_settings.media_type, file_format'TAN ÖNCE set edilmeli.
  • macOS'ta compute_device_type sadece 'NONE'|'METAL'; denoiser sadece
    'OPENIMAGEDENOISE' (OPTIX NVIDIA'ya özel, TypeError verir).
  • default_value DAİMA scene-linear'dır — sRGB rengi s2l() ile çevir.
  • İlk render'da Metal kernel derlemesi ~60-90 sn sürer, sonra ~1 sn.
"""

import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

# ---------------------------------------------------------------------------
# 0. YARDIMCILAR
# ---------------------------------------------------------------------------

def s2l(c: float) -> float:
    """sRGB 0-1 -> scene-linear. Renk atarken ZORUNLU."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def L(rgb) -> tuple:
    return tuple(s2l(c) for c in rgb) + (1.0,)


def sok(node, *adlar, cikis=False):
    """Sürüm-güvenli soket bulucu: yeni ad önce, eski ad yedek."""
    kol = node.outputs if cikis else node.inputs
    for a in adlar:
        s = kol.get(a)
        if s is not None:
            return s
    raise KeyError(f"{node.bl_idname}: {adlar} yok — mevcut: "
                   f"{[x.name for x in kol]}")


def temizle():
    """Sahneyi tamamen boşalt."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'


# ---------------------------------------------------------------------------
# 1. MODEL ALIMI
# ---------------------------------------------------------------------------

def glb_al(yol: str, hedef_yukseklik_m: float | None = None):
    """build123d GLB'sini alır ve METRE ölçeğinde olduğundan emin olur.

    build123d export_gltf(unit=Unit.MM) glTF sözleşmesine uyar ve METRE
    yazar — yani ek ölçekleme GEREKMEZ. Ama başka bir araçtan gelen
    mm-birimli GLB de olabileceği için ölçek ÖLÇÜLEREK belirlenir:
    mobilya 10 m'den büyük görünüyorsa dosya mm'dir, 0.001 uygulanır.
    """
    bpy.ops.import_scene.gltf(filepath=yol)
    nesneler = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if not nesneler:
        raise RuntimeError(f"{yol} içinde mesh yok")

    kok = [o for o in bpy.context.scene.objects if o.parent is None]
    mn, mx = sinir_kutusu(nesneler)
    if (mx - mn).length > 10.0:          # 10 m'den büyük -> dosya mm birimli
        print("[model] mm birimli GLB algılandı, 0.001 ölçek uygulanıyor")
        for o in kok:
            o.scale = (0.001, 0.001, 0.001)
        bpy.context.view_layer.update()
        bpy.ops.object.select_all(action='DESELECT')
        for o in kok:
            o.select_set(True)
        bpy.context.view_layer.objects.active = kok[0]
        bpy.ops.object.transform_apply(location=False, rotation=False,
                                       scale=True)

    # Tabanı Z=0'a otur
    mn, mx = sinir_kutusu(nesneler)
    for o in kok:
        o.location.z -= mn.z
    bpy.context.view_layer.update()

    mn, mx = sinir_kutusu(nesneler)
    boyut = mx - mn
    print(f"[model] {len(nesneler)} parça · "
          f"{boyut.x*1000:.0f} x {boyut.y*1000:.0f} x {boyut.z*1000:.0f} mm")
    if hedef_yukseklik_m and abs(boyut.z - hedef_yukseklik_m) > 0.01:
        print(f"[UYARI] beklenen yükseklik {hedef_yukseklik_m*1000:.0f} mm, "
              f"gelen {boyut.z*1000:.0f} mm — ölçek kontrolü gerekli")
    return nesneler


def sinir_kutusu(nesneler):
    dep = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in nesneler:
        ev = o.evaluated_get(dep)
        for c in ev.bound_box:
            pts.append(ev.matrix_world @ Vector(c))
    mn = Vector((min(p[i] for p in pts) for i in range(3)))
    mx = Vector((max(p[i] for p in pts) for i in range(3)))
    return mn, mx


def _dondur(nesne, pivot, eksen: str, derece: float):
    """Nesneyi dünya uzayında verilen pivot noktası etrafında döndürür."""
    import mathutils
    R = mathutils.Matrix.Rotation(math.radians(derece), 4, eksen)
    T1 = mathutils.Matrix.Translation(-pivot)
    T2 = mathutils.Matrix.Translation(pivot)
    nesne.matrix_world = T2 @ R @ T1 @ nesne.matrix_world


def kapaklari_ac(nesneler, menteseli: float = 105.0, devrilir: float = 50.0):
    """Kapakları menteşe/pivot ekseninde açar — iç düzeni gösteren görsel için.

    Menteşeli kapak : sol düşey kenarda (min X) Z ekseni etrafında döner.
    Devrilir kapak  : alt kenarda X ekseni etrafında öne devrilir.
    Ayna kapak da menteşeli sayılır.
    """
    import re
    from mathutils import Vector

    def bolge_etiketi(ad):
        m = re.search(r"\(([^)]*)\)", ad)
        return m.group(1).strip().lower() if m else None

    # Devrilir mekanizmanın ara rafı gövdeye değil KAPAĞA bağlıdır —
    # kapakla birlikte dönmeli. Bölge etiketinden eşleştirilir.
    mek_raflar = {}
    for o in nesneler:
        if "MEKANIZMA" in o.name.upper() or "MEKANİZMA" in o.name.upper():
            mek_raflar.setdefault(bolge_etiketi(o.name), []).append(o)

    # Gövdenin (kapak olmayan parçaların) X merkezi — menteşe tarafını
    # buna göre seçiyoruz ki kapaklar DIŞA, karşılıklı açılsın.
    govde = [o for o in nesneler if "KAPAK" not in o.name.upper()]
    if govde:
        gmn, gmx = sinir_kutusu(govde)
        merkez_x = (gmn.x + gmx.x) / 2.0
    else:
        merkez_x = 0.0

    acilan = []
    for o in nesneler:
        ad = o.name.upper()
        if "KAPAK" not in ad:
            continue
        mn, mx = sinir_kutusu([o])
        if "DEVRILIR" in ad or "DEVRİLİR" in ad:
            # alt-ön kenar: pivot y = ön yüz, z = alt kenar
            pivot = Vector((0.0, mn.y, mn.z))
            _dondur(o, pivot, 'X', devrilir)
            for raf in mek_raflar.get(bolge_etiketi(o.name), []):
                _dondur(raf, pivot, 'X', devrilir)
            acilan.append((o.name, "devrilir", devrilir))
        else:
            # Kapağın merkezi gövde merkezinin solundaysa SOL kenardan,
            # sağındaysa SAĞ kenardan menteşelenir. Tek kapakta varsayılan
            # sol menteşedir (kapak merkezi gövde merkeziyle çakışır).
            kapak_x = (mn.x + mx.x) / 2.0
            if kapak_x > merkez_x + 1e-4:
                _dondur(o, Vector((mx.x, mx.y, 0.0)), 'Z', menteseli)
                acilan.append((o.name, "sağ menteşe", menteseli))
            else:
                _dondur(o, Vector((mn.x, mx.y, 0.0)), 'Z', -menteseli)
                acilan.append((o.name, "sol menteşe", -menteseli))
    for ad, tur, aci in acilan:
        print(f"[kapak] {ad} -> {tur} {aci:+.0f}°")
    print(f"[kapak] {len(acilan)} kapak açıldı")
    return acilan


# ---------------------------------------------------------------------------
# 2. UV — panel mobilyada operatör DEĞİL, veri seviyesi
# ---------------------------------------------------------------------------

def kutu_uv(nesne, desen: str = "Z", yogunluk: float = 1.0):
    """Dünya-eksenli düzlemsel UV. 1 UV birimi = 1/yogunluk metre.

    bpy.ops.uv.* yerine doğrudan UV yazar: mod değiştirmez, deterministiktir
    ve desen yönünü parça bazında kontrol etmeyi sağlar.

    desen: dokunun U ekseninin hangi dünya eksenine oturacağı.
           "Z" -> desen dikey akar (yan panel, kapak)
           "X" -> desen yatay akar (raf, tabla)
    """
    me = nesne.data
    uv = me.uv_layers.get("UVMap") or me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        n = poly.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if ax == 0:      u, v = co.y, co.z      # X'e bakan yüz -> YZ
            elif ax == 1:    u, v = co.x, co.z      # Y'ye bakan yüz -> XZ
            else:            u, v = co.x, co.y      # Z'ye bakan yüz -> XY
            if desen == "X":
                u, v = v, u
            uv.data[li].uv = (u * yogunluk, v * yogunluk)
    return uv


# ---------------------------------------------------------------------------
# 3. MATERYALLER
# ---------------------------------------------------------------------------

AHSAP_PALET = {
    # (erken halka, geç halka, aksan) — sRGB 0-1
    "mese":   ((0.46, 0.33, 0.20), (0.60, 0.45, 0.29), (0.66, 0.51, 0.34)),
    "ceviz":  ((0.22, 0.14, 0.09), (0.34, 0.23, 0.16), (0.42, 0.30, 0.21)),
    "kayin":  ((0.66, 0.53, 0.39), (0.76, 0.64, 0.49), (0.82, 0.71, 0.57)),
    "antrasit": ((0.13, 0.13, 0.14), (0.17, 0.17, 0.18), (0.20, 0.20, 0.21)),
}

MELAMIN_DUZ = {
    "beyaz":    (0.92, 0.915, 0.905),
    "kirik_beyaz": (0.90, 0.88, 0.84),
    "antrasit": (0.16, 0.16, 0.17),
    "gri":      (0.55, 0.55, 0.55),
    "krem":     (0.87, 0.82, 0.72),
}


def _yeni_mat(ad: str):
    """5.x'te node_tree hazır gelir; use_nodes'a dokunma (deprecated)."""
    mat = bpy.data.materials.new(ad)
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    out = nt.nodes["Material Output"]
    return mat, nt, bsdf, out


def melamin(ad: str, renk="beyaz", parlaklik: float = 0.30,
            lak: float = 0.04):
    """Düz renk melamin. Katalog rengi tutması gereken yüzey için."""
    rgb = MELAMIN_DUZ.get(renk, renk) if isinstance(renk, str) else renk
    mat, nt, bsdf, out = _yeni_mat(ad)
    bsdf.inputs["Base Color"].default_value = L(rgb)
    bsdf.inputs["Roughness"].default_value = parlaklik
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["IOR"].default_value = 1.5
    bsdf.inputs["Coat Weight"].default_value = lak
    bsdf.inputs["Coat Roughness"].default_value = 0.25
    return mat


def ayna(ad: str = "Ayna"):
    """Ayna kapak yüzeyi. Cam + gümüş sırt yerine tek katman metal —
    panel mobilyada fark edilmez, örnekleme çok daha ucuzdur."""
    mat, nt, bsdf, out = _yeni_mat(ad)
    bsdf.inputs["Base Color"].default_value = L((0.95, 0.96, 0.97))
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.02
    return mat


def ahsap_prosedurel(ad: str, tur: str = "mese", desen_ekseni: str = "V",
                     halka_araligi_m: float = 0.13,
                     desen_uzunlugu_m: float = 2.0,
                     parlaklik: float = 0.36, kabartma: float = 0.30):
    """Doku dosyası olmadan ahşap desen. Musgrave YOK — TexNoise + TexWave.

    Kritik nokta: kıvrımı Wave'in kendi Distortion'ıyla değil, KOORDİNATI
    Wave'den ÖNCE bozarak yap. Distortion düzenli dalga verir; koordinat
    bozma katedral deseni verir. Wave.Detail=0 olmalı — üstü oluklu mukavva
    görüntüsü yapar.
    """
    erken, gec, aksan = AHSAP_PALET.get(tur, AHSAP_PALET["mese"])
    mat, nt, bsdf, out = _yeni_mat(ad)
    n, lnk = nt.nodes, nt.links

    tc = n.new("ShaderNodeTexCoord"); tc.location = (-1600, 0)
    mp = n.new("ShaderNodeMapping");  mp.location = (-1400, 0)
    mp.vector_type = 'POINT'
    dik, boyunca = 1.0 / halka_araligi_m, 1.0 / desen_uzunlugu_m
    if desen_ekseni == "V":
        mp.inputs["Scale"].default_value = (dik, boyunca, dik); bant = 'X'
    else:
        mp.inputs["Scale"].default_value = (boyunca, dik, dik); bant = 'Y'
    lnk.new(tc.outputs["UV"], mp.inputs["Vector"])

    # Parça başına rastgele kaydırma — komşu paneller aynı deseni tekrarlamasın
    oi = n.new("ShaderNodeObjectInfo");  oi.location = (-1900, -420)
    cb = n.new("ShaderNodeCombineXYZ");  cb.location = (-1780, -560)
    sc = n.new("ShaderNodeVectorMath");  sc.location = (-1620, -560)
    sc.operation = 'SCALE'; sc.inputs["Scale"].default_value = 37.0
    lnk.new(oi.outputs["Random"], cb.inputs["X"])
    lnk.new(oi.outputs["Random"], cb.inputs["Y"])
    lnk.new(cb.outputs["Vector"], sc.inputs[0])
    lnk.new(sc.outputs["Vector"], mp.inputs["Location"])

    # Koordinat bozma — KENDİ mapping'i olmalı.
    # Bozma gürültüsü halka ekseninde YAVAŞ, lif ekseninde HIZLI değişmeli;
    # aynı mapping'i paylaşırsa bozma yatayda ortalanır ve panel oluklu
    # mukavvaya benzer (ilk denemede tam bunu verdi).
    wm = n.new("ShaderNodeMapping"); wm.location = (-1350, -320)
    wm.vector_type = 'POINT'
    wm.inputs["Scale"].default_value = ((0.9, 2.2, 0.9)
                                        if desen_ekseni == "V"
                                        else (2.2, 0.9, 0.9))
    lnk.new(tc.outputs["UV"], wm.inputs["Vector"])

    wn = n.new("ShaderNodeTexNoise"); wn.location = (-1150, -320)
    wn.noise_dimensions = '3D'; wn.noise_type = 'FBM'; wn.normalize = True
    wn.inputs["Scale"].default_value = 0.8
    wn.inputs["Detail"].default_value = 5.0
    wn.inputs["Roughness"].default_value = 0.5
    lnk.new(wm.outputs["Vector"], wn.inputs["Vector"])

    sub = n.new("ShaderNodeVectorMath"); sub.location = (-930, -320)
    sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (.5, .5, .5)
    lnk.new(wn.outputs["Color"], sub.inputs[0])
    scl = n.new("ShaderNodeVectorMath"); scl.location = (-760, -320)
    scl.operation = 'SCALE'; scl.inputs["Scale"].default_value = 1.15
    lnk.new(sub.outputs["Vector"], scl.inputs[0])
    add = n.new("ShaderNodeVectorMath"); add.location = (-600, 0)
    add.operation = 'ADD'
    lnk.new(mp.outputs["Vector"], add.inputs[0])
    lnk.new(scl.outputs["Vector"], add.inputs[1])

    wave = n.new("ShaderNodeTexWave"); wave.location = (-400, 0)
    wave.wave_type = 'BANDS'; wave.bands_direction = bant
    wave.wave_profile = 'SIN'
    wave.inputs["Scale"].default_value = 1.0
    wave.inputs["Distortion"].default_value = 0.0
    wave.inputs["Detail"].default_value = 0.0
    lnk.new(add.outputs["Vector"], wave.inputs["Vector"])

    ramp = n.new("ShaderNodeValToRGB"); ramp.location = (-150, 0)
    cr = ramp.color_ramp; cr.interpolation = 'B_SPLINE'
    cr.elements[0].position = 0.02; cr.elements[0].color = L(erken)
    cr.elements[1].position = 0.50; cr.elements[1].color = L(gec)
    cr.elements.new(0.93).color = L(aksan)
    lnk.new(sok(wave, "Factor", "Fac", cikis=True), sok(ramp, "Factor", "Fac"))

    # Lif dokusu (çok uzatılmış gürültü)
    fm = n.new("ShaderNodeMapping"); fm.location = (-1150, -700)
    fm.vector_type = 'POINT'
    fpm = 1200.0
    fm.inputs["Scale"].default_value = ((fpm, fpm / 200.0, 1.0)
                                        if desen_ekseni == "V"
                                        else (fpm / 200.0, fpm, 1.0))
    lnk.new(tc.outputs["UV"], fm.inputs["Vector"])
    fib = n.new("ShaderNodeTexNoise"); fib.location = (-930, -700)
    fib.noise_dimensions = '2D'; fib.noise_type = 'FBM'; fib.normalize = True
    fib.inputs["Detail"].default_value = 5.0
    lnk.new(fm.outputs["Vector"], fib.inputs["Vector"])

    mix = n.new("ShaderNodeMix"); mix.location = (150, 0)
    mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
    mix.inputs["Factor"].default_value = 0.14
    lnk.new(ramp.outputs["Color"], mix.inputs[6])    # A (RGBA)
    lnk.new(fib.outputs["Color"], mix.inputs[7])     # B (RGBA)
    lnk.new(mix.outputs[2], bsdf.inputs["Base Color"])   # Result (RGBA)

    rr = n.new("ShaderNodeMapRange"); rr.location = (500, -350)
    rr.inputs["To Min"].default_value = parlaklik - 0.06
    rr.inputs["To Max"].default_value = parlaklik + 0.06
    lnk.new(sok(wave, "Factor", "Fac", cikis=True), rr.inputs["Value"])
    lnk.new(rr.outputs["Result"], bsdf.inputs["Roughness"])

    bmp = n.new("ShaderNodeBump"); bmp.location = (800, -550)
    bmp.inputs["Strength"].default_value = kabartma
    bmp.inputs["Distance"].default_value = 0.0010
    lnk.new(sok(fib, "Factor", "Fac", cikis=True), bmp.inputs["Height"])
    lnk.new(bmp.outputs["Normal"], bsdf.inputs["Normal"])

    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["IOR"].default_value = 1.5
    bsdf.inputs["Coat Weight"].default_value = 0.05
    bsdf.inputs["Coat Roughness"].default_value = 0.28
    return mat


def pbr_dokulu(ad: str, klasor: str, doku_boyu_m: float = 1.0,
               desen_donus: float = 0.0, normal_gucu: float = 1.0):
    """ambientCG / Poly Haven indirilmiş doku klasöründen PBR materyal.

    Renk haritası 'sRGB', diğer HEPSİ 'Non-Color' olmalı.
    ('Raw' ve 'Linear' 4.0'da KALDIRILDI — kullanırsan TypeError.)
    """
    import glob
    ekler = {
        "renk":   ["_diff_", "_col_", "_color", "_albedo", "_basecolor"],
        "puruz":  ["_rough_", "_roughness"],
        "normal": ["_nor_gl_", "_normalgl", "_normal_gl"],
    }
    bulunan = {}
    for f in sorted(glob.glob(os.path.join(klasor, "*"))):
        alt = os.path.basename(f).lower()
        if not alt.endswith((".jpg", ".jpeg", ".png", ".exr")):
            continue
        for k, sfx in ekler.items():
            if any(s in alt for s in sfx):
                bulunan.setdefault(k, f)
    if "renk" not in bulunan:
        raise FileNotFoundError(f"{klasor} içinde renk haritası yok")

    mat, nt, bsdf, out = _yeni_mat(ad)
    n, lnk = nt.nodes, nt.links
    tc = n.new("ShaderNodeTexCoord"); tc.location = (-1100, 0)
    mp = n.new("ShaderNodeMapping");  mp.location = (-900, 0)
    mp.vector_type = 'POINT'
    s = 1.0 / doku_boyu_m
    mp.inputs["Scale"].default_value = (s, s, s)
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(desen_donus))
    lnk.new(tc.outputs["UV"], mp.inputs["Vector"])

    def doku(yol, uzay, y):
        t = n.new("ShaderNodeTexImage"); t.location = (-650, y)
        img = bpy.data.images.load(yol, check_existing=True)
        img.colorspace_settings.name = uzay
        t.image = img
        t.extension = 'REPEAT'
        lnk.new(mp.outputs["Vector"], t.inputs["Vector"])
        return t

    lnk.new(doku(bulunan["renk"], 'sRGB', 300).outputs["Color"],
            bsdf.inputs["Base Color"])
    if "puruz" in bulunan:
        lnk.new(doku(bulunan["puruz"], 'Non-Color', 0).outputs["Color"],
                bsdf.inputs["Roughness"])
    if "normal" in bulunan:
        nrm = doku(bulunan["normal"], 'Non-Color', -350)
        nm = n.new("ShaderNodeNormalMap"); nm.location = (-300, -350)
        nm.space = 'TANGENT'
        nm.inputs["Strength"].default_value = normal_gucu
        lnk.new(nrm.outputs["Color"], nm.inputs["Color"])
        lnk.new(nm.outputs["Normal"], bsdf.inputs["Normal"])

    bsdf.inputs["Coat Weight"].default_value = 0.05
    return mat


def bant_ata(nesne, govde_mat, bant_mat, kalinlik_ekseni: str = "z"):
    """Kenar bandını AYRI GEOMETRİ değil, 2. materyal slotu olarak uygula.

    Yan yüzler (kalınlık yüzeyleri) slot 1'e atanır. Parça yeniden
    boyutlandığında bozulmaz, glTF/USDZ'ye doğru gider, bant rengi dekordan
    bağımsız değiştirilebilir — gerçek hayatta da ayrı SKU'durlar.
    """
    import bmesh
    me = nesne.data
    me.materials.clear()
    me.materials.append(govde_mat)
    me.materials.append(bant_mat)
    ekseni = {"x": 0, "y": 1, "z": 2}[kalinlik_ekseni]
    bm = bmesh.new(); bm.from_mesh(me)
    for f in bm.faces:
        f.material_index = 0 if abs(f.normal[ekseni]) > 0.5 else 1
    bm.to_mesh(me); bm.free()


def pah(nesne, genislik_mm: float = 0.5):
    """Panel kenarına küçük pah — ışığı yakalar, plastik görüntüyü kırar."""
    b = nesne.modifiers.new("Pah", 'BEVEL')
    b.width = genislik_mm / 1000.0
    b.segments = 2
    b.limit_method = 'ANGLE'
    b.angle_limit = math.radians(30)
    b.harden_normals = False
    return b


# ---------------------------------------------------------------------------
# 4. IŞIK · KAMERA · DÜNYA
# ---------------------------------------------------------------------------

def alan_isigi(ad, konum, hedef, gen, yuk, guc, kelvin):
    ld = bpy.data.lights.new(ad, type='AREA')
    ld.shape = 'RECTANGLE'
    ld.size, ld.size_y = gen, yuk
    ld.energy = guc
    ld.use_temperature = True
    ld.temperature = kelvin
    ob = bpy.data.objects.new(ad, ld)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = konum
    ob.rotation_euler = (Vector(hedef) - Vector(konum)).to_track_quat(
        '-Z', 'Y').to_euler()
    ob.visible_camera = False     # softbox kadraja/yansımaya girmesin
    return ob


def studyo(yukseklik_m: float = 1.0, anahtar_w: float = 110.0):
    """Kalibre 3 nokta softbox.

    Güç ölçülerek bulundu: ~1 m yüksek nesne için 100-110 W anahtar ışık
    doğru pozu verir. 500 W albedo'yu patlatır, desen kaybolur.
    """
    hedef = (0, 0, yukseklik_m * 0.55)
    k = yukseklik_m
    alan_isigi("Anahtar", (-1.6 * k, -1.9 * k, 2.1 * k), hedef,
               1.8, 1.8, anahtar_w, 5600)
    alan_isigi("Dolgu", (2.0 * k, -1.4 * k, 1.2 * k), hedef,
               2.2, 2.2, anahtar_w * 0.41, 5200)
    alan_isigi("Kontur", (1.1 * k, 2.0 * k, 2.0 * k), hedef,
               1.0, 1.6, anahtar_w * 0.64, 6200)


def hdri_dunya(yol: str, guc: float = 1.0, donus: float = 0.0,
               kamerada_gorunsun: bool = False):
    w = bpy.data.worlds.new("HDRI")
    bpy.context.scene.world = w
    nt = w.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_WORLD':
            nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = guc
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    img = bpy.data.images.load(yol, check_existing=True)
    img.colorspace_settings.name = 'Linear Rec.709'
    env.image = img
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(donus))
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    w.cycles_visibility.camera = kamerada_gorunsun
    return w


def notr_dunya(parlaklik: float = 0.45):
    """HDRI yokken nötr gri ortam. Kameraya görünmez ama YANSIR —
    aynalı/parlak yüzeyler boşluğu yansıtıp simsiyah çıkmasın diye."""
    w = bpy.data.worlds.new("Notr")
    bpy.context.scene.world = w
    nt = w.node_tree
    bg = [n for n in nt.nodes if n.type == 'BACKGROUND'][0]
    bg.inputs["Color"].default_value = L((parlaklik,) * 3)
    bg.inputs["Strength"].default_value = 1.0
    w.cycles_visibility.camera = False
    return w


def zemin(golge_yakalayici: bool = True, boyut: float = 20.0):
    bpy.ops.mesh.primitive_plane_add(size=boyut, location=(0, 0, 0))
    z = bpy.context.object
    z.name = "Zemin"
    z.is_shadow_catcher = golge_yakalayici   # Cycles'a özel
    return z


def kamera(nesneler, azimut: float = 35.0, yukselis: float = 12.0,
           odak: float = 85.0, pay: float = 1.06):
    """Ürün fotoğrafı konvansiyonu: 85 mm, 3/4 açı.

    35 mm panel kenarlarını fıçılaştırır, kutu formda derinliği abartır.
    85-105 mm kenarları paralel tutar.

    KADRAJ: sınır KÜRESİNE göre değil, sınır kutusunun 8 KÖŞESİNE göre
    hesaplanır. Küre yaklaşımı uzun-ince gövdede ve sert açılarda (alttan
    bakış, üstten bakış) yetersiz mesafe verir ve cismin bir kısmı kadraj
    dışında kalır. Burada her köşe için gereken mesafe kapalı formülle
    çözülüp en büyüğü alınır — her açıda tam sığar.
    """
    cd = bpy.data.cameras.new("Kamera")
    cd.lens = odak
    cam = bpy.data.objects.new("Kamera", cd)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam

    mn, mx = sinir_kutusu(nesneler)
    merkez = (mn + mx) * 0.5

    az, el = math.radians(azimut), math.radians(yukselis)
    d = Vector((math.sin(az) * math.cos(el),
                -math.cos(az) * math.cos(el), math.sin(el)))
    d.normalize()

    # Kamera ekseni: f = bakış (kameradan cisme), r = sağ, u = yukarı
    f = -d
    dunya_ust = Vector((0.0, 0.0, 1.0))
    if abs(f.dot(dunya_ust)) > 0.999:          # tepeden/alttan bakış
        dunya_ust = Vector((0.0, 1.0, 0.0))
    r = f.cross(dunya_ust).normalized()
    u = r.cross(f).normalized()

    sc = bpy.context.scene
    rx, ry = sc.render.resolution_x, sc.render.resolution_y
    if ry > rx:
        sw, sh = cd.sensor_width * rx / ry, cd.sensor_width
    else:
        sw, sh = cd.sensor_width, cd.sensor_width * ry / rx
    tan_h = (sw / (2 * cd.lens)) / pay
    tan_v = (sh / (2 * cd.lens)) / pay

    # Her köşe için: |p·r| <= (p·f + mesafe)·tan_h  ve  |p·u| <= (...)·tan_v
    #   -> mesafe >= |p·r|/tan_h - p·f        (u için de aynısı)
    mesafe = 0.0
    yaricap = 0.0
    for i in range(8):
        p = Vector((mx.x if i & 1 else mn.x,
                    mx.y if i & 2 else mn.y,
                    mx.z if i & 4 else mn.z)) - merkez
        yaricap = max(yaricap, p.length)
        pf = p.dot(f)
        mesafe = max(mesafe,
                     abs(p.dot(r)) / tan_h - pf,
                     abs(p.dot(u)) / tan_v - pf)
    mesafe = max(mesafe, yaricap * 1.2)        # cismin içine girme

    cam.location = merkez + d * mesafe
    cam.rotation_euler = (merkez - cam.location).to_track_quat(
        '-Z', 'Y').to_euler()
    cd.clip_start = max(0.01, mesafe - yaricap * 3)
    cd.clip_end = mesafe + yaricap * 6
    return cam


# ---------------------------------------------------------------------------
# 5. RENDER AYARLARI
# ---------------------------------------------------------------------------

def cycles_kur(ornek: int = 400, gpu: bool = True):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    if gpu:
        try:
            bpy.ops.preferences.addon_enable(module='cycles')
            pr = bpy.context.preferences.addons['cycles'].preferences
            pr.compute_device_type = 'METAL'   # macOS'ta tek geçerli değer
            pr.refresh_devices()
            for d in pr.devices:
                d.use = (d.type == 'METAL')
            pr.metalrt = 'ON'
            sc.cycles.device = 'GPU'
        except Exception as e:
            print(f"[uyarı] Metal GPU kurulamadı, CPU'ya düşülüyor: {e}")
            sc.cycles.device = 'CPU'
    cy = sc.cycles
    cy.samples = ornek
    cy.use_adaptive_sampling = True
    cy.adaptive_threshold = 0.01
    cy.use_denoising = True
    cy.denoiser = 'OPENIMAGEDENOISE'      # macOS'ta tek seçenek
    cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    cy.denoising_prefilter = 'ACCURATE'
    cy.denoising_quality = 'HIGH'
    cy.denoising_use_gpu = True
    cy.max_bounces = 12
    cy.diffuse_bounces = 4
    cy.glossy_bounces = 4
    cy.volume_bounces = 0
    cy.caustics_reflective = False
    cy.caustics_refractive = False
    cy.use_light_tree = True


def eevee_kur(ornek: int = 64):
    """Hızlı önizleme. Motor adı 'BLENDER_EEVEE' — '_NEXT' YOK."""
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE'
    ev = sc.eevee
    ev.taa_render_samples = ornek
    ev.use_raytracing = True
    ev.use_shadows = True


def cikti_kur(gen=1920, yuk=1440, seffaf=False, mod: str = "katalog"):
    """mod: 'katalog' -> renk doğruluğu ('Standard')
            'vitrin'  -> ürün görseli ('Khronos PBR Neutral')"""
    sc = bpy.context.scene
    r = sc.render
    r.resolution_x, r.resolution_y = gen, yuk
    r.resolution_percentage = 100
    r.film_transparent = seffaf
    r.image_settings.media_type = 'IMAGE'       # file_format'TAN ÖNCE
    r.image_settings.file_format = 'PNG'
    r.image_settings.color_mode = 'RGBA' if seffaf else 'RGB'
    r.image_settings.color_depth = '8'
    sc.display_settings.display_device = 'sRGB'
    sc.view_settings.view_transform = ('Standard' if mod == "katalog"
                                       else 'Khronos PBR Neutral')
    sc.view_settings.look = 'None'
    sc.view_settings.exposure = 0.0


def beyaz_fon(seviye: float = 4.0):
    """Katalog için beyaz zemin.

    seviye view transform'a göre değişir — kompozitör scene-linear'da
    çalışır, 1.0 ekranda beyaz DEĞİLDİR:
      Standard -> 1.0 · Khronos PBR Neutral -> 4.0 · AgX -> 16.0
    """
    sc = bpy.context.scene
    # AlphaOver'in çalışması için render'ın alfası olmalı; yoksa arka plan
    # siyah kalır ve kompozit hiçbir şey yapmaz.
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = 'RGB'
    ng = bpy.data.node_groups.new("BeyazFon", "CompositorNodeTree")
    ng.interface.new_socket("Image", in_out='OUTPUT',
                            socket_type='NodeSocketColor')
    n = ng.nodes
    rl = n.new("CompositorNodeRLayers"); rl.scene = sc; rl.location = (-400, 0)
    col = n.new("CompositorNodeRGB"); col.location = (-400, -250)
    col.outputs[0].default_value = (seviye, seviye, seviye, 1.0)
    ust = n.new("CompositorNodeAlphaOver"); ust.location = (-100, 0)
    out = n.new("NodeGroupOutput"); out.location = (200, 0)
    ng.links.new(col.outputs[0], ust.inputs["Background"])
    ng.links.new(rl.outputs["Image"], ust.inputs["Foreground"])
    ng.links.new(ust.outputs[0], out.inputs[0])
    sc.compositing_node_group = ng      # scene.node_tree KALDIRILDI
    sc.render.use_compositing = True
    return ng


def render_et(yol: str):
    os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
    bpy.context.scene.render.filepath = yol
    bpy.ops.render.render(write_still=True)
    print(f"[render] {yol}")
    return yol


def doner_kare(nesneler, klasor: str, adet: int = 8, yukseklik_m: float = 1.0):
    """Turntable. Nesneyi DEĞİL kamerayı döndür — nesne dönerse dünya-uzaylı
    UV'ler kayar ve desen yönü bozulur."""
    sc = bpy.context.scene
    mn, mx = sinir_kutusu(nesneler)
    merkez = (mn + mx) * 0.5
    piv = bpy.data.objects.new("Pivot", None)
    sc.collection.objects.link(piv)
    piv.location = merkez
    cam = sc.camera
    yerel = cam.matrix_world.translation - merkez
    cam.parent = piv
    cam.location = yerel
    cam.rotation_euler = (-yerel).to_track_quat('-Z', 'Y').to_euler()
    yollar = []
    for i in range(adet):
        piv.rotation_euler = (0, 0, math.radians(360.0 * i / adet))
        yollar.append(render_et(os.path.join(klasor, f"tur_{i:02d}.png")))
    return yollar


def usdz_ver(yol: str):
    """AR / web için. generate_preview_surface AR Quick Look için ZORUNLU."""
    bpy.ops.wm.usd_export(
        filepath=yol, export_materials=True, generate_preview_surface=True,
        export_textures_mode='NEW', usdz_downscale_size='2048',
        export_uvmaps=True, evaluation_mode='RENDER',
        export_lights=False, export_cameras=False)
    print(f"[usdz] {yol}")
    return yol


def glb_ver(yol: str):
    bpy.ops.export_scene.gltf(
        filepath=yol, export_format='GLB', export_materials='EXPORT',
        export_image_format='AUTO', export_apply=True, export_yup=True)
    print(f"[glb] {yol}")
    return yol


# ---------------------------------------------------------------------------
# 6. ÇOKLU GÖRÜNÜŞ + 3B BAĞLI AÇIKLAMA OKLARI
# ---------------------------------------------------------------------------

# (dosya adı, azimut, yükseliş, kapak açık mı, başlık)
STANDART_ACILAR = [
    ("uc_ceyrek", 35.0, 12.0, False, "Üç çeyrek"),
    ("on",         0.0,  4.0, False, "Ön"),
    ("sag",       90.0,  4.0, False, "Sağ yan"),
    ("sol",      -90.0,  4.0, False, "Sol yan"),
    ("arka",     180.0,  4.0, False, "Arka"),
    ("ust",        0.0, 72.0, False, "Üst"),
    ("acik",      14.0,  8.0, True,  "Açık"),
    ("acik_ceyrek", 38.0, 10.0, True, "Açık · üç çeyrek"),
    ("ic_detay",  22.0,  -6.0, True, "İç detay"),
]


def _en_yakin_carpma(nesneler, deps, kam, yon, uz):
    """Kameradan çıkan ışının ürün parçalarına en yakın çarpma
    mesafesi. Gölge yakalayıcı zemin gibi sahne yardımcıları
    DAHİL EDİLMEZ — yoksa alttan bakışta her nokta kapalı sanılır."""
    en = None
    for o in nesneler:
        ev = o.evaluated_get(deps)
        mi = ev.matrix_world.inverted()
        yer = mi @ kam
        d = (mi.to_3x3() @ yon).normalized()
        try:
            vurdu, kon, _, _ = ev.ray_cast(yer, d, distance=uz)
        except Exception:
            continue
        if vurdu:
            m = (ev.matrix_world @ kon - kam).length
            if en is None or m < en:
                en = m
    return en


def not_pikselleri(notlar, gen, yuk, nesneler=None):
    """3B model noktalarını render pikseline çevirir.

    notlar: [{"metin":..., "konum":(x,y,z) mm}, ...]
    Dönen: [{"metin":..., "x":px, "y":px, "gorunur":bool}, ...]
    y ekseni GÖRÜNTÜ yönünde (üstten aşağı) verilir.
    """
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    cam = sc.camera
    deps = bpy.context.evaluated_depsgraph_get()
    kam = cam.matrix_world.translation
    out = []
    for n in notlar:
        v = Vector([c / 1000.0 for c in n["konum"]])       # mm -> m
        co = world_to_camera_view(sc, cam, v)
        kadrajda = bool(0.02 <= co.x <= 0.98 and 0.02 <= co.y <= 0.98
                        and co.z > 0)

        # Kapalılık testi: kameradan noktaya ışın at. İlk çarpma noktadan
        # belirgin biçimde ÖNCE ise nokta bir parçanın arkasında kalmıştır
        # (ör. açık kapağın arkasındaki kaide) — ok boşluğu göstermesin.
        acik = True
        if kadrajda:
            d = v - kam
            uz = d.length
            if uz > 1e-6 and nesneler:
                d.normalize()
                m = _en_yakin_carpma(nesneler, deps, kam, d, uz)
                if m is not None and m < uz - 0.025:            # 25 mm pay
                    acik = False

        out.append({
            "metin": n["metin"],
            "x": co.x * gen,
            "y": (1.0 - co.y) * yuk,
            "gorunur": bool(kadrajda and acik),
            "yon": n.get("yon", "sag"),
        })
    return out


def olcu_pikselleri(olculer, gen, yuk):
    """Ölçü kalemlerinin 3B uç noktalarını render pikseline çevirir.

    olculer: [{"etiket":..., "a":(x,y,z), "b":(...), "d":(...)}, ...]  mm
    Dönen her kalem: ax/ay · bx/by (ölçülen doğru) · dx/dy (dışa kaçış
    yönünü veren üçüncü nokta) — hepsi piksel, y üstten aşağı.

    Kapalılık testi YAPILMAZ: ölçü çizgisi gövdenin dışında durur,
    ürünün arkasında kalması beklenmez.
    """
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    cam = sc.camera

    def nokta(k):
        co = world_to_camera_view(sc, cam, Vector([c / 1000.0 for c in k]))
        return co.x * gen, (1.0 - co.y) * yuk, co.z > 0

    out = []
    for o in olculer:
        ax, ay, a_on = nokta(o["a"])
        bx, by, b_on = nokta(o["b"])
        dx, dy, _ = nokta(o["d"])
        out.append({
            "etiket": o["etiket"], "sinif": o.get("sinif", "zincir"),
            "ax": ax, "ay": ay, "bx": bx, "by": by, "dx": dx, "dy": dy,
            "kadrajda": bool(a_on and b_on
                             and -0.15 * gen <= ax <= 1.15 * gen
                             and -0.15 * gen <= bx <= 1.15 * gen),
        })
    return out


def coklu_render(nesneler, klasor, notlar=None, acilar=None, ornek=300,
                 gen=1400, yuk=1500, kapak_aci=105.0, mod="vitrin",
                 olculer=None):
    """Standart görünüş setini render eder; her kare için açıklama
    noktalarının PİKSEL konumlarını da yazar.

    Kapak açık kareler için sahne yeniden kurulmaz — kapaklar açılır,
    render alınır, sonra ters açıyla eski hâline döndürülür. Böylece
    materyal/ışık kurulumu bir kez yapılır.
    """
    import json
    os.makedirs(klasor, exist_ok=True)
    acilar = acilar or STANDART_ACILAR
    sonuc = {}
    acik_durum = False

    for ad, az, yuks, acik, baslik in acilar:
        if acik and not acik_durum:
            kapaklari_ac(nesneler, menteseli=kapak_aci,
                         devrilir=min(kapak_aci, 52.0))
            acik_durum = True
        elif not acik and acik_durum:
            kapaklari_ac(nesneler, menteseli=-kapak_aci,
                         devrilir=-min(kapak_aci, 52.0))
            acik_durum = False

        sc = bpy.context.scene
        sc.render.resolution_x, sc.render.resolution_y = gen, yuk
        for o in list(sc.objects):
            if o.type == 'CAMERA':
                bpy.data.objects.remove(o, do_unlink=True)
        kamera(nesneler, azimut=az, yukselis=yuks)
        yol = render_et(os.path.join(klasor, f"{ad}.png"))
        kayit = {"dosya": os.path.basename(yol), "baslik": baslik,
                 "azimut": az, "yukselis": yuks, "acik": acik,
                 "gen": gen, "yuk": yuk}
        if notlar:
            kayit["notlar"] = not_pikselleri(notlar, gen, yuk,
                                             nesneler=nesneler)
        if olculer:
            kayit["olculer"] = olcu_pikselleri(olculer, gen, yuk)
        sonuc[ad] = kayit

    with open(os.path.join(klasor, "goruntuler.json"), "w",
              encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)
    print(f"[set] {len(sonuc)} görünüş -> {klasor}/goruntuler.json")
    return sonuc


# ---------------------------------------------------------------------------
# 7. CLI
# ---------------------------------------------------------------------------

def main():
    argv = sys.argv
    args = argv[argv.index("--") + 1:] if "--" in argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", required=True)
    ap.add_argument("--out", default="render")
    ap.add_argument("--govde", default="mese",
                    help="mese|ceviz|kayin|antrasit veya melamin rengi")
    ap.add_argument("--melamin", action="store_true",
                    help="ahşap yerine düz renk melamin")
    ap.add_argument("--bant", default="antrasit",
                    help="melamin rengi; 'ayni' = bant gövde dekoruyla aynı "
                         "(dekor baskılı PVC bant)")
    ap.add_argument("--doku", default=None, help="PBR doku klasörü")
    ap.add_argument("--hdri", default=None)
    ap.add_argument("--ornek", type=int, default=400)
    ap.add_argument("--gen", type=int, default=1920)
    ap.add_argument("--yuk", type=int, default=1440)
    ap.add_argument("--mod", default="vitrin", choices=["vitrin", "katalog"])
    ap.add_argument("--eevee", action="store_true")
    ap.add_argument("--tur", type=int, default=0, help="turntable kare sayısı")
    ap.add_argument("--usdz", action="store_true")
    ap.add_argument("--kapak-ac", type=float, default=0.0,
                    dest="kapak_ac",
                    help="kapakları bu açıyla aç (menteşeli derece)")
    ap.add_argument("--azimut", type=float, default=35.0)
    ap.add_argument("--yukselis", type=float, default=12.0,
                    help="kamera yükseliş açısı; negatif = alttan bakış")
    ap.add_argument("--dosya", default="hero")
    ap.add_argument("--set", action="store_true",
                    dest="tam_set",
                    help="standart görünüş setini render et")
    ap.add_argument("--notlar", default=None,
                    help="açıklama noktaları JSON dosyası")
    ap.add_argument("--olculer", default=None,
                    help="render üzerine çizilecek ölçüler JSON dosyası")
    a = ap.parse_args(args)

    temizle()
    nesneler = glb_al(a.glb)
    mn, mx = sinir_kutusu(nesneler)
    yuk_m = (mx - mn).z

    # Materyaller
    if a.doku:
        govde = pbr_dokulu("Gövde", a.doku)
        govde_yatay = pbr_dokulu("Gövde_Yatay", a.doku, desen_donus=90)
    elif a.melamin:
        govde = govde_yatay = melamin("Gövde", a.govde)
    else:
        govde = ahsap_prosedurel("Gövde", a.govde, desen_ekseni="V")
        govde_yatay = ahsap_prosedurel("Gövde_Yatay", a.govde, desen_ekseni="U")
    # 'ayni': dekor baskılı bant — yüzeyle aynı materyal, ayrı slotta kalır
    bant = None if a.bant == "ayni" else melamin("KenarBandi", a.bant,
                                                  parlaklik=0.35)

    ayna_mat = ayna()
    for o in nesneler:
        if "AYNA" in o.name.upper():
            o.data.materials.clear()
            o.data.materials.append(ayna_mat)
            pah(o, 0.4)
            continue
        boyut = o.dimensions
        # En ince eksen = kalınlık ekseni
        kal_ekseni = "xyz"[min(range(3), key=lambda i: boyut[i])]
        # Yatay paneller (kalınlığı Z'de) desen yatay aksın
        yatay = (kal_ekseni == "z")
        kutu_uv(o, desen="X" if yatay else "Z", yogunluk=1.0)
        gm = govde_yatay if yatay else govde
        bant_ata(o, gm, bant if bant is not None else gm, kal_ekseni)
        pah(o, 0.5)

    # --set kendi kapak durumunu yönetir; burada AÇMA, yoksa "kapalı"
    # kareler açık render edilir ve açık kareler iki kez açılır.
    if a.kapak_ac and not a.tam_set:
        kapaklari_ac(nesneler, menteseli=a.kapak_ac,
                     devrilir=min(a.kapak_ac, 52.0))

    # Sahne
    if a.hdri:
        hdri_dunya(a.hdri, guc=1.0)
    else:
        studyo(yuk_m, anahtar_w=110.0 * max(yuk_m, 0.5))
        notr_dunya(0.45)
    zemin(golge_yakalayici=True)
    cikti_kur(a.gen, a.yuk, seffaf=False, mod=a.mod)
    kamera(nesneler, azimut=a.azimut, yukselis=a.yukselis)
    (eevee_kur(64) if a.eevee else cycles_kur(a.ornek))
    beyaz_fon(1.0 if a.mod == "katalog" else 4.0)

    if a.tam_set:
        import json
        notlar = olculer = None
        if a.notlar and os.path.exists(a.notlar):
            notlar = json.load(open(a.notlar, encoding="utf-8"))
        if a.olculer and os.path.exists(a.olculer):
            olculer = json.load(open(a.olculer, encoding="utf-8"))
        coklu_render(nesneler, a.out, notlar=notlar, ornek=a.ornek,
                     gen=a.gen, yuk=a.yuk,
                     kapak_aci=a.kapak_ac or 105.0, mod=a.mod,
                     olculer=olculer)
        if a.usdz:
            usdz_ver(os.path.join(a.out, "model.usdz"))
        return

    render_et(os.path.join(a.out, f"{a.dosya}.png"))
    if a.tur:
        doner_kare(nesneler, os.path.join(a.out, "turntable"), a.tur, yuk_m)
    if a.usdz:
        usdz_ver(os.path.join(a.out, "model.usdz"))


if __name__ == "__main__":
    main()
