from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float


class CaptionNode(BaseModel):
    text: str
    bbox: Optional[BoundingBox] = None


class ImageNode(BaseModel):
    path: str
    bbox: Optional[BoundingBox] = None
    captions: List[CaptionNode] = Field(default_factory=list)


class ArticleNode(BaseModel):
    article_id: str
    headline: str
    bbox: Optional[BoundingBox] = None
    body_blocks: List[str] = Field(default_factory=list)
    images: List[ImageNode] = Field(default_factory=list)
    captions: List[CaptionNode] = Field(default_factory=list)


class PageNode(BaseModel):
    page_number: int
    width: Optional[float] = None
    height: Optional[float] = None
    articles: List[ArticleNode] = Field(default_factory=list)
    ads: List[str] = Field(default_factory=list)
    headers: List[str] = Field(default_factory=list)


class ParseQuality(BaseModel):
    status: str = "success"
    parser: str = "mineru"
    warnings: List[str] = Field(default_factory=list)


class ParseResponse(BaseModel):
    document_id: str
    pages: List[PageNode] = Field(default_factory=list)
    quality: ParseQuality = Field(default_factory=ParseQuality)
