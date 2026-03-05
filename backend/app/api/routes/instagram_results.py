"""
Router: Instagram Results
Grup khusus untuk melihat dan mengakses hasil crawling Instagram.
"""

from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any

from ...utils import (
    list_crawl_results_metadata,
    get_crawl_result_detail,
    get_crawl_result_by_target,
)
from ..deps import get_api_key

router = APIRouter(
    prefix="/instagram/results",
    tags=["Hasil Crawling Instagram"],
    dependencies=[Depends(get_api_key)],
)

# ============================================================
# Comment (Username) Results
# ============================================================

@router.get(
    "/comment/list",
    response_model=List[Dict[str, Any]],
    summary="List semua hasil crawling username Instagram",
)
async def list_comment_results():
    """
    Menampilkan **daftar semua file** hasil crawling komentar Instagram (berdasarkan username/profil).

    Setiap item berisi metadata ringkas: `id` (nama file), `target`, `total_comments`, `crawled_at`, `status`.
    """
    metadata = list_crawl_results_metadata("instagram", "comment")
    if not metadata:
        raise HTTPException(
            status_code=404,
            detail="Belum ada data crawling Instagram. Silakan lakukan crawling terlebih dahulu.",
        )
    return metadata


@router.get(
    "/comment/detail/{identifier}",
    response_model=Dict[str, Any],
    summary="Detail hasil crawling username Instagram",
)
async def get_comment_detail(identifier: str):
    """
    Mengambil **isi lengkap** dari satu file hasil crawling komentar Instagram.

    `identifier` bisa berupa:
    - **Nama file** (contoh: `instagram_2026-03-05T10-00-00.json`)
    - **Username** target (contoh: `namaprofil`)
    """
    # Coba anggap sebagai filename dulu
    result = get_crawl_result_detail("instagram", "comment", identifier)

    # Jika tidak ketemu sebagai file, coba cari by target/username
    if not result:
        result = get_crawl_result_by_target("instagram", "comment", identifier)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Hasil crawling untuk '{identifier}' tidak ditemukan.",
        )
    return result


# ============================================================
# Hashtag Results
# ============================================================

@router.get(
    "/hashtag/list",
    response_model=List[Dict[str, Any]],
    summary="List semua hasil crawling hashtag Instagram",
)
async def list_hashtag_results():
    """
    Menampilkan **daftar semua file** hasil crawling hashtag Instagram.

    Setiap item berisi metadata ringkas: `id` (nama file), `target`, `total_comments`, `crawled_at`, `status`.
    """
    metadata = list_crawl_results_metadata("instagram", "hashtag")
    if not metadata:
        raise HTTPException(
            status_code=404,
            detail="Belum ada data crawling hashtag Instagram. Silakan lakukan crawling terlebih dahulu.",
        )
    return metadata


@router.get(
    "/hashtag/detail/{identifier}",
    response_model=Dict[str, Any],
    summary="Detail hasil crawling hashtag Instagram",
)
async def get_hashtag_detail(identifier: str):
    """
    Mengambil **isi lengkap** dari satu file hasil crawling hashtag Instagram.

    `identifier` bisa berupa:
    - **Nama file** (contoh: `instagram_2026-03-05T10-00-00.json`)
    - **Nama hashtag** (contoh: `teknologi` atau `#teknologi`)
    """
    # URL-decode dulu (mis: %23banjir → #banjir), lalu buang tanda # atau %23
    decoded = unquote(identifier)          # %23banjirpasuruan → #banjirpasuruan
    clean_id = decoded.lstrip("#")         # #banjirpasuruan  → banjirpasuruan

    # Coba sebagai filename asli, lalu sebagai target/hashtag name
    result = get_crawl_result_detail("instagram", "hashtag", identifier)
    if not result:
        result = get_crawl_result_detail("instagram", "hashtag", decoded)
    if not result:
        result = get_crawl_result_by_target("instagram", "hashtag", clean_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Hasil crawling untuk hashtag '{clean_id}' tidak ditemukan.",
        )
    return result
