"""
Router: TikTok Results
Grup khusus untuk melihat dan mengakses hasil crawling TikTok.
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
    prefix="/tiktok/results",
    tags=["Hasil Crawling TikTok"],
    dependencies=[Depends(get_api_key)],
)

# ============================================================
# Comment (Username) Results
# ============================================================

@router.get(
    "/comment/list",
    response_model=List[Dict[str, Any]],
    summary="List semua hasil crawling username TikTok",
)
async def list_comment_results():
    """
    Menampilkan **daftar semua file** hasil crawling komentar TikTok (berdasarkan username/profil).

    Setiap item berisi metadata ringkas: `id` (nama file), `target`, `total_comments`, `crawled_at`, `status`.
    """
    metadata = list_crawl_results_metadata("tiktok", "comment")
    if not metadata:
        raise HTTPException(
            status_code=404,
            detail="Belum ada data crawling TikTok. Silakan lakukan crawling terlebih dahulu.",
        )
    return metadata


@router.get(
    "/comment/detail/{identifier}",
    response_model=Dict[str, Any],
    summary="Detail hasil crawling username TikTok",
)
async def get_comment_detail(identifier: str):
    """
    Mengambil **isi lengkap** dari satu file hasil crawling komentar TikTok.

    `identifier` bisa berupa:
    - **Nama file** (contoh: `tiktok_2026-03-05T10-00-00.json`)
    - **Username** target (contoh: `namaakun`)
    """
    result = get_crawl_result_detail("tiktok", "comment", identifier)
    if not result:
        result = get_crawl_result_by_target("tiktok", "comment", identifier)

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
    summary="List semua hasil crawling hashtag TikTok",
)
async def list_hashtag_results():
    """
    Menampilkan **daftar semua file** hasil crawling hashtag TikTok.

    Setiap item berisi metadata ringkas: `id` (nama file), `target`, `total_comments`, `crawled_at`, `status`.
    """
    metadata = list_crawl_results_metadata("tiktok", "hashtag")
    if not metadata:
        raise HTTPException(
            status_code=404,
            detail="Belum ada data crawling hashtag TikTok. Silakan lakukan crawling terlebih dahulu.",
        )
    return metadata


@router.get(
    "/hashtag/detail/{identifier}",
    response_model=Dict[str, Any],
    summary="Detail hasil crawling hashtag TikTok",
)
async def get_hashtag_detail(identifier: str):
    """
    Mengambil **isi lengkap** dari satu file hasil crawling hashtag TikTok.

    `identifier` bisa berupa:
    - **Nama file** (contoh: `tiktok_2026-03-05T10-00-00.json`)
    - **Nama hashtag** (contoh: `fyp` atau `#fyp`)
    """
    # URL-decode dulu (mis: %23fyp → #fyp), lalu buang tanda #
    decoded = unquote(identifier)          # %23fyp → #fyp
    clean_id = decoded.lstrip("#")         # #fyp  → fyp

    result = get_crawl_result_detail("tiktok", "hashtag", identifier)
    if not result:
        result = get_crawl_result_detail("tiktok", "hashtag", decoded)
    if not result:
        result = get_crawl_result_by_target("tiktok", "hashtag", clean_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Hasil crawling untuk hashtag '{clean_id}' tidak ditemukan.",
        )
    return result
