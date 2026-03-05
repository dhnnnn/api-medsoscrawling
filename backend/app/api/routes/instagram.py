"""
Router: Crawling Instagram
Endpoint untuk menjalankan proses crawling pada platform Instagram.
"""

import asyncio
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from typing import Dict, Any

from ...schemas.models import InstagramCrawlRequest, HashtagCrawlRequest, CrawlResult
from ...services.crawler_service import crawl_instagram_profile, crawl_instagram_hashtag
from ...utils import get_latest_crawl_result
from ..deps import get_api_key

router = APIRouter(
    prefix="/instagram",
    tags=["Crawling Instagram"],
    dependencies=[Depends(get_api_key)],
)

# ============================================================
# Crawl Actions
# ============================================================

@router.post("/crawl/username", response_model=CrawlResult, summary="Crawl komentar Instagram by username")
async def crawl_profile(request: InstagramCrawlRequest) -> CrawlResult:
    """
    Crawl komentar dari profil Instagram berdasarkan **username** atau URL profil.

    Hasil crawling disimpan otomatis di `data/crawling/instagram/comment/`.
    """
    if not request.target.strip():
        raise HTTPException(status_code=400, detail="Target tidak boleh kosong.")

    logger.info(f"[API:IG] POST /instagram/crawl/username | target={request.target}")
    try:
        result = await asyncio.to_thread(
            crawl_instagram_profile,
            request.target.strip(),
            request.max_posts,
        )
        return result
    except Exception as e:
        logger.error(f"[API:IG] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crawl/hashtag", response_model=CrawlResult, summary="Crawl komentar Instagram by hashtag")
async def crawl_hashtag(request: HashtagCrawlRequest) -> CrawlResult:
    """
    Crawl postingan dan komentar dari Instagram berdasarkan **hashtag**.

    Hasil crawling disimpan otomatis di `data/crawling/instagram/hashtag/`.
    """
    hashtag = request.hashtag.strip().lstrip("#")
    if not hashtag:
        raise HTTPException(status_code=400, detail="Hashtag tidak boleh kosong.")

    logger.info(f"[API:IG] POST /instagram/crawl/hashtag | hashtag=#{hashtag}")
    try:
        result = await asyncio.to_thread(
            crawl_instagram_hashtag,
            hashtag,
            request.max_posts,
        )
        return result
    except Exception as e:
        logger.error(f"[API:IG] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Quick Access — File Terbaru
# ============================================================

@router.get(
    "/latest/username",
    response_model=Dict[str, Any],
    summary="File terbaru — crawling username Instagram",
)
async def get_latest_username_result():
    """
    Mengambil hasil crawling **username terbaru** Instagram secara langsung (full data).

    Response menyertakan field `crawled_at` sebagai tanggal crawling.
    """
    result = get_latest_crawl_result("instagram", "comment")
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Belum ada data crawling username Instagram.",
        )
    return result


@router.get(
    "/latest/hashtag",
    response_model=Dict[str, Any],
    summary="File terbaru — crawling hashtag Instagram",
)
async def get_latest_hashtag_result():
    """
    Mengambil hasil crawling **hashtag terbaru** Instagram secara langsung (full data).

    Response menyertakan field `crawled_at` sebagai tanggal crawling.
    """
    result = get_latest_crawl_result("instagram", "hashtag")
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Belum ada data crawling hashtag Instagram.",
        )
    return result
