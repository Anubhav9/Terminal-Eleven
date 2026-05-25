"""
Static profile data for each of the 48 nations at the 2026 FIFA World Cup.

Schema per team:
    captain        — current senior-team captain
    coach          — current head coach / manager
    confederation  — AFC / CAF / CONCACAF / CONMEBOL / OFC / UEFA
    nickname       — popular team nickname
    best_finish    — best-ever World Cup result
    last_wc        — result at the 2022 World Cup (or "Did not qualify")

Keys must match the team names used in static_data/groups/*.py.
"""

TEAM_INFORMATION: dict[str, dict[str, str]] = {
    # ── Group A ────────────────────────────────────────────────
    "Mexico": {
        "captain": "Edson Álvarez",
        "coach": "Javier Aguirre",
        "confederation": "CONCACAF",
        "nickname": "El Tri",
        "best_finish": "Quarter-finals (1970, 1986)",
        "last_wc": "Group stage — 2022",
    },
    "South Africa": {
        "captain": "Ronwen Williams",
        "coach": "Hugo Broos",
        "confederation": "CAF",
        "nickname": "Bafana Bafana",
        "best_finish": "Group stage (1998, 2002, 2010)",
        "last_wc": "Did not qualify",
    },
    "South Korea": {
        "captain": "Son Heung-min",
        "coach": "Hong Myung-bo",
        "confederation": "AFC",
        "nickname": "Taegeuk Warriors",
        "best_finish": "Fourth place — 2002",
        "last_wc": "Round of 16 — 2022",
    },
    "Czechia": {
        "captain": "Tomáš Souček",
        "coach": "Ivan Hašek",
        "confederation": "UEFA",
        "nickname": "Národní tým",
        "best_finish": "Runners-up — 1934, 1962 (as Czechoslovakia)",
        "last_wc": "Did not qualify",
    },

    # ── Group B ────────────────────────────────────────────────
    "Canada": {
        "captain": "Alphonso Davies",
        "coach": "Jesse Marsch",
        "confederation": "CONCACAF",
        "nickname": "Les Rouges",
        "best_finish": "Group stage (1986, 2022)",
        "last_wc": "Group stage — 2022",
    },
    "Switzerland": {
        "captain": "Granit Xhaka",
        "coach": "Murat Yakin",
        "confederation": "UEFA",
        "nickname": "Nati",
        "best_finish": "Quarter-finals (1934, 1938, 1954)",
        "last_wc": "Round of 16 — 2022",
    },
    "Qatar": {
        "captain": "Akram Afif",
        "coach": "Bartolomé Márquez",
        "confederation": "AFC",
        "nickname": "Al-Annabi",
        "best_finish": "Group stage — 2022",
        "last_wc": "Group stage — 2022",
    },
    "Bosnia and Herzegovina": {
        "captain": "Edin Džeko",
        "coach": "Sergej Barbarez",
        "confederation": "UEFA",
        "nickname": "Zmajevi",
        "best_finish": "Group stage — 2014",
        "last_wc": "Did not qualify",
    },

    # ── Group C ────────────────────────────────────────────────
    "Brazil": {
        "captain": "Marquinhos",
        "coach": "Carlo Ancelotti",
        "confederation": "CONMEBOL",
        "nickname": "Seleção",
        "best_finish": "Winners (5x) — 1958, 1962, 1970, 1994, 2002",
        "last_wc": "Quarter-finals — 2022",
    },
    "Morocco": {
        "captain": "Romain Saïss",
        "coach": "Walid Regragui",
        "confederation": "CAF",
        "nickname": "Atlas Lions",
        "best_finish": "Fourth place — 2022",
        "last_wc": "Fourth place — 2022",
    },
    "Scotland": {
        "captain": "Andy Robertson",
        "coach": "Steve Clarke",
        "confederation": "UEFA",
        "nickname": "The Tartan Army",
        "best_finish": "Group stage (8 appearances)",
        "last_wc": "Did not qualify",
    },
    "Haiti": {
        "captain": "Frantzdy Pierrot",
        "coach": "Sébastien Migné",
        "confederation": "CONCACAF",
        "nickname": "Les Grenadiers",
        "best_finish": "Group stage — 1974",
        "last_wc": "Did not qualify",
    },

    # ── Group D ────────────────────────────────────────────────
    "United States": {
        "captain": "Christian Pulisic",
        "coach": "Mauricio Pochettino",
        "confederation": "CONCACAF",
        "nickname": "The Stars and Stripes",
        "best_finish": "Third place — 1930",
        "last_wc": "Round of 16 — 2022",
    },
    "Paraguay": {
        "captain": "Gustavo Gómez",
        "coach": "Gustavo Alfaro",
        "confederation": "CONMEBOL",
        "nickname": "La Albirroja",
        "best_finish": "Quarter-finals — 2010",
        "last_wc": "Did not qualify",
    },
    "Australia": {
        "captain": "Mat Ryan",
        "coach": "Tony Popovic",
        "confederation": "AFC",
        "nickname": "Socceroos",
        "best_finish": "Round of 16 (2006, 2022)",
        "last_wc": "Round of 16 — 2022",
    },
    "Turkiye": {
        "captain": "Hakan Çalhanoğlu",
        "coach": "Vincenzo Montella",
        "confederation": "UEFA",
        "nickname": "Ay-Yıldızlılar",
        "best_finish": "Third place — 2002",
        "last_wc": "Did not qualify",
    },

    # ── Group E ────────────────────────────────────────────────
    "Germany": {
        "captain": "Joshua Kimmich",
        "coach": "Julian Nagelsmann",
        "confederation": "UEFA",
        "nickname": "Die Mannschaft",
        "best_finish": "Winners (4x) — 1954, 1974, 1990, 2014",
        "last_wc": "Group stage — 2022",
    },
    "Ecuador": {
        "captain": "Enner Valencia",
        "coach": "Sebastián Beccacece",
        "confederation": "CONMEBOL",
        "nickname": "La Tri",
        "best_finish": "Round of 16 — 2006",
        "last_wc": "Group stage — 2022",
    },
    "Ivory Coast": {
        "captain": "Franck Kessié",
        "coach": "Emerse Faé",
        "confederation": "CAF",
        "nickname": "Les Éléphants",
        "best_finish": "Group stage (2006, 2010, 2014)",
        "last_wc": "Did not qualify",
    },
    "Curacao": {
        "captain": "Leandro Bacuna",
        "coach": "Dick Advocaat",
        "confederation": "CONCACAF",
        "nickname": "Familia Kòrsou",
        "best_finish": "Debutant — first WC in 2026",
        "last_wc": "Did not qualify",
    },

    # ── Group F ────────────────────────────────────────────────
    "Netherlands": {
        "captain": "Virgil van Dijk",
        "coach": "Ronald Koeman",
        "confederation": "UEFA",
        "nickname": "Oranje",
        "best_finish": "Runners-up (1974, 1978, 2010)",
        "last_wc": "Quarter-finals — 2022",
    },
    "Japan": {
        "captain": "Wataru Endō",
        "coach": "Hajime Moriyasu",
        "confederation": "AFC",
        "nickname": "Samurai Blue",
        "best_finish": "Round of 16 (2002, 2010, 2018, 2022)",
        "last_wc": "Round of 16 — 2022",
    },
    "Tunisia": {
        "captain": "Aïssa Laïdouni",
        "coach": "Sami Trabelsi",
        "confederation": "CAF",
        "nickname": "Eagles of Carthage",
        "best_finish": "Group stage (6 appearances)",
        "last_wc": "Group stage — 2022",
    },
    "Sweden": {
        "captain": "Victor Lindelöf",
        "coach": "Graham Potter",
        "confederation": "UEFA",
        "nickname": "Blågult",
        "best_finish": "Runners-up — 1958",
        "last_wc": "Did not qualify",
    },

    # ── Group G ────────────────────────────────────────────────
    "Belgium": {
        "captain": "Kevin De Bruyne",
        "coach": "Rudi Garcia",
        "confederation": "UEFA",
        "nickname": "Red Devils",
        "best_finish": "Third place — 2018",
        "last_wc": "Group stage — 2022",
    },
    "Iran": {
        "captain": "Ehsan Hajsafi",
        "coach": "Amir Ghalenoei",
        "confederation": "AFC",
        "nickname": "Team Melli",
        "best_finish": "Group stage (6 appearances)",
        "last_wc": "Group stage — 2022",
    },
    "Egypt": {
        "captain": "Mohamed Salah",
        "coach": "Hossam Hassan",
        "confederation": "CAF",
        "nickname": "The Pharaohs",
        "best_finish": "Group stage (1934, 1990, 2018)",
        "last_wc": "Did not qualify",
    },
    "New Zealand": {
        "captain": "Chris Wood",
        "coach": "Darren Bazeley",
        "confederation": "OFC",
        "nickname": "All Whites",
        "best_finish": "Group stage (1982, 2010)",
        "last_wc": "Did not qualify",
    },

    # ── Group H ────────────────────────────────────────────────
    "Spain": {
        "captain": "Álvaro Morata",
        "coach": "Luis de la Fuente",
        "confederation": "UEFA",
        "nickname": "La Roja",
        "best_finish": "Winners — 2010",
        "last_wc": "Round of 16 — 2022",
    },
    "Uruguay": {
        "captain": "José Giménez",
        "coach": "Marcelo Bielsa",
        "confederation": "CONMEBOL",
        "nickname": "La Celeste",
        "best_finish": "Winners (2x) — 1930, 1950",
        "last_wc": "Group stage — 2022",
    },
    "Saudi Arabia": {
        "captain": "Salem Al-Dawsari",
        "coach": "Hervé Renard",
        "confederation": "AFC",
        "nickname": "Green Falcons",
        "best_finish": "Round of 16 — 1994",
        "last_wc": "Group stage — 2022",
    },
    "Cape Verde": {
        "captain": "Ryan Mendes",
        "coach": "Pedro \"Bubista\" Brito",
        "confederation": "CAF",
        "nickname": "Tubarões Azuis",
        "best_finish": "Debutant — first WC in 2026",
        "last_wc": "Did not qualify",
    },

    # ── Group I ────────────────────────────────────────────────
    "France": {
        "captain": "Kylian Mbappé",
        "coach": "Didier Deschamps",
        "confederation": "UEFA",
        "nickname": "Les Bleus",
        "best_finish": "Winners (2x) — 1998, 2018",
        "last_wc": "Runners-up — 2022",
    },
    "Senegal": {
        "captain": "Kalidou Koulibaly",
        "coach": "Pape Thiaw",
        "confederation": "CAF",
        "nickname": "Lions of Teranga",
        "best_finish": "Quarter-finals — 2002",
        "last_wc": "Round of 16 — 2022",
    },
    "Norway": {
        "captain": "Martin Ødegaard",
        "coach": "Ståle Solbakken",
        "confederation": "UEFA",
        "nickname": "Drillos",
        "best_finish": "Round of 16 — 1998",
        "last_wc": "Did not qualify",
    },
    "Iraq": {
        "captain": "Aymen Hussein",
        "coach": "Graham Arnold",
        "confederation": "AFC",
        "nickname": "Lions of Mesopotamia",
        "best_finish": "Group stage — 1986",
        "last_wc": "Did not qualify",
    },

    # ── Group J ────────────────────────────────────────────────
    "Argentina": {
        "captain": "Lionel Messi",
        "coach": "Lionel Scaloni",
        "confederation": "CONMEBOL",
        "nickname": "La Albiceleste",
        "best_finish": "Winners (3x) — 1978, 1986, 2022",
        "last_wc": "Winners — 2022",
    },
    "Austria": {
        "captain": "Marcel Sabitzer",
        "coach": "Ralf Rangnick",
        "confederation": "UEFA",
        "nickname": "Das Team",
        "best_finish": "Third place — 1954",
        "last_wc": "Did not qualify",
    },
    "Algeria": {
        "captain": "Riyad Mahrez",
        "coach": "Vladimir Petković",
        "confederation": "CAF",
        "nickname": "Les Fennecs",
        "best_finish": "Round of 16 — 2014",
        "last_wc": "Did not qualify",
    },
    "Jordan": {
        "captain": "Yazan Al-Arab",
        "coach": "Jamal Sellami",
        "confederation": "AFC",
        "nickname": "Al-Nashama",
        "best_finish": "Debutant — first WC in 2026",
        "last_wc": "Did not qualify",
    },

    # ── Group K ────────────────────────────────────────────────
    "Portugal": {
        "captain": "Cristiano Ronaldo",
        "coach": "Roberto Martínez",
        "confederation": "UEFA",
        "nickname": "A Seleção das Quinas",
        "best_finish": "Third place — 1966",
        "last_wc": "Quarter-finals — 2022",
    },
    "Colombia": {
        "captain": "James Rodríguez",
        "coach": "Néstor Lorenzo",
        "confederation": "CONMEBOL",
        "nickname": "Los Cafeteros",
        "best_finish": "Quarter-finals — 2014",
        "last_wc": "Did not qualify",
    },
    "Uzbekistan": {
        "captain": "Eldor Shomurodov",
        "coach": "Timur Kapadze",
        "confederation": "AFC",
        "nickname": "The White Wolves",
        "best_finish": "Debutant — first WC in 2026",
        "last_wc": "Did not qualify",
    },
    "DR Congo": {
        "captain": "Chancel Mbemba",
        "coach": "Sébastien Desabre",
        "confederation": "CAF",
        "nickname": "Les Léopards",
        "best_finish": "Group stage — 1974 (as Zaire)",
        "last_wc": "Did not qualify",
    },

    # ── Group L ────────────────────────────────────────────────
    "England": {
        "captain": "Harry Kane",
        "coach": "Thomas Tuchel",
        "confederation": "UEFA",
        "nickname": "Three Lions",
        "best_finish": "Winners — 1966",
        "last_wc": "Quarter-finals — 2022",
    },
    "Croatia": {
        "captain": "Luka Modrić",
        "coach": "Zlatko Dalić",
        "confederation": "UEFA",
        "nickname": "Vatreni",
        "best_finish": "Runners-up — 2018",
        "last_wc": "Third place — 2022",
    },
    "Ghana": {
        "captain": "André Ayew",
        "coach": "Otto Addo",
        "confederation": "CAF",
        "nickname": "Black Stars",
        "best_finish": "Quarter-finals — 2010",
        "last_wc": "Group stage — 2022",
    },
    "Panama": {
        "captain": "Aníbal Godoy",
        "coach": "Thomas Christiansen",
        "confederation": "CONCACAF",
        "nickname": "La Marea Roja",
        "best_finish": "Group stage — 2018",
        "last_wc": "Did not qualify",
    },
}
