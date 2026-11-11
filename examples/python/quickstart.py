"""Newest flats for sale in an Istanbul county, then the full record of one.

    python quickstart.py kadikoy

Two calls: /search-property and /property-details. The county is Hepsiemlak's slug
(kadikoy, besiktas, uskudar...); /locations-autocomplete finds it for any place.
"""

import sys

from client import SITE, attributes, first, get, listings, unique_listings

county = sys.argv[1] if len(sys.argv) > 1 else "kadikoy"

page = get(
    "/search-property",
    main_category="konut",   # residential
    category="satilik",      # for sale (kiralik = for rent)
    sub_category="daire",    # flats
    city="istanbul",
    counties=county,
    sort="newest",
    size=20,
)
cards = listings(page["content"])
unique = unique_listings(cards)
print(f"{page['page']['totalElements']:,} flats for sale in {county}")
print(f"This page: {len(page['content'])} rows, {len(cards)} listings, {len(unique)} after removing repeats\n")

for c in unique[:10]:
    price, gross = first(c["price"]), first(c["sqm"]["grossSqm"])
    per_m2 = f"{price / gross:,.0f} TL/m2" if price and gross else "-"
    print(
        f"{price:>12,} {c['currency']['code']}  {first(c['roomAndLivingRoom']):<4} "
        f"{gross or '?':>4} m2 gross  {per_m2:>15}  age {c['age']:<3} {c['district']['name']}"
    )

listing = unique[0]
details = get("/property-details", listing_id=listing["listingId"])
attrs = attributes(details)
print(f"\n{details['title']}")
for label in ("Fiyat", "Brüt / Net m2", "Bulunduğu Kat", "Bina Yaşı", "Isınma Tipi", "Aidat", "Kira Getirisi", "Tapu Durumu"):
    if attrs.get(label):
        print(f"  {label}: {attrs[label]}")
address = details["address"]
print(f"  Location ids: city {address['city']['id']}, county {address['county']['id']}, district {address['district']['id']}")
print(f"  {SITE}{details['detailUrl']}")
