"""Check one Hepsiemlak listing against its county: price per m2 and gross rental yield.

    python yield_check.py 172049-46

Two calls: /property-details for the listing, then /price-index for its county, which
gives Hepsiemlak's median sale and rent prices per m2 there. The yield uses the rent the
listing states ("Kira Getirisi") when it has one, and the county's median rent per m2
otherwise. A first screen, not a valuation.
"""

import sys

from client import attributes, get, lira, net_sqm

listing_id = sys.argv[1] if len(sys.argv) > 1 else "172049-46"

d = get("/property-details", listing_id=listing_id)
attrs = attributes(d)
address = d["address"]
price, gross, net = d["price"], d.get("grossSqm"), net_sqm(d)
place = f"{address['district']['name']}, {address['county']['name']}, {address['city']['name']}"
print(f"{d['title']}\n{place}: {price:,} {d['currency']}, {gross} m2 gross / {net or '?'} m2 net\n")

index = get("/price-index", city_id=address["city"]["id"], county_id=address["county"]["id"])
sale_m2, rent_m2 = index["medianSalesPricePerSqm"], index["medianRentalPricePerSqm"]
print(f"County medians: {sale_m2:,.0f} TL/m2 to buy, {rent_m2:,.0f} TL/m2 a month to rent")
print(f"  Hepsiemlak amortisation: {index['amortisation']} years")

# Hepsiemlak does not say whether its index is per gross or net m2, so show both.
for label, area in (("gross", gross), ("net", net)):
    if area:
        per_m2 = price / area
        print(f"  This listing per {label} m2: {per_m2:,.0f} TL ({per_m2 / sale_m2 - 1:+.0%} vs county median)")

stated = lira(attrs.get("Kira Getirisi"))
if stated:
    rent, source = stated, "rent stated in the listing"
else:
    rent, source = rent_m2 * (gross or 0), "county median rent per m2 x gross m2"
if rent:
    print(f"\nMonthly rent: {rent:,.0f} TL ({source})")
    print(f"Gross yield: {rent * 12 / price:.1%}, {price / (rent * 12):.1f} years of rent to repay the price")
fee = lira(attrs.get("Aidat"))
if fee:
    print(f"Building fee (aidat): {fee:,} TL a month")

# One series per level in dataAxes: the city first, then the county. Take the last one.
series = index["salesSqmPriceDataSet"]["monthly"]
axis, months = series["dataAxes"][-1], series["timeAxes"]
values = axis["data"]
if len(values) > 1:
    change = values[-1] / values[0] - 1
    print(
        f"\n{axis['name']} sale price per m2, {months[0]['month']}/{months[0]['year']} to "
        f"{months[-1]['month']}/{months[-1]['year']}: {values[0]:,.0f} to {values[-1]:,.0f} TL ({change:+.0%})"
    )
