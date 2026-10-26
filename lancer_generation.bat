@echo off
chcp 65001 > nul
title Générateur de Codes-Barres FEMAX
echo ========================================================
echo  Lancement de la génération des codes-barres...
echo ========================================================
python generate_barcodes.py
echo.
echo ========================================================
echo  Opération terminée avec succès !
echo  Consultez le dossier "output" pour voir les fichiers.
echo ========================================================
pause
