import base64
import pandas as pd
import pycountry
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

_ISO3_OVERRIDES = {
    "US": "USA",
    "South Korea": "KOR",
    "North Korea": "PRK",
    "Taiwan*": "TWN",
    "Russia": "RUS",
    "Iran": "IRN",
    "Syria": "SYR",
    "Tanzania": "TZA",
    "Venezuela": "VEN",
    "Moldova": "MDA",
    "Vietnam": "VNM",
    "Brunei": "BRN",
    "Bolivia": "BOL",
    "Laos": "LAO",
    "Congo (Kinshasa)": "COD",
    "Congo (Brazzaville)": "COG",
    "West Bank and Gaza": "PSE",
    "Burma": "MMR",
    "Kosovo": "XKX",
}


def _to_iso3(name: str) -> str | None:
    if name in _ISO3_OVERRIDES:
        return _ISO3_OVERRIDES[name]
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(BASE_DIR / "data" / "processed" / "covid_tratado.csv")
    df["iso_alpha"] = df["country_region"].apply(_to_iso3)
    return df


def get_base64(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
