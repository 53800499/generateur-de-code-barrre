# 🎫 Générateur de Codes-Barres FEMAX

Script Python automatisé pour la création en masse de codes-barres haute définition (**Code 128**) avec étiquettes personnalisées.

---

## 📋 Catégories et Séries Générées

| Catégorie | Plage de Numérotation | Format du Numéro | Nombre de Codes | Dossier de Destination |
| :--- | :---: | :---: | :---: | :--- |
| **Gala solidaire** | 1 à 200 | `N 001` à `N 200` | 200 | `output/01_Gala_solidaire/` |
| **ticket espoir** | 1 à 100 | `N 001` à `N 100` | 100 | `output/02_Ticket_espoir/` |
| **ticket marraine** | 1 à 50 | `N 01` à `N 50` | 50 | `output/03_Ticket_marraine/` |
| **ticket coeur d'or** | 1 à 50 | `N 01` à `N 50` | 50 | `output/04_Ticket_coeur_dor/` |
| **ticket table partenaire**| 1 à 10 | `N 01` à `N 10` | 10 | `output/05_Ticket_table_partenaire/` |
| **TOUS LES CODES** | — | — | **410** | `output/tous_les_codes_barre/` |

---

## 🎯 Spécifications Respectées

1. **Nom de chaque image** : Exactement l'élément encodé dans le code-barre (ex: `Gala solidaire N 001.png`, `ticket coeur d'or N 01.png`).
2. **Affichage sur l'image** :
   - Titre de la catégorie en grand (`GALA SOLIDAIRE`, `TICKET COEUR D'OR`, etc.).
   - Numéro clairement visible au-dessus du code-barre (`N 001`, `N 01`, etc.).
   - Barres du code-barre nettes et scannables au format standard **Code 128**.
   - Texte encodé également visible en légende sous les barres.
3. **Organisation** : Fichiers organisés par dossiers thématiques **et** également regroupés dans un dossier global `output/tous_les_codes_barre/`.
4. **Galerie Web / Impression** : Un fichier `output/galerie_apercu.html` interactif permet de visualiser, filtrer et imprimer tous les codes directement depuis le navigateur.

---

## 🚀 Utilisation

### 1. Installation des dépendances (si nécessaire)
```bash
pip install -r requirements.txt
```

### 2. Exécution du script
- **Via le terminal** :
  ```bash
  python generate_barcodes.py
  ```
- **Ou sous Windows** : Double-cliquez directement sur `lancer_generation.bat`.

---

## 📂 Structure du Répertoire

```text
code_barre/
├── generate_barcodes.py        # Script principal de génération
├── lancer_generation.bat       # Lanceur en un clic pour Windows
├── requirements.txt            # Dépendances requises (python-barcode, Pillow)
├── README.md                   # Documentation complète
└── output/
    ├── galerie_apercu.html     # Galerie web interactive & outil d'impression
    ├── tous_les_codes_barre/   # Les 410 images regroupées
    ├── 01_Gala_solidaire/      # 200 images (N 001 à N 200)
    ├── 02_Ticket_espoir/       # 100 images (N 001 à N 100)
    ├── 03_Ticket_marraine/     # 50 images (N 01 à N 50)
    ├── 04_Ticket_coeur_dor/    # 50 images (N 01 à N 50)
    └── 05_Ticket_table_partenaire/ # 10 images (N 01 à N 10)
```
