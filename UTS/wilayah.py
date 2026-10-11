# -*- coding: utf-8 -*-
"""
================================================================================
wilayah.py – Modul Bantu Wilayah Jawa Timur
================================================================================
Menyediakan fungsi-fungsi umum yang dipakai oleh semua notebook dan app.py:
- muat_batas        : muat GeoDataFrame batas administrasi
- batas_gabungan    : satukan semua fitur menjadi satu geometri
- bbox_dari_batas   : ekstrak bounding box dari batas (BUKAN nilai tulis tangan)
- titik_di_dalam    : uji apakah titik-titik berada di dalam batas (vectorized)
- mask_raster       : buat mask raster boolean dari geometri
- luas_piksel_km2   : hitung luas piksel dengan koreksi lintang

Semua path RELATIF terhadap folder UTS (BASE_DIR).
CRS yang didukung: EPSG:4326 (lon/lat WGS84).
================================================================================
"""

from pathlib import Path
import numpy as np
import geopandas as gpd
from shapely.geometry import mapping
from shapely.ops import unary_union
from shapely.validation import make_valid
import pandas as pd

# ------------------------------------------------------------------------------
# KONSTANTA KONVERSI DERAJAT -> KM
# ------------------------------------------------------------------------------
KM_PER_DEG_LAT = 110.574   # km per derajat lintang (hampir konstan)
KM_PER_DEG_LON_EQ = 111.32  # km per derajat bujur di ekuator


# ------------------------------------------------------------------------------
# 1. muat_batas
# ------------------------------------------------------------------------------
def muat_batas(path: str | Path) -> gpd.GeoDataFrame:
    """
    Muat file GeoJSON/Shapefile batas administrasi sebagai GeoDataFrame EPSG:4326 yang valid.

    Parameter
    ---------
    path : str atau Path
        Path ke file geojson (atau format vektor yang didukung geopandas).

    Mengembalikan
    -------------
    GeoDataFrame dengan CRS EPSG:4326, geometri valid.
    Jika ada geometri tidak valid, diperbaiki dengan make_valid().
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File batas tidak ditemukan: {path}")

    gdf = gpd.read_file(path)

    # Pastikan CRS adalah EPSG:4326
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
        print("[wilayah] CRS tidak ditemukan, diasumsikan EPSG:4326.")
    elif gdf.crs.to_epsg() != 4326:
        crs_asal = gdf.crs
        gdf = gdf.to_crs("EPSG:4326")
        print(f"[wilayah] Reproyeksi dari {crs_asal} ke EPSG:4326.")

    # Perbaiki geometri tidak valid
    n_invalid = (~gdf.geometry.is_valid).sum()
    if n_invalid > 0:
        gdf["geometry"] = gdf.geometry.apply(
            lambda g: make_valid(g) if not g.is_valid else g
        )
        print(f"[wilayah] {n_invalid} geometri diperbaiki dengan make_valid().")
    else:
        print(f"[wilayah] Semua {len(gdf)} geometri valid.")

    return gdf


# ------------------------------------------------------------------------------
# 2. batas_gabungan
# ------------------------------------------------------------------------------
def batas_gabungan(gdf: gpd.GeoDataFrame):
    """
    Satukan semua fitur menjadi satu geometri (unary_union).

    Parameter
    ---------
    gdf : GeoDataFrame

    Mengembalikan
    -------------
    Shapely geometry tunggal (Polygon atau MultiPolygon).
    """
    return unary_union(gdf.geometry)


# ------------------------------------------------------------------------------
# 3. bbox_dari_batas
# ------------------------------------------------------------------------------
def bbox_dari_batas(gdf: gpd.GeoDataFrame, margin: float = 0.0) -> dict:
    """
    Hitung bounding box dari total_bounds GeoDataFrame.
    BUKAN nilai tulis tangan – selalu dihitung dari data aktual.

    Parameter
    ---------
    gdf    : GeoDataFrame (EPSG:4326)
    margin : penambahan margin dalam derajat (default 0.0)

    Mengembalikan
    -------------
    dict dengan kunci 'west', 'south', 'east', 'north'
    """
    west, south, east, north = gdf.total_bounds
    return {
        "west":  float(west  - margin),
        "south": float(south - margin),
        "east":  float(east  + margin),
        "north": float(north + margin),
    }


# ------------------------------------------------------------------------------
# 4. titik_di_dalam
# ------------------------------------------------------------------------------
def titik_di_dalam(
    df: pd.DataFrame,
    gdf_batas: gpd.GeoDataFrame,
    lon: str = "lon",
    lat: str = "lat",
) -> pd.Series:
    """
    Uji apakah setiap baris DataFrame berada di dalam batas administrasi.
    Menggunakan spatial join (vectorized) – aman untuk 600 ribu baris.

    Parameter
    ---------
    df        : DataFrame dengan kolom lon dan lat
    gdf_batas : GeoDataFrame batas wilayah (EPSG:4326)
    lon       : nama kolom bujur
    lat       : nama kolom lintang

    Mengembalikan
    -------------
    pd.Series boolean (True = di dalam batas), index sama dengan df.
    """
    # Buat GeoDataFrame titik
    gdf_titik = gpd.GeoDataFrame(
        {"_idx": df.index},
        geometry=gpd.points_from_xy(df[lon], df[lat]),
        crs="EPSG:4326",
        index=df.index,
    )

    # Spatial join: keep only points that intersect boundary
    # Gunakan unary_union batas sebagai satu geometri
    geom_gabungan = batas_gabungan(gdf_batas)
    gdf_batas_union = gpd.GeoDataFrame(
        {"dummy": [0]},
        geometry=[geom_gabungan],
        crs="EPSG:4326",
    )

    joined = gpd.sjoin(
        gdf_titik,
        gdf_batas_union,
        how="left",
        predicate="within",
    )

    # Jika index_right tidak NaN berarti titik di dalam
    dalam = joined["index_right"].notna()
    # Pastikan index sama dengan df
    return dalam.reindex(df.index, fill_value=False)


# ------------------------------------------------------------------------------
# 5. mask_raster
# ------------------------------------------------------------------------------
def mask_raster(
    shape: tuple,
    transform,
    geom,
    all_touched: bool = True,
) -> np.ndarray:
    """
    Buat mask boolean dari geometri shapely untuk grid raster.

    Catatan: all_touched=True digunakan agar pulau-pulau kecil (misalnya
    Kepulauan Kangean) tidak hilang pada resolusi ~250 m. Piksel yang
    menyentuh batas (tidak hanya di pusat piksel) tetap dimasukkan.

    Parameter
    ---------
    shape       : (height, width) – dimensi raster
    transform   : Affine transform dari rasterio
    geom        : Shapely geometry (Polygon/MultiPolygon) – batas wilayah
    all_touched : jika True, piksel yang disentuh batas ikut dimasukkan

    Mengembalikan
    -------------
    np.ndarray boolean shape (height, width), True = di dalam batas
    """
    from rasterio.features import geometry_mask

    # geometry_mask mengembalikan True di LUAR, jadi invert=True agar
    # True = di dalam batas
    mask = geometry_mask(
        geometries=[mapping(geom)],
        out_shape=shape,
        transform=transform,
        invert=True,       # True = piksel di dalam batas
        all_touched=all_touched,
    )
    return mask


# ------------------------------------------------------------------------------
# 6. luas_piksel_km2
# ------------------------------------------------------------------------------
def luas_piksel_km2(transform, shape: tuple) -> np.ndarray:
    """
    Hitung luas per baris piksel dengan koreksi lintang.

    Lebar piksel dalam derajat bujur dikali 111.32*cos(lintang) memberi
    lebar piksel dalam km. Tinggi piksel dikali 110.574 memberi tinggi km.
    Koreksi ini penting karena derajat bujur mengecil mendekati kutub.

    Parameter
    ---------
    transform : Affine transform rasterio (atau rasterio.transform.Affine)
    shape     : (height, width) dimensi raster

    Mengembalikan
    -------------
    np.ndarray shape (height,) – luas piksel (km²) per baris
    """
    height, width = shape

    # Resolusi piksel dalam derajat (ambil nilai absolut)
    res_lon_deg = abs(transform.a)   # lebar piksel dalam derajat bujur
    res_lat_deg = abs(transform.e)   # tinggi piksel dalam derajat lintang

    # Lintang tengah tiap baris piksel
    # transform.f = koordinat Y (lintang) tepi atas kiri
    lat_atas = transform.f
    # Baris 0 -> pusat = lat_atas - 0.5*res_lat_deg, dst.
    lats = lat_atas - (np.arange(height) + 0.5) * res_lat_deg

    # Lebar piksel dalam km (koreksi lintang)
    lebar_km = res_lon_deg * KM_PER_DEG_LON_EQ * np.cos(np.radians(lats))
    # Tinggi piksel dalam km
    tinggi_km = res_lat_deg * KM_PER_DEG_LAT

    luas_km2_per_baris = lebar_km * tinggi_km  # shape (height,)
    return luas_km2_per_baris


# ------------------------------------------------------------------------------
# UTILITAS TAMBAHAN
# ------------------------------------------------------------------------------
def sederhanakan_batas(
    gdf: gpd.GeoDataFrame,
    toleransi: float = 0.001,
    path_simpan: str | Path | None = None,
) -> gpd.GeoDataFrame:
    """
    Sederhanakan geometri untuk tampilan peta agar file HTML tidak membengkak.
    Topologi dipertahankan dengan preserve_topology=True.
    Versi asli TIDAK diubah – fungsi ini mengembalikan salinan.

    Parameter
    ---------
    gdf         : GeoDataFrame asli (dipakai untuk masking dan analisis)
    toleransi   : toleransi simplifikasi dalam derajat (default 0.001 ≈ 100 m)
    path_simpan : jika diberikan, simpan ke file ini

    Mengembalikan
    -------------
    GeoDataFrame dengan geometri yang telah disederhanakan
    """
    gdf_simple = gdf.copy()
    gdf_simple["geometry"] = gdf_simple.geometry.simplify(
        tolerance=toleransi, preserve_topology=True
    )
    if path_simpan is not None:
        path_simpan = Path(path_simpan)
        gdf_simple.to_file(str(path_simpan), driver="GeoJSON")
        print(f"[wilayah] Batas sederhana disimpan ke: {path_simpan}")
    return gdf_simple


def luas_batas_km2(gdf: gpd.GeoDataFrame, epsg_metrik: int = 32749) -> float:
    """
    Hitung luas total batas dalam km² menggunakan proyeksi metrik.

    Parameter
    ---------
    gdf        : GeoDataFrame (EPSG:4326)
    epsg_metrik: EPSG CRS metrik (default 32749 = UTM Zone 49S, cocok Jawa Timur)

    Mengembalikan
    -------------
    Luas total dalam km²
    """
    gdf_m = gdf.to_crs(epsg=epsg_metrik)
    luas_m2 = gdf_m.geometry.area.sum()
    return luas_m2 / 1e6  # m² -> km²


# ------------------------------------------------------------------------------
# 8. fokus_ke_jatim
# ------------------------------------------------------------------------------
def fokus_ke_jatim(
    m,
    gdf_batas: gpd.GeoDataFrame,
    padding: tuple = (20, 20),
    max_zoom: int = 10,
    min_zoom: int = 6
):
    """
    Fokuskan peta Folium ke batas wilayah Jawa Timur dengan validasi CRS dan rentang koordinat.
    Menambahkan pula event listener JavaScript (invalidateSize dan resize) agar peta di iframe
    Streamlit tidak zoom out ke tingkat dunia.

    Parameter
    ---------
    m          : folium.Map
        Objek peta Folium yang akan difokuskan.
    gdf_batas  : gpd.GeoDataFrame
        GeoDataFrame batas administrasi Jawa Timur.
    padding    : tuple of int
        Padding tampilan dalam piksel (default (20, 20)).
    max_zoom   : int
        Batas maksimal zoom fit_bounds (default 10).
    min_zoom   : int
        Batas minimal zoom peta agar pengguna tidak zoom out ke peta dunia (default 6).

    Mengembalikan
    -------------
    folium.Map yang telah difit_bounds dan dilengkapi skrip inisialisasi browser.
    """
    import folium

    # 1. Pastikan CRS adalah EPSG:4326
    if gdf_batas.crs is None:
        raise ValueError("gdf_batas tidak memiliki CRS terdefinisi! Harap definisikan CRS.")
    if gdf_batas.crs.to_epsg() != 4326:
        gdf_batas = gdf_batas.to_crs(epsg=4326)

    # 2. Ambil total_bounds dan validasi
    west, south, east, north = gdf_batas.total_bounds
    
    # Periksa nilai NaN atau Inf
    if not (np.isfinite(west) and np.isfinite(south) and np.isfinite(east) and np.isfinite(north)):
        raise ValueError(
            f"Bounds batas mengandung nilai non-finite/NaN: "
            f"west={west}, south={south}, east={east}, north={north}."
        )

    # Rentang wajar wilayah Jawa Timur (termasuk pulau Madura, Bawean, Kangean)
    # West ~110 - 116, East ~110 - 116.5, South ~ -9.5 - -5.0, North ~ -9.0 - -5.0
    if not (110.0 <= west <= 116.0 and 110.0 <= east <= 116.5 and
            -9.5 <= south <= -5.0 and -9.0 <= north <= -5.0 and
            west < east and south < north):
        raise ValueError(
            f"total_bounds di luar rentang wajar Jawa Timur: "
            f"west={west}, south={south}, east={east}, north={north}. "
            f"Kemungkinan penyebab: CRS salah (satuan meter/terproyeksi), urutan terbalik, atau geometri kosong."
        )

    # 3. Urutan argumen fit_bounds Folium: [[south, west], [north, east]] -> [[lat_min, lon_min], [lat_max, lon_max]]
    m.fit_bounds([[float(south), float(west)], [float(north), float(east)]], padding=padding, max_zoom=max_zoom)

    # 4. Tambahkan MacroElement yang dieksekusi TEPAT SETELAH inisialisasi objek map Leaflet
    class SkripInisialisasiJatim(folium.MacroElement):
        def __init__(self, target_map_id, s_val, w_val, n_val, e_val, pad, max_z):
            super().__init__()
            self._target_map_id = target_map_id
            self._template = folium.elements.Template(f"""
                {{% macro script(this, kwargs) %}}
                (function() {{
                    var mapInstance = {target_map_id};
                    var boundsJatim = [[{s_val}, {w_val}], [{n_val}, {e_val}]];
                    var opts = {{padding: [{pad[0]}, {pad[1]}], maxZoom: {max_z}}};

                    function lakukanFokus() {{
                        if (mapInstance && typeof mapInstance.invalidateSize === 'function') {{
                            mapInstance.invalidateSize();
                            if (!mapInstance._user_has_interacted) {{
                                mapInstance.fitBounds(boundsJatim, opts);
                            }}
                        }}
                    }}

                    if (mapInstance) {{
                        mapInstance.on('movestart zoomstart', function() {{
                            mapInstance._user_has_interacted = true;
                        }});
                        // Panggilan berkala untuk mengatasi layout iframe di streamlit tabs
                        setTimeout(lakukanFokus, 50);
                        setTimeout(lakukanFokus, 200);
                        setTimeout(lakukanFokus, 500);
                        setTimeout(lakukanFokus, 1000);
                    }}

                    window.addEventListener('resize', function() {{
                        if (mapInstance && typeof mapInstance.invalidateSize === 'function') {{
                            mapInstance.invalidateSize();
                        }}
                    }});
                }})();
                {{% endmacro %}}
            """)

    map_var_name = m.get_name()
    m.add_child(SkripInisialisasiJatim(
        map_var_name,
        float(south), float(west), float(north), float(east),
        padding, max_zoom
    ))

    return m

