from pydantic import BaseModel


class ProfileIn(BaseModel):
    """Editable user profile fields (README §8).

    `age_band` is one of `<25`, `25–34`, `35–44`, `45+`; `occupation` is one of
    Student / Office worker / Self-employed / Researcher / Homemaker / Other.
    Kept as free `str` for MVP robustness — the frontend supplies fixed options.
    """

    postcode_area: str
    age_band: str
    occupation: str
    interests: str


class ProfileOut(ProfileIn):
    updated_at: str
