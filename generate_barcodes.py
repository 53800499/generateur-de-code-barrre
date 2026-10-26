#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Codes-Barres Professionnels
========================================
Génère les codes-barres Code 128 au format PNG pour différentes catégories d'événements :
  - Gala solidaire N 001 à N 200
  - Ticket espoir N 001 à N 100
  - Ticket marraine N 01 à N 50
  - Ticket coeur d'or N 01 à N 50
  - Ticket table partenaire N 01 à N 10

Chaque fichier PNG est nommé exactement selon l'élément encodé dans le code-barre.
L'image comporte le titre de la catégorie, le numéro bien visible (ex: N 001),
le code-barre haute définition ainsi que la légende du texte encodé.
"""

import os
import io
import time
import unicodedata
from pathlib import Path
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

# Configuration des séries
CONFIG_SERIES = [
    {
        "id": "gala_solidaire",
        "name": "Gala solidaire",
        "display_title": "GALA SOLIDAIRE",
        "folder": "01_Gala_solidaire",
        "prefix": "Gala solidaire",
        "start": 1,
        "end": 200,
        "padding": 3,       # N 001 à N 200
        "num_prefix": "N ",
    },
    {
        "id": "ticket_espoir",
        "name": "ticket espoir",
        "display_title": "TICKET ESPOIR",
        "folder": "02_Ticket_espoir",
        "prefix": "ticket espoir",
        "start": 1,
        "end": 100,
        "padding": 3,       # N 001 à N 100
        "num_prefix": "N ",
    },
    {
        "id": "ticket_marraine",
        "name": "ticket marraine",
        "display_title": "TICKET MARRAINE",
        "folder": "03_Ticket_marraine",
        "prefix": "ticket marraine",
        "start": 1,
        "end": 50,
        "padding": 2,       # N 01 à N 50
        "num_prefix": "N ",
    },
    {
        "id": "ticket_coeur_dor",
        "name": "ticket coeur d'or",
        "display_title": "TICKET COEUR D'OR",
        "folder": "04_Ticket_coeur_dor",
        "prefix": "ticket coeur d'or",
        "start": 1,
        "end": 50,
        "padding": 2,       # N 01 à N 50
        "num_prefix": "N ",
    },
    {
        "id": "ticket_table_partenaire",
        "name": "ticket table partenaire",
        "display_title": "TICKET TABLE PARTENAIRE",
        "folder": "05_Ticket_table_partenaire",
        "prefix": "ticket table partenaire",
        "start": 1,
        "end": 10,
        "padding": 2,       # N 01 à N 10
        "num_prefix": "N ",
    },
]

def sanitize_for_barcode128(text: str) -> str:
    """
    Code 128 accepte uniquement les caractères ASCII (0-127).
    Convertit les caractères spéciaux / ligatures (ex: œ -> oe) si nécessaire.
    """
    # Remplacer les ligatures courantes
    replacements = {
        'œ': 'oe', 'Œ': 'OE',
        'æ': 'ae', 'Æ': 'AE',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Décomposer et retirer les accents si présents
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

def sanitize_filename(name: str) -> str:
    """Évite les caractères interdits dans les noms de fichiers Windows."""
    invalid_chars = '<>:"/\\|?*'
    for ch in invalid_chars:
        name = name.replace(ch, '_')
    return name

def load_fonts():
    """Charge les polices TrueType système ou revient aux polices par défaut."""
    font_candidates_bold = [
        "arialbd.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "calibrib.ttf",
        "segoeuib.ttf",
    ]
    font_candidates_regular = [
        "arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "calibri.ttf",
        "segoeui.ttf",
    ]

    title_font = None
    num_font = None
    sub_font = None

    for f in font_candidates_bold:
        try:
            title_font = ImageFont.truetype(f, 32)
            num_font = ImageFont.truetype(f, 48)
            break
        except Exception:
            continue

    for f in font_candidates_regular:
        try:
            sub_font = ImageFont.truetype(f, 22)
            break
        except Exception:
            continue

    if title_font is None:
        title_font = ImageFont.load_default()
        num_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    return title_font, num_font, sub_font

def create_barcode_card(display_title: str, number_str: str, encoded_text: str, fonts) -> Image.Image:
    """
    Crée une image élégante, lisible et prête pour impression contenant :
      - Le titre de la catégorie (ex: GALA SOLIDAIRE)
      - Le numéro en gros caractères bien visibles (ex: N 001)
      - Le code-barre Code 128
      - Le texte encodé en bas de carte
    """
    title_font, num_font, sub_font = fonts
    ascii_encoded_text = sanitize_for_barcode128(encoded_text)

    # 1. Génération du code-barre via python-barcode
    code = barcode.get('code128', ascii_encoded_text, writer=ImageWriter())
    buf = io.BytesIO()
    code.write(buf, options={
        'write_text': False,
        'module_height': 16.0,
        'module_width': 0.32,
        'quiet_zone': 2.0
    })
    buf.seek(0)
    bc_img = Image.open(buf).convert('RGBA')

    # Dimensions du badge
    card_width = max(bc_img.width + 100, 840)
    card_height = bc_img.height + 230

    img = Image.new('RGB', (card_width, card_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Bordure sobre et soignée
    draw.rounded_rectangle([(12, 12), (card_width - 12, card_height - 12)], radius=16, outline=(203, 213, 225), width=2)

    # En-tête : Titre de la catégorie
    bbox_title = draw.textbbox((0, 0), display_title, font=title_font)
    w_title = bbox_title[2] - bbox_title[0]
    draw.text(((card_width - w_title) // 2, 28), display_title, fill=(30, 41, 59), font=title_font)

    # Numéro bien visible
    bbox_num = draw.textbbox((0, 0), number_str, font=num_font)
    w_num = bbox_num[2] - bbox_num[0]
    draw.text(((card_width - w_num) // 2, 74), number_str, fill=(15, 23, 42), font=num_font)

    # Positionnement du code-barre
    bc_x = (card_width - bc_img.width) // 2
    bc_y = 140
    img.paste(bc_img, (bc_x, bc_y), bc_img)

    # Texte encodé en bas (légende du code-barre)
    bbox_sub = draw.textbbox((0, 0), encoded_text, font=sub_font)
    w_sub = bbox_sub[2] - bbox_sub[0]
    draw.text(((card_width - w_sub) // 2, bc_y + bc_img.height + 12), encoded_text, fill=(100, 116, 139), font=sub_font)

    return img

def generate_all(base_output_dir: Path):
    """Génère tous les codes-barres pour toutes les séries configurées."""
    print("=" * 70)
    print(" DÉMARRAGE DE LA GÉNÉRATION DES CODES-BARRES")
    print("=" * 70)

    fonts = load_fonts()
    total_generated = 0
    start_time = time.time()

    # Dossier général regroupant TOUS les codes
    all_in_one_dir = base_output_dir / "tous_les_codes_barre"
    all_in_one_dir.mkdir(parents=True, exist_ok=True)

    summary_stats = []
    gallery_data = []

    for series in CONFIG_SERIES:
        series_name = series["name"]
        series_title = series["display_title"]
        prefix = series["prefix"]
        folder_name = series["folder"]
        start_num = series["start"]
        end_num = series["end"]
        padding = series["padding"]
        num_prefix = series["num_prefix"]

        series_dir = base_output_dir / folder_name
        series_dir.mkdir(parents=True, exist_ok=True)

        count = end_num - start_num + 1
        print(f"\n[+] Génération série : {series_title} ({count} codes de {num_prefix}{start_num:0{padding}d} à {num_prefix}{end_num:0{padding}d})")

        series_start_time = time.time()

        for n in range(start_num, end_num + 1):
            number_str = f"{num_prefix}{n:0{padding}d}"
            encoded_text = f"{prefix} {number_str}"
            file_base_name = sanitize_filename(encoded_text)
            file_name = f"{file_base_name}.png"

            # Génération de l'image
            card_img = create_barcode_card(series_title, number_str, encoded_text, fonts)

            # Sauvegarde dans le dossier de la catégorie
            cat_file_path = series_dir / file_name
            card_img.save(cat_file_path, "PNG", optimize=True)

            # Sauvegarde dans le dossier unique regroupant tout
            all_file_path = all_in_one_dir / file_name
            card_img.save(all_file_path, "PNG", optimize=True)

            total_generated += 1

            # Données pour la galerie HTML
            gallery_data.append({
                "category": series_title,
                "number": number_str,
                "text": encoded_text,
                "file_name": file_name,
                "relative_path": f"{folder_name}/{file_name}"
            })

        duration = time.time() - series_start_time
        summary_stats.append({
            "name": series_title,
            "count": count,
            "folder": str(series_dir),
            "duration": f"{duration:.2f}s"
        })
        print(f"    Terminé : {count} images générées en {duration:.2f}s")

    total_duration = time.time() - start_time

    # Génération du fichier HTML de prévisualisation
    generate_html_gallery(base_output_dir, gallery_data)

    print("\n" + "=" * 70)
    print(" RÉCAPITULATIF DE LA GÉNÉRATION")
    print("=" * 70)
    for stat in summary_stats:
        print(f" - {stat['name']:<26}: {stat['count']:>4} codes ({stat['duration']}) -> {stat['folder']}")
    print("-" * 70)
    print(f" TOTAL : {total_generated} codes-barres générés en {total_duration:.2f} secondes !")
    print(f" Dossier global : {all_in_one_dir}")
    print(f" Aperçu HTML   : {base_output_dir / 'galerie_apercu.html'}")
    print("=" * 70)

def generate_html_gallery(output_dir: Path, gallery_data: list):
    """Génère une interface web élégante pour visualiser, rechercher et imprimer les codes."""
    html_path = output_dir / "galerie_apercu.html"

    # Extraction des catégories uniques
    categories = list(dict.fromkeys(item["category"] for item in gallery_data))
    cat_buttons = "\n".join([f'<button class="filter-btn" onclick="filterCategory(\'{cat}\')">{cat}</button>' for cat in categories])

    # Génération des cartes
    cards_html = []
    for item in gallery_data:
        cards_html.append(f"""
        <div class="barcode-card" data-category="{item['category']}" data-search="{item['text'].lower()} {item['number'].lower()}">
            <div class="card-badge">{item['category']}</div>
            <div class="card-num">{item['number']}</div>
            <img src="{item['relative_path']}" alt="{item['text']}" loading="lazy">
            <div class="card-filename">{item['file_name']}</div>
        </div>
        """)

    cards_joined = "\n".join(cards_html)

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galerie des Codes-Barres Événementiels</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0b0f19;
            --surface: #131b2e;
            --surface-card: #1a243b;
            --border: #243250;
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.25);
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --accent: #f59e0b;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2.5rem 2rem;
        }}
        .header {{
            max-width: 1400px;
            margin: 0 auto 2rem auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1.5rem;
        }}
        .header h1 {{
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .header p {{
            color: var(--text-muted);
            margin-top: 0.35rem;
            font-size: 1rem;
        }}
        .stats-badge {{
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 0.6rem 1.2rem;
            border-radius: 999px;
            font-weight: 700;
            color: var(--primary);
            box-shadow: 0 4px 15px var(--primary-glow);
        }}
        .controls {{
            max-width: 1400px;
            margin: 0 auto 2rem auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        .search-bar {{
            width: 100%;
            padding: 0.9rem 1.4rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--surface);
            color: var(--text-main);
            font-size: 1.05rem;
            outline: none;
            transition: all 0.2s ease;
        }}
        .search-bar:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }}
        .filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
        }}
        .filter-btn {{
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 0.5rem 1.1rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--primary);
            color: #0b0f19;
            border-color: var(--primary);
            box-shadow: 0 4px 12px var(--primary-glow);
        }}
        .print-btn {{
            margin-left: auto;
            background: #10b981;
            color: #ffffff;
            border: none;
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            transition: background 0.2s;
        }}
        .print-btn:hover {{
            background: #059669;
        }}
        .grid {{
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.5rem;
        }}
        .barcode-card {{
            background: var(--surface-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .barcode-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            border-color: #3b82f6;
        }}
        .card-badge {{
            align-self: flex-start;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: rgba(56, 189, 248, 0.12);
            color: var(--primary);
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        }}
        .card-num {{
            font-size: 1.2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 0.75rem;
        }}
        .barcode-card img {{
            width: 100%;
            height: auto;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        .card-filename {{
            margin-top: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-muted);
            word-break: break-all;
            text-align: center;
        }}
        @media print {{
            body {{
                background: white;
                color: black;
                padding: 0;
            }}
            .header, .controls {{
                display: none;
            }}
            .grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }}
            .barcode-card {{
                border: 1px dashed #ccc;
                background: white;
                box-shadow: none;
                page-break-inside: avoid;
            }}
            .card-badge, .card-num, .card-filename {{
                color: black;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Système de Codes-Barres FEMAX</h1>
            <p>Tous les codes-barres générés au format Code 128 avec étiquettes haute précision</p>
        </div>
        <div class="stats-badge">
            Total : {len(gallery_data)} codes générés
        </div>
    </div>

    <div class="controls">
        <input type="text" id="searchInput" class="search-bar" placeholder="Rechercher par numéro (ex: 001, N 50) ou catégorie..." oninput="handleSearch()">
        <div class="filters">
            <button class="filter-btn active" onclick="filterCategory('ALL')">Tous ({len(gallery_data)})</button>
            {cat_buttons}
            <button class="print-btn" onclick="window.print()">Imprimer la sélection</button>
        </div>
    </div>

    <div class="grid" id="barcodeGrid">
        {cards_joined}
    </div>

    <script>
        let currentCategory = 'ALL';
        let searchQuery = '';

        function filterCategory(cat) {{
            currentCategory = cat;
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.innerText.startsWith(cat) || (cat === 'ALL' && btn.innerText.startsWith('Tous'))) {{
                    btn.classList.add('active');
                }}
            }});
            applyFilters();
        }}

        function handleSearch() {{
            searchQuery = document.getElementById('searchInput').value.toLowerCase().trim();
            applyFilters();
        }}

        function applyFilters() {{
            const cards = document.querySelectorAll('.barcode-card');
            let visibleCount = 0;
            cards.forEach(card => {{
                const cat = card.getAttribute('data-category');
                const search = card.getAttribute('data-search');

                const matchCat = (currentCategory === 'ALL' || cat === currentCategory);
                const matchSearch = (!searchQuery || search.includes(searchQuery));

                if (matchCat && matchSearch) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    output_directory = Path(__file__).resolve().parent / "output"
    generate_all(output_directory)
