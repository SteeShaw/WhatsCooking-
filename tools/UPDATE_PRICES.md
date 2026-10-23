# Monthly price refresh

WhatsCooking keeps its Aldi and Sainsbury's prices inside `index.html`. This is the procedure for refreshing them. It only changes prices — never products, names, pack sizes or anything else in the app.

## Rules
- Read pages with WebFetch only. **Aldi blocks automated reading of page 2+ and search (robots.txt)** — read only the first page of each category below, and never work around a blocked page with curl, mirrors or caches.
- If a page can't be fetched, skip it; those products simply keep their current price.
- Prices: use the current shelf price (ignore "was" prices and Nectar-only prices).

## 1. Aldi — first page of each category
Ask WebFetch for every product as `name | pack size | price | url-slug (the part after /product/)`.

```
https://www.aldi.co.uk/products/fresh-food/poultry/k/1588161416978050004
https://www.aldi.co.uk/products/fresh-food/beef/k/1588161416978050005
https://www.aldi.co.uk/products/fresh-food/pork-gammon/k/1588161416978050006
https://www.aldi.co.uk/products/fresh-food/fish/k/1588161416978050011
https://www.aldi.co.uk/products/fresh-food/bacon-sausages/k/1588161416978050007
https://www.aldi.co.uk/products/fresh-food/fruit/k/1588161416978050001
https://www.aldi.co.uk/products/fresh-food/vegetables/k/1588161416978050002
https://www.aldi.co.uk/products/fresh-food/stir-fry-vegetables-sauce-noodles/k/1588161416978050003
https://www.aldi.co.uk/products/chilled-food/milk/k/1588161416978051001
https://www.aldi.co.uk/products/chilled-food/dairy/k/1588161416978051002
https://www.aldi.co.uk/products/chilled-food/eggs/k/1588161416978051003
https://www.aldi.co.uk/products/chilled-food/cheese/k/1588161416978051004
https://www.aldi.co.uk/products/chilled-food/yogurts/k/1588161416978051005
https://www.aldi.co.uk/products/bakery/bread/k/1588161416978049001
https://www.aldi.co.uk/products/bakery/wraps-naans-pittas-thins/k/1588161416978049007
https://www.aldi.co.uk/products/food-cupboard/cereals-snack-bars/k/1588161416978053002
https://www.aldi.co.uk/products/food-cupboard/biscuits-crackers/k/1588161416978053001
https://www.aldi.co.uk/products/food-cupboard/crisps-snacks/k/1588161416978053004
https://www.aldi.co.uk/products/food-cupboard/chocolate-sweets/k/1588161416978053003
https://www.aldi.co.uk/products/food-cupboard/jams-spreads-syrups/k/1588161416978053006
https://www.aldi.co.uk/products/food-cupboard/tins-cans-packets/k/1588161416978053012
https://www.aldi.co.uk/products/food-cupboard/rice-pasta-noodles/k/1588161416978053008
https://www.aldi.co.uk/products/food-cupboard/sauces-oils-dressings/k/1588161416978053010
https://www.aldi.co.uk/products/drinks/tea/k/1588161416978054001
https://www.aldi.co.uk/products/drinks/coffee/k/1588161416978054002
https://www.aldi.co.uk/products/drinks/soft-drinks-juices/k/1588161416978054004
https://www.aldi.co.uk/products/drinks/water/k/1588161416978054005
https://www.aldi.co.uk/products/frozen-food/vegetables-sides/k/1588161416978056004
https://www.aldi.co.uk/products/frozen-food/fish-seafood/k/1588161416978056002
https://www.aldi.co.uk/products/frozen-food/chips-potato/k/1588161416978056003
https://www.aldi.co.uk/products/frozen-food/ice-cream-desserts/k/1588161416978056009
https://www.aldi.co.uk/products/frozen-food/pizzas-garlic-bread/k/1588161416978056006
https://www.aldi.co.uk/products/home-essentials/toilet-roll-kitchen-roll-tissues/k/1588161416978059007
https://www.aldi.co.uk/products/home-essentials/house-cleaning/k/1588161416978059005
https://www.aldi.co.uk/products/home-essentials/dishwashing/k/1588161416978059003
https://www.aldi.co.uk/products/home-essentials/laundry/k/1588161416978059006
https://www.aldi.co.uk/products/home-essentials/food-bags-foil-cling-film/k/1588161416978059004
https://www.aldi.co.uk/products/health-beauty/dental-care/k/1588161416978058004
https://www.aldi.co.uk/products/health-beauty/bath-shower-soap/k/1588161416978058001
```

Lean Pork Fillet is sold by weight — record its **price per kg** against its slug (`ashfields-british-lean-pork-fillet-000000000000386133`).

## 2. Sainsbury's — fill-in items
Search `https://www.sainsburys.co.uk/gol-ui/SearchResults/<search>` and take the price of the product named. Key = the exact text in the left column.

| prices.json key | search |
|---|---|
| Sainsbury's Stir Fry Beef\|350g | beef stir fry strips |
| Sainsbury's Chorizo Ring Mild\|225g | cooking chorizo |
| Sainsbury's Red Onions\|3 pack | red onions |
| Sainsbury's Tenderstem Broccoli\|200g | tenderstem broccoli |
| Sainsbury's Tenderstem Broccoli\|330g | tenderstem broccoli |
| Sainsbury's Courgettes\|500g (≈2) | courgettes |
| Sainsbury's Spring Onions\|bunch | spring onion bunch |
| Sainsbury's Pak Choi\|250g (≈2) | pak choi bok choy |
| Sainsbury's Lighter Mature Cheese\|400g | lighter mature cheddar |
| Sainsbury's Cous Cous\|500g | couscous |
| Sainsbury's Spanish Paella Rice\|500g | paella rice |
| Sainsbury's Passata\|500g | passata |
| Sainsbury's Black Beans in Water\|400g tin | black beans |
| Sainsbury's Chickpeas in Water\|400g tin | chickpeas in water |
| Sainsbury's Coconut Milk Light\|400ml | light coconut milk |
| Sainsbury's Chicken Stock Cubes\|10 pack | chicken stock cubes |
| Sainsbury's Green Pesto\|190g jar | green pesto |
| Sainsbury's Fragrant Tikka Curry Paste\|200g jar | tikka paste |
| Sainsbury's Mild Salsa\|200g | salsa dip |
| Sainsbury's Edamame Beans (frozen)\|500g | edamame |

Some Sainsbury's searches occasionally return an empty page — retry once with the alternative wording, then skip.

## 3. Apply and publish
1. Write everything to `prices.json` (outside the repo, e.g. the scratchpad):
   `{"aldi": {"<slug>": price, …}, "sainsburys": {"<key>": price, …}}`
   Include every Aldi product you saw — the script ignores slugs the app doesn't use.
2. `python3 tools/update_prices.py /path/to/prices.json --date "<today, e.g. 1 Nov 2026>"`
3. Check the app still parses: extract the `<script>` block and run `node --check` on it.
4. If any single price moved by more than 50%, double-check it before keeping it.
5. Commit `index.html` with message `Monthly price refresh — <date>` and push to `main`. GitHub Pages republishes automatically.
6. Report: number of prices changed, the biggest rises and falls, and any pages that couldn't be read.
