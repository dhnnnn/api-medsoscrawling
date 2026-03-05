"""
Router: Crawling TikTok
Endpoint untuk menjalankan proses crawling pada platform TikTok.
"""

import asyncio
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from typing import Dict, Any

from ...schemas.models import TikTokCrawlRequest, HashtagCrawlRequest, CrawlResult
from ...services.crawler_service import crawl_tiktok_profile, crawl_tiktok_hashtag
from ...utils import get_latest_crawl_result
from ..deps import get_api_key

router = APIRouter(
    prefix="/tiktok",
    tags=["Crawling TikTok"],
    dependencies=[Depends(get_api_key)],
)

# ============================================================
# Crawl Actions
# ============================================================

@router.post("/crawl/username", response_model=CrawlResult, summary="Crawl komentar TikTok by username")
async def crawl_profile(request: TikTokCrawlRequest) -> CrawlResult:
    """
    Crawl komentar dari profil TikTok berdasarkan **username** (tanpa @) atau URL profil.

    Hasil crawling disimpan otomatis di `data/crawling/tiktok/comment/`.
    """
    if not request.target.strip():
        raise HTTPException(status_code=400, detail="Target tidak boleh kosong.")

    logger.info(f"[API:TT] POST /tiktok/crawl/username | target={request.target}")
    try:
        result = await asyncio.to_thread(
            crawl_tiktok_profile,
            request.target.strip(),
            request.max_posts,
        )
        return result
    except Exception as e:
        logger.error(f"[API:TT] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crawl/hashtag", response_model=CrawlResult, summary="Crawl komentar TikTok by hashtag")
async def crawl_hashtag(request: HashtagCrawlRequest) -> CrawlResult:
    """
    Crawl postingan dan komentar dari TikTok berdasarkan **hashtag**.

    Hasil crawling disimpan otomatis di `data/crawling/tiktok/hashtag/`.
    """
    hashtag = request.hashtag.strip().lstrip("#")
    if not hashtag:
        raise HTTPException(status_code=400, detail="Hashtag tidak boleh kosong.")

    logger.info(f"[API:TT] POST /tiktok/crawl/hashtag | hashtag=#{hashtag}")
    try:
        result = await asyncio.to_thread(
            crawl_tiktok_hashtag,
            hashtag,
            request.max_posts,
        )
        return result
    except Exception as e:
        logger.error(f"[API:TT] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Quick Access — File Terbaru
# ============================================================

@router.get(
    "/latest/username",
    response_model=Dict[str, Any],
    summary="File terbaru — crawling username TikTok",
)
async def get_latest_username_result():
    """
    Mengambil hasil crawling **username terbaru** TikTok secara langsung (full data).

    Response menyertakan field `crawled_at` sebagai tanggal crawling.
    """
    result = get_latest_crawl_result("tiktok", "comment")
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Belum ada data crawling username TikTok.",
        )
    return result


@router.get(
    "/latest/hashtag",
    response_model=Dict[str, Any],
    summary="File terbaru — crawling hashtag TikTok",
)
async def get_latest_hashtag_result():
    """
    Mengambil hasil crawling **hashtag terbaru** TikTok secara langsung (full data).

    Response menyertakan field `crawled_at` sebagai tanggal crawling.
    """
    result = get_latest_crawl_result("tiktok", "hashtag")
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Belum ada data crawling hashtag TikTok.",
        )
    return result
