from screens.text import TextSpec


ASCII_TITLE = r"""
 _______                  _             _   ______ _                     
|__   __|                (_)           | | |  ____| |                    
   | | ___ _ __ _ __ ___  _ _ __   __ _| | | |__  | | _____   _____ _ __ 
   | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | | |  __| | |/ _ \ \ / / _ \ '_ \
   | |  __/ |  | | | | | | | | | | (_| | | | |____| |  __/\ V /  __/ | | |
   |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_| |______|_|\___| \_/ \___|_| |_|
"""

MEDIUM_ASCII_TITLE = r"""
 _____                  _          _   ___ _                  
|_   _|__ _ _ _ __  (_)_ _  __ _| | | __| |_____ _____ _ _ 
  | |/ -_) '_| '  \ | | ' \/ _` | | | _|| / -_) V / -_) ' \
  |_|\___|_| |_|_|_|_|_|_||_\__,_|_| |___|_\___|\_/\___|_||_|
"""

SMALL_ASCII_TITLE = r"""
 _____              _       _   ___ _             
|_   _|__ _ _ _ __ (_)_ _  /_\ | __| |_____ _____
  | |/ -_) '_| '  \| | ' \/ _ \| _|| / -_) V / -_)
  |_|\___|_| |_|_|_|_|_||_/_/ \_\___|_\___|\_/\___|
"""

TINY_ASCII_TITLE = r"""
 _____ _ _ 
|_   _/ / |
  | | | | |
  |_| |_|_|
"""

TITLE = TextSpec(
    text=ASCII_TITLE,
    id="title",
    font_color="#ffbf69",
    font_size="hero",
    font_type="ascii",
    text_style="bold",
)
SUBTITLE = TextSpec(
    text=":: PATH TO GLORY ::",
    id="subtitle",
    font_color="#7dd3fc",
    font_size="large",
    font_type="terminal",
    text_style="bold",
)
TAGLINE = TextSpec(
    text="Your all-in-one terminal companion for FIFA World Cup 2026 - 🇺🇸 🇲🇽 🇨🇦",
    id="tagline",
    font_color="#cbf3f0",
    font_size="small",
    font_type="terminal",
)
MENU_TITLE = TextSpec(
    text="Menu",
    id="menu-title",
    font_color="#ffbf69",
    font_size="small",
    font_type="terminal",
    text_style="bold",
)
MENU_ITEMS = (
    TextSpec(text="Group", font_size="small", font_type="terminal", styling={"screen": "groups"}),
    TextSpec(text="Fixtures", font_size="small", font_type="terminal", styling={"screen": "fixtures"}),
    TextSpec(text="Squad List", font_size="small", font_type="terminal"),
    TextSpec(text="Live Score", font_size="small", font_type="terminal", styling={"screen": "live-scores"}),
)
