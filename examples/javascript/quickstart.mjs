// Hepsiemlak API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs kadikoy

const HOST = 'hepsiemlak-turkish-property-api.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Hepsiemlak API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const county = process.argv[2] ?? 'kadikoy';

// Flats (daire) for sale (satilik) in an Istanbul county, newest first.
const page = await get('/search-property', {
  main_category: 'konut',
  category: 'satilik',
  sub_category: 'daire',
  city: 'istanbul',
  counties: county,
  sort: 'newest',
});
console.log(`${page.page.totalElements} flats for sale in ${county}`);

// Rows hold a listing (realty) or a new-build project card (project); keep the listings.
for (const { realty } of page.content.filter((row) => row.realty)) {
  const [price] = realty.price;
  const [gross] = realty.sqm.grossSqm;
  const perM2 = gross ? Math.round(price / gross).toLocaleString('en-US') : '-';
  console.log(`${price.toLocaleString('en-US')} TL  ${realty.roomAndLivingRoom[0]}  ${gross} m2  ${perM2} TL/m2  ${realty.district.name}`);
}
