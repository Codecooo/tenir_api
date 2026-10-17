from typing import List, Optional

from ninja import Field, FilterSchema, ModelSchema, Schema

from mountain.models import DifficultyLevel, Mountain, MountainPicture


class MountainPictureOut(ModelSchema):
    class Meta:
        model = MountainPicture
        fields = ["id", "image", "description"]


class MountainListOut(ModelSchema):
    """Ringkas, dipakai untuk daftar gunung (tanpa deskripsi & galeri)."""

    class Meta:
        model = Mountain
        fields = [
            "id",
            "name",
            "location",
            "region",
            "height",
            "difficulty_level",
            "alert_level",
            "main_image",
            "is_favorite",
            "is_volcanic_active",
            "indonesian_weekday_price",
            "indonesian_weekend_price",
            "international_weekday_price",
            "international_weekend_price",
        ]


class MountainDetailOut(ModelSchema):
    """Lengkap, dipakai untuk halaman detail gunung beserta galeri foto."""

    pictures: List[MountainPictureOut]

    class Meta:
        model = Mountain
        fields = [
            "id",
            "name",
            "location",
            "description",
            "region",
            "height",
            "difficulty_level",
            "alert_level",
            "main_image",
            "is_favorite",
            "is_volcanic_active",
            "indonesian_weekday_price",
            "indonesian_weekend_price",
            "international_weekday_price",
            "international_weekend_price",
        ]


class MountainFilter(FilterSchema):
    region: Optional[str] = Field(None, q="region__iexact")
    difficulty: Optional[DifficultyLevel] = Field(None, q="difficulty_level")


class ErrorOut(Schema):
    detail: str