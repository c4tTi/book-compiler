# 2. The route, travel times and maps

Confidence: ✅ well established · ⚠️ contested or weakly supported · 🔎 verify before relying on it

## 2.1 Shape of the route

- From Chang'an the road runs west through the Hexi (Gansu) Corridor via Liangzhou (Wuwei), Ganzhou, Suzhou and Guazhou to Dunhuang ✅ [@unesco-1442; @hansen2012].
- Beyond Dunhuang the routes split around the Taklamakan: **north** via Yizhou (Hami) and Xizhou (Gaochang, near Turfan), then Karashahr, Kucha, Aksu, and either over the Tianshan to Suyab and the Chu/Talas valleys or on to Kashgar; **south** via Khotan and Yarkand to Kashgar ✅ [@whe-map8; @unesco-1442].
- From Kashgar or Suyab the road crosses to Ferghana or to Chach (Tashkent) and down the Zarafshan valley to Samarkand; Bukhara lies further west ✅ [@bdk-xuanzang; @hansen2012].
- The UNESCO "Chang'an–Tianshan Corridor" World Heritage listing (2014) covers 33 sites on the northern line: Chang'an palaces, Qocho, Kizil, Suyab (Ak-Beshim), beacon towers and posthouses ✅ [@unesco-1442]. Its nomination dossier has detailed site maps 🔎 (site blocked our fetch).
- Xuanzang's 7th-century route (Turfan–Kucha–Bedel pass–Issyk Kul–Suyab–Talas–Chach–Samarkand) is the best-described version of the northern route, a century before 750 [@bdk-xuanzang]. Hyecho came the other way c. 727, via the Pamirs, Wakhan and Kashgar to Kucha [@hyecho; @yang1984].

## 2.2 How fast did people move?

- **Official Tang rates** (attributed to the *Tang Liudian*): about 70 li a day on horseback, 50 on foot or by donkey, 30 by cart; post stations roughly every 30 li; 1,639 stations empire-wide ⚠️ (reported by secondary sites; check a scholarly treatment of the *Tang Liudian*) [@chiculture-posts; @wotc-driving; @tangliudian].
- **Caravans** were small in the Tang: "often a dozen people or so", sometimes grouping into about 50 for dangerous stretches; the legends of 500-merchant caravans are Buddhist stereotypes ✅ [@hansen2005].
- **Camel caravans** covered roughly 25–40 km a day on popular estimates ⚠️ (tourism-grade sources only; no scholarly figure found) [@fad-caravans].
- **Estimated journey**, Chang'an → Samarkand on the northern route (≈4,600 km, rough modern estimate 🔎), computed in `workbench/travel.py`:

| Mode | Days incl. 1 rest day per 4 | ≈ Months |
|---|---|---|
| Official horse rate (70 li) | 151 | 5.0 |
| Foot/donkey (50 li) | 212 | 7.1 |
| Cart (30 li) | 353 | 11.8 |
| Camel caravan, slow (24 km) | 239 | 8.0 |
| Camel caravan, fast (32 km) | 179 | 6.0 |

Sensitivity for a slow caravan: 153–366 days depending on distance error (±20%) and waiting time. Waits of days or weeks for snow on passes are normal 🔎 [@fad-caravans]. **For a novel: six to twelve months one way is defensible; a year with trading stops is safest.**

- **Paperwork shapes the journey.** Each pass required inspecting the *guosuo* travel permit, listing every person and animal. Deviating from the stated itinerary required a new permit ✅ [@hansen2005; @emco-passport].

## 2.3 Landscape and environment

- Oasis cities are islands of irrigated farmland: wheat, barley, millet, grapes and fruit ✅ [@penn-tarimfood; @hansen2005].
- For visual reference of the landscapes before modern development, the NHK/CCTV 1980 series follows Xi'an → Pamirs in 12 episodes ✅ [@nhk1980].
- ⚠️ Climate: paleoclimate work has been used to re-read Uyghur–Tang relations (drought and steppe stress). Not added as a source; search "Uyghur Empire paleoclimate" to follow up.

## 2.4 Cities you will need (c. 750)

| City | Who controlled it c. 750 | What it's good for in a story | Sources |
|---|---|---|---|
| Chang'an | Tang capital; 1 million people ⚠️; walled wards with night curfew; East and West markets | Departure; the West Market's foreign quarter | [@heng2014; @heng1999; @wp-anlushan] |
| Liangzhou (Wuwei) | Tang; old Sogdian colony led by the An family as *sabao* | Sogdian community, horses | [@rong-newlight; @wp-sabao] |
| Dunhuang (Shazhou) | Tang; Mogao caves | Monasteries, scribes, painters | [@rong2013; @digitaldunhuang] |
| Xizhou (Gaochang/Turfan) | Tang prefecture since 640 | Markets, contracts, the Astana documents | [@hansen2005; @hansenrong2013] |
| Kucha | Seat of Anxi; Tocharian-speaking Buddhist kingdom | Army HQ, musicians, Kizil caves | [@wp-anxi; @spp085; @cetom] |
| Khotan | Garrison; Vijaya kings | Jade, silk, Buddhism | [@wp-khotan; @isaw-khotan] |
| Suyab | Turgesh then Tang-razed (748), Karluk later | Steppe city, Li Bai's supposed birthplace 🔎 | [@wp-turgesh; @unesco-1442] |
| Samarkand | Ikhshid Turgar under Abbasid-aligned Khurasan | Sogdian capital, Afrasiab palace murals | [@wp-turgar; @wp-afrasiab] |
| Panjikent | Sogdian town, sacked 722, reoccupied till c. 770s 🔎 | Best-excavated Sogdian houses and murals | [@marshak2002; @grenet2002] |

## 2.5 Maps and GIS

- **CHGIS** (Harvard/Fudan): free GIS of Tang prefectures and place names ✅ [@chgis].
- **OWTRAD** (Ciolek): georeferenced historical route data incl. NW China 100–1400 CE, CC BY-NC ✅ (site down at time of check) [@owtrad].
- **World History Encyclopedia** late-8th-century route map (quick visual) [@whe-map8].
- **Smithsonian Sogdians** exhibition has an interactive map [@si-sogdians].
- **Usmanova & Antonov** reconstruct the Talas battlefield landscape and troop routes (Russian, with map) [@usmanova2024].
- **Benkato's** mapping of the Mount Mugh letters locates early-8th-century Sogdian places [@benkato-mugh].

## Purpose note

- **Essential:** the route sequence, realistic journey length (6–12 months), permit checks, small caravans.
- **Optional:** exact stage distances (only if the plot hinges on days); GIS layers.
- **Cut:** the maritime route (except for Du Huan's return by sea in 762).
