"""Minimal client for the Hepsiemlak API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os
import re
from statistics import median

import requests

HOST = "hepsiemlak-turkish-property-api.p.rapidapi.com"
SITE = "https://www.hepsiemlak.com/"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def listings(content):
    """The listing cards of a search page.

    Each row holds either `realty` (a listing) or `project` (a new-build project card with
    a price range), never both. Project rows are skipped here.
    """
    return [row["realty"] for row in content if row.get("realty")]


def first(value):
    """Prices, gross areas and room counts on search cards are one-item lists."""
    if isinstance(value, list):
        return value[0] if value else None
    return value


def unique_listings(cards):
    """The same flat is often listed by several offices. Keep one card per
    (district, rooms, gross m2, net m2, floor, price)."""
    seen, out = set(), []
    for c in cards:
        key = (
            c["district"]["name"],
            first(c["roomAndLivingRoom"]),
            first(c["sqm"]["grossSqm"]),
            c["sqm"]["netSqm"],
            c["floor"]["name"],
            first(c["price"]),
        )
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


def attributes(details):
    """`realtyAttributes` is a list of Turkish label/value text pairs. Return a dict."""
    return {a["name"]: a["value"] for a in details.get("realtyAttributes") or []}


def lira(text):
    """'85000 TL' or '12.750.000 TL' to an int, or None. Dots are thousands separators."""
    digits = re.sub(r"[^\d]", "", text or "")
    return int(digits) if digits else None


def net_sqm(details):
    """Net area from the 'Brüt / Net m2' attribute ('90 m2 / 60 m2')."""
    found = re.findall(r"(\d+)\s*m2", attributes(details).get("Brüt / Net m2", ""))
    return int(found[1]) if len(found) > 1 else None


def middle(values):
    values = [v for v in values if v]
    return median(values) if values else None
