"""FIFA World Cup 2026 knowledge base (teams, players, stadiums, fixtures)."""

TOURNAMENT = {
    "name": "FIFA World Cup 2026",
    "hosts": ["United States", "Canada", "Mexico"],
    "teams": 48,
    "dates": "11 June - 19 July 2026",
    "slogan": "We Are 26",
}

TEAMS = [
    {"name": "Argentina",   "flag": "🇦🇷", "group": "C", "colors": [(117, 170, 219), (255, 255, 255)], "rank": 1,  "nickname": "La Albiceleste"},
    {"name": "France",      "flag": "🇫🇷", "group": "F", "colors": [(0, 35, 149), (237, 41, 57)],      "rank": 2,  "nickname": "Les Bleus"},
    {"name": "Spain",       "flag": "🇪🇸", "group": "B", "colors": [(170, 21, 27), (241, 191, 0)],     "rank": 3,  "nickname": "La Roja"},
    {"name": "England",     "flag": "🏴", "group": "D", "colors": [(255, 255, 255), (207, 8, 31)],     "rank": 4,  "nickname": "Three Lions"},
    {"name": "Brazil",      "flag": "🇧🇷", "group": "C", "colors": [(0, 156, 59), (255, 223, 0)],      "rank": 5,  "nickname": "Selecao"},
    {"name": "Portugal",    "flag": "🇵🇹", "group": "E", "colors": [(0, 102, 0), (255, 0, 0)],         "rank": 6,  "nickname": "Selecao das Quinas"},
    {"name": "Netherlands", "flag": "🇳🇱", "group": "A", "colors": [(255, 102, 0), (33, 70, 139)],     "rank": 7,  "nickname": "Oranje"},
    {"name": "Croatia",     "flag": "🇭🇷", "group": "D", "colors": [(255, 0, 0), (255, 255, 255)],     "rank": 8,  "nickname": "Vatreni"},
    {"name": "Germany",     "flag": "🇩🇪", "group": "B", "colors": [(0, 0, 0), (221, 0, 0)],           "rank": 9,  "nickname": "Die Mannschaft"},
    {"name": "Belgium",     "flag": "🇧🇪", "group": "F", "colors": [(0, 0, 0), (253, 218, 36)],        "rank": 10, "nickname": "Red Devils"},
    {"name": "USA",         "flag": "🇺🇸", "group": "D", "colors": [(10, 49, 97), (179, 25, 66)],      "rank": 11, "nickname": "Stars and Stripes"},
    {"name": "Mexico",      "flag": "🇲🇽", "group": "A", "colors": [(0, 104, 71), (206, 17, 38)],      "rank": 14, "nickname": "El Tri"},
    {"name": "Uruguay",     "flag": "🇺🇾", "group": "E", "colors": [(124, 185, 232), (0, 20, 137)],    "rank": 15, "nickname": "La Celeste"},
    {"name": "Austria",     "flag": "🇦🇹", "group": "C", "colors": [(237, 41, 57), (255, 255, 255)],   "rank": 22, "nickname": "Das Team"},
    {"name": "Canada",      "flag": "🇨🇦", "group": "A", "colors": [(255, 0, 0), (255, 255, 255)],     "rank": 28, "nickname": "Les Rouges"},
    {"name": "Australia",   "flag": "🇦🇺", "group": "D", "colors": [(0, 132, 61), (255, 205, 0)],      "rank": 24, "nickname": "Socceroos"},
    {"name": "Paraguay",    "flag": "🇵🇾", "group": "D", "colors": [(213, 43, 30), (0, 56, 168)],      "rank": 36, "nickname": "La Albirroja"},
    {"name": "Turkey",      "flag": "🇹🇷", "group": "D", "colors": [(227, 10, 23), (255, 255, 255)],   "rank": 26, "nickname": "Ay-Yildizlilar"},
]

PLAYERS = [
    {"name": "Lionel Messi",      "team": "Argentina", "pos": "Forward",    "age": 38, "number": 10,
     "stats": {"caps": 191, "goals": 112, "assists": 58},
     "facts": ["8-time Ballon d'Or winner", "Led Argentina to the 2022 World Cup title", "All-time top scorer for Argentina"]},
    {"name": "Kylian Mbappe",     "team": "France",    "pos": "Forward",    "age": 27, "number": 10,
     "stats": {"caps": 86, "goals": 48, "assists": 30},
     "facts": ["World Cup winner in 2018 at age 19", "Scored a hat-trick in the 2022 final", "One of the fastest players in football"]},
    {"name": "Lamine Yamal",      "team": "Spain",     "pos": "Winger",     "age": 18, "number": 19,
     "stats": {"caps": 25, "goals": 9, "assists": 14},
     "facts": ["Euro 2024 champion as a teenager", "Youngest goalscorer in Euros history", "La Masia academy product"]},
    {"name": "Jude Bellingham",   "team": "England",   "pos": "Midfielder", "age": 22, "number": 10,
     "stats": {"caps": 42, "goals": 8, "assists": 9},
     "facts": ["Real Madrid midfield engine", "His #22 shirt was retired at Birmingham City", "Won the Champions League in 2024"]},
    {"name": "Vinicius Junior",   "team": "Brazil",    "pos": "Winger",     "age": 25, "number": 7,
     "stats": {"caps": 40, "goals": 6, "assists": 8},
     "facts": ["Champions League final scorer in 2024", "Known for electric dribbling", "Real Madrid's left-wing talisman"]},
    {"name": "Cristiano Ronaldo", "team": "Portugal",  "pos": "Forward",    "age": 41, "number": 7,
     "stats": {"caps": 217, "goals": 138, "assists": 47},
     "facts": ["All-time top scorer in men's international football", "5-time Ballon d'Or winner", "Played in a record number of World Cups"]},
    {"name": "Harry Kane",        "team": "England",   "pos": "Striker",    "age": 32, "number": 9,
     "stats": {"caps": 105, "goals": 69, "assists": 20},
     "facts": ["England's all-time top scorer", "2018 World Cup Golden Boot winner", "Lethal from open play and penalties"]},
    {"name": "Christian Pulisic", "team": "USA",       "pos": "Winger",     "age": 27, "number": 10,
     "stats": {"caps": 78, "goals": 32, "assists": 25},
     "facts": ["Captain America of US soccer", "First American to score in a Champions League knockout", "Face of the US team on home soil"]},
]

STADIUMS = [
    {"name": "MetLife Stadium", "city": "New York / New Jersey", "country": "USA", "capacity": 82500, "opened": 2010,
     "architecture": "Modern bowl with a dual-team aluminium-louvre facade that lights up in team colours.",
     "note": "Hosts the 2026 World Cup Final."},
    {"name": "Estadio Azteca", "city": "Mexico City", "country": "Mexico", "capacity": 87000, "opened": 1966,
     "architecture": "Iconic concrete bowl, one of the largest and most storied stadiums in the world.",
     "note": "Only stadium to host three different World Cups (1970, 1986, 2026)."},
    {"name": "SoFi Stadium", "city": "Los Angeles", "country": "USA", "capacity": 70000, "opened": 2020,
     "architecture": "Translucent ETFE canopy roof and a 360-degree dual-sided videoboard (the Infinity Screen).",
     "note": "Most expensive stadium ever built."},
    {"name": "AT&T Stadium", "city": "Dallas", "country": "USA", "capacity": 80000, "opened": 2009,
     "architecture": "Retractable roof with a huge column-free interior and a giant centre-hung screen.",
     "note": "Nicknamed 'Jerry World'."},
    {"name": "BC Place", "city": "Vancouver", "country": "Canada", "capacity": 54500, "opened": 1983,
     "architecture": "Cable-supported retractable fabric roof, the largest of its kind in the world.",
     "note": "Vancouver's downtown waterfront landmark."},
    {"name": "Estadio BBVA", "city": "Monterrey", "country": "Mexico", "capacity": 53500, "opened": 2015,
     "architecture": "Steel-lattice 'El Gigante de Acero' framing views of the Cerro de la Silla mountain.",
     "note": "Praised as one of Latin America's best venues."},
]

FIXTURES = [
    {"home": "England",   "away": "Croatia",     "group": "D", "date": "2026-06-18", "venue": "AT&T Stadium"},
    {"home": "Argentina", "away": "Austria",     "group": "C", "date": "2026-06-19", "venue": "MetLife Stadium"},
    {"home": "Brazil",    "away": "Argentina",   "group": "C", "date": "2026-06-22", "venue": "Estadio Azteca"},
    {"home": "France",    "away": "Belgium",     "group": "F", "date": "2026-06-20", "venue": "SoFi Stadium"},
    {"home": "Spain",     "away": "Germany",     "group": "B", "date": "2026-06-21", "venue": "BC Place"},
    {"home": "USA",       "away": "Australia",   "group": "D", "date": "2026-06-23", "venue": "SoFi Stadium"},
    {"home": "Portugal",  "away": "Uruguay",     "group": "E", "date": "2026-06-24", "venue": "Estadio BBVA"},
    {"home": "Mexico",    "away": "Netherlands", "group": "A", "date": "2026-06-25", "venue": "Estadio Azteca"},
]

GROUPS = {
    "A": ["Mexico", "Netherlands", "Canada"],
    "B": ["Spain", "Germany"],
    "C": ["Argentina", "Brazil", "Austria"],
    "D": ["England", "Croatia", "USA", "Australia", "Paraguay", "Turkey"],
    "E": ["Portugal", "Uruguay"],
    "F": ["France", "Belgium"],
}

TEAM_BY_NAME = {t["name"]: t for t in TEAMS}
PLAYER_BY_NAME = {p["name"]: p for p in PLAYERS}
STADIUM_BY_NAME = {s["name"]: s for s in STADIUMS}


def team_color(name, i=0):
    t = TEAM_BY_NAME.get(name)
    return t["colors"][i % len(t["colors"])] if t else (26, 115, 232)


def team_flag(name):
    t = TEAM_BY_NAME.get(name)
    return t["flag"] if t else "⚽"


def nearest_team_by_color(rgb):
    """Map a detected jersey colour to the closest national team (jersey recognition)."""
    best, bestd = None, 1e9
    for t in TEAMS:
        for c in t["colors"]:
            d = sum((a - b) ** 2 for a, b in zip(rgb, c))
            if d < bestd:
                bestd, best = d, t["name"]
    return best
