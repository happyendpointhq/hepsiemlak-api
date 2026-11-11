# Hepsiemlak API and Scraper

The Hepsiemlak API returns Turkish real estate data from hepsiemlak.com as JSON: homes,
commercial property, land, timeshares and tourism businesses for sale and for rent across
Turkey's 81 provinces, with price, gross and net area, rooms, floor, building age, heating,
title deed status, monthly building fee and photos, plus Hepsiemlak's price index with
median sale and rent prices per square metre and their history for a province, county or
district. Hepsiemlak has no public API, so this REST API is the way to get its listings
into your own code without building and maintaining a Hepsiemlak scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/hepsiemlak-api?utm_source=github&utm_medium=readme&utm_campaign=hepsiemlak-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/hepsiemlak-turkish-property-api
- Product page: https://happyendpoint.com/library/hepsiemlak-api?utm_source=github&utm_medium=readme&utm_campaign=hepsiemlak-api
- Postman documentation: https://documenter.getpostman.com/view/56555678/2sBYHYud6u
- Postman collection (fork and run): https://www.postman.com/happyendpoints-team/hepsiemlak-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://hepsiemlak-turkish-property-api.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 12, all `GET` |
| Coverage | Turkey: provinces (`/cities`), counties and districts |
| Categories | Residential (`konut`), commercial (`isyeri`), land (`arsa`), timeshare (`devremulk`), tourism (`turistik-isletme`) |
| Deal types | For sale (`satilik`), for rent (`kiralik`), seasonal rent, transfer, and land-for-flat deals |
| Language | Listing text and attribute labels are Turkish; filter values are Turkish slugs |
| Page size | `size`, default 20, paged with `page` |
| Format | JSON, every response wrapped in `{"success": true, "data": ...}` |

---

## What data you get

**Search**
- Listings by category, deal type and sub-type (`daire` for flats, `villa`, `mustakil-ev` for detached houses), province, counties and districts
- Filters for rooms, bathrooms, building age, floor, heating, facing, occupancy, furnishing, balcony, lift, parking, garden, gated complex, listing date, price and gross or net area
- Eight sort orders, including newest and price per square metre
- Any search pasted as a hepsiemlak.com URL

**Listings**
- Price and currency, gross and net m2, rooms ("2+1"), bathrooms, floor and number of floors, building age, heating and fuel, title deed type, mortgage eligibility, monthly building fee (aidat), stated rental income, facing, photos and coordinates
- Province, county and district ids for each listing, and similar listings

**Market data and reference**
- Price index: median sale and rent price, and per m2, for a province, county or district, with Hepsiemlak's amortisation in years, monthly series for the last 12 months and annual series back to 2014
- Provinces, counties, districts, location autocomplete and the valid filter values for each category

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/hepsiemlak-turkish-property-api). Current plans are listed there. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

Flats (`daire`) for sale (`satilik`) in Kadıköy, Istanbul, newest first:

```bash
curl "https://hepsiemlak-turkish-property-api.p.rapidapi.com/search-property?main_category=konut&category=satilik&sub_category=daire&city=istanbul&counties=kadikoy&sort=newest" \
  -H "x-rapidapi-host: hepsiemlak-turkish-property-api.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

The price index for the same county (Istanbul is province 34, Kadıköy county 1421):

```bash
curl "https://hepsiemlak-turkish-property-api.p.rapidapi.com/price-index?city_id=34&county_id=1421" \
  -H "x-rapidapi-host: hepsiemlak-turkish-property-api.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py kadikoy
```

```python
from client import first, get, listings, unique_listings

page = get("/search-property", main_category="konut", category="satilik",
           sub_category="daire", city="istanbul", counties="kadikoy", sort="newest")
for card in unique_listings(listings(page["content"])):
    print(first(card["price"]), first(card["roomAndLivingRoom"]),
          first(card["sqm"]["grossSqm"]), card["district"]["name"], card["listingId"])

index = get("/price-index", city_id=34, county_id=1421)
print(index["medianSalesPricePerSqm"], index["medianRentalPricePerSqm"], index["amortisation"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs kadikoy
```

---

## Example response

`GET /price-index?city_id=34&county_id=1421`, trimmed to the headline figures and the first
and last month of one series (the `"..."` marks values left out). Taken on 4 November 2026. More responses are in
[`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "amortisation": 17,
    "medianRentalPrice": 91173.41897937183,
    "medianRentalPricePerSqm": 769.4605543843196,
    "medianSalesPrice": 19050035.82133368,
    "medianSalesPricePerSqm": 159058.48040921788,
    "salesSqmPriceDataSet": {
      "monthly": {
        "timeAxes": [{ "month": "11", "year": "2025" }, "...", { "month": "10", "year": "2026" }],
        "dataAxes": [
          { "name": "İstanbul", "type": "CITY", "data": [61743.36, "...", 76097.41] },
          { "name": "Kadıköy", "type": "COUNTY", "data": [133751.9, "...", 159058.48] }
        ]
      }
    }
  }
}
```

---

## Endpoints

Base URL: `https://hepsiemlak-turkish-property-api.p.rapidapi.com`

### Search

| Endpoint | Returns |
|---|---|
| `GET /search-property` | Listings by category, deal type, location and filters, with paging and eight sort orders |
| `GET /search-by-url` | The listings of a hepsiemlak.com search URL |

### Listings

| Endpoint | Returns |
|---|---|
| `GET /property-details` | The full record of one listing by its id (`172049-46`) |
| `GET /property-details-by-url` | The same record from a hepsiemlak.com listing URL |
| `GET /similar-properties` | Listings similar to a given one, as full cards |

### Locations and filters

| Endpoint | Returns |
|---|---|
| `GET /locations-autocomplete` | Locations, housing complexes, nearby places and projects matching a keyword, with the slugs searches take |
| `GET /cities` | All Turkish provinces with their ids |
| `GET /counties` | The counties of a province |
| `GET /districts` | The districts of a county |
| `GET /search-filters` | The valid filter values for a category and deal type |

### Market data

| Endpoint | Returns |
|---|---|
| `GET /price-index` | Median sale and rent prices and per m2, amortisation, and monthly and annual series for a province, county or district |
| `GET /status` | Service health |

---

## Things to know about the data

These come from running the examples against the API on 4 November 2026, for Kadıköy,
Istanbul. They are the mistakes that produce wrong numbers rather than errors.

- **A search row is a listing or a project.** Each row of `content` holds `realty` (a
  listing) or `project` (a new-build project card with a price range), and the other is
  `null`. One of the 20 rows in the Kadıköy search was a project. `client.listings()` keeps
  the listings.
- **The same flat is listed by several offices.** A 3+1, 128 m2 gross, 97 m2 net, first
  floor flat in Göztepe at 19,000,000 TL appeared three times on one page under three
  listing ids. Removing repeats took the page from 19 listings to 17
  (`client.unique_listings()`).
- **Search card values are one-item lists.** `price`, `sqm.grossSqm`, `room` and
  `roomAndLivingRoom` are lists such as `[16000000]` and `["3+1"]`, while `netSqm` is a plain
  number. The detail record uses plain values (`price: 12750000`, `roomAndLivingRoom: "2+1"`).
- **Gross and net area differ a lot.** The same 2+1 is 90 m2 gross and 60 m2 net. Price per
  m2 on gross area was 11% below the Kadıköy median; on net area it was 34% above.
  Hepsiemlak does not say which area its index uses, so `yield_check.py` shows both.
- **Details are Turkish label/value text.** `realtyAttributes` is a list such as
  `{"name": "Aidat", "value": "3000 TL"}` and `{"name": "Brüt / Net m2", "value": "90 m2 / 60 m2"}`.
  Prices use dots as thousands separators (`"12.750.000 TL"`). `client.attributes()` and
  `client.lira()` turn them into a dict and numbers. Some listings state their rental income
  ("Kira Getirisi", 85,000 TL on one Göztepe flat); most do not.
- **The price index series hold one row per level.** With `county_id`, each `dataAxes` list
  has the province first and the county second; the headline medians are the county's. Take
  the last row.
- **Amortisation is rounded and per m2.** Kadıköy's `amortisation: 17` matches the median sale
  price per m2 divided by twelve months of median rent per m2 (17.2), not the two median
  prices (17.4 here, 15.2 for all of Istanbul against its 14).
- **The figures are nominal lira.** The Istanbul sale price per m2 rose from 3,667 TL in
  October 2014 to 76,097 TL in October 2026, and 23% in the last twelve months. Adjust for
  inflation before comparing years.
- **Place names repeat.** `/locations-autocomplete` for "kadikoy" returned the Istanbul county
  (id 1421, slug `kadikoy`) and also Kadıköy neighbourhoods in Balıkesir, Yalova and Samsun.
  Use the county slug with `city=istanbul`, or the ids.
- **Building age 0 means new.** Several Kadıköy flats had `age: 0`, and floors are text
  ("Giriş Katı" is the ground floor, "Yüksek Giriş" a raised ground floor).

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Newest flats for sale in an Istanbul county with price per m2, repeats removed, then one listing's attributes and location ids |
| [`examples/python/yield_check.py`](examples/python/yield_check.py) | One listing against its county: price per gross and net m2 versus the county median, gross rental yield, building fee and the county's 12-month price change |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The quickstart in Node 18+, no dependencies |
| [`samples/`](samples/) | Real responses for four endpoints |

---

## API or your own Hepsiemlak scraper

A Hepsiemlak scraper you write yourself works until the site changes its pages, its internal
search calls or its bot protection, and then it returns nothing or the wrong fields. This API
returns the same listings and price index as documented JSON, so the work you keep is the
analysis, not the parser. If you need a one-off export or a recurring file rather than API
calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=hepsiemlak-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can search Hepsiemlak
without code:

```json
{
  "mcpServers": {
    "hepsiemlak": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: hepsiemlak-turkish-property-api.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Hepsiemlak API?

Hepsiemlak does not publish a public developer API for its listings. This API, built and
maintained by Happy Endpoint and independent of Hepsiemlak, returns hepsiemlak.com listings,
listing details, locations and the price index as REST and JSON.

### Can I get Turkish property prices per square metre?

Yes, two ways. `/price-index` returns Hepsiemlak's median sale and rent price per m2 for a
province, county or district, with monthly and annual history. Listings carry the price and
gross and net area, so you can compute your own medians, after removing the repeats.

### How do I calculate rental yield in Istanbul with the API?

Take a listing's price from `/property-details` and a rent: the listing's stated rental
income when it has one, or the county's `medianRentalPricePerSqm` from `/price-index` times
the area. [`yield_check.py`](examples/python/yield_check.py) does both and prints the gross
yield.

### Can I search Hepsiemlak in English?

The parameters are English, but their values are Turkish slugs (`konut`, `satilik`,
`kiralik`, `daire`) and listing text is Turkish. `/search-filters` lists the valid values for
each category, and `/locations-autocomplete` returns the slugs for places.

### How do I use the Hepsiemlak API in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI headers.
[`examples/python/client.py`](examples/python/client.py) is a short client with helpers for
search rows, repeats and Turkish attribute text, and the other scripts in that folder are
ready to run.

### Is there a free Hepsiemlak API?

Plans, including what each one allows, are on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/hepsiemlak-turkish-property-api),
where every endpoint can also be tested in the browser.

### Where is the documentation?

Every endpoint, parameter and response is documented on the RapidAPI listing, and the
endpoint tables above summarise them. Example responses are in [`samples/`](samples/).

---

## Related repos

- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [yad2-api](https://github.com/happyendpointhq/yad2-api) - Israel listings with registered sale prices
- [fotocasa-api](https://github.com/happyendpointhq/fotocasa-api) - Spanish property listings from Fotocasa
- [uae-real-estate-api](https://github.com/happyendpointhq/uae-real-estate-api) - asking versus paid prices in Dubai
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment research

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: hello@happyendpoint.com

## Licence

MIT. See [LICENSE](LICENSE).
