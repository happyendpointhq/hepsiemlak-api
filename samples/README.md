# Sample responses

Real `200` responses from four Hepsiemlak API endpoints, taken on 4 November 2026 for
Kadıköy, Istanbul. The search page is cut to four rows (three listings and one new-build
project card), and the listing office, its staff, phone numbers and the free-text
description are removed. The agency group is removed from the autocomplete response. Field
names and values are otherwise unchanged. File names follow the endpoint path.

Privacy review (4 Nov 2026): the listing's `mapLocation` coordinates in `property-details.json` are rounded to three decimals (about 100 m).

| File | Request |
|---|---|
| `locations-autocomplete.json` | `GET /locations-autocomplete?keyword=kadikoy` |
| `search-property.json` | `GET /search-property?main_category=konut&category=satilik&sub_category=daire&city=istanbul&counties=kadikoy&sort=newest&page=1&size=20` |
| `property-details.json` | `GET /property-details?listing_id=172049-46` |
| `price-index.json` | `GET /price-index?city_id=34` |

They are useful for writing parsers and tests before you subscribe. Listings and prices
change daily, so do not hard-code these values.
