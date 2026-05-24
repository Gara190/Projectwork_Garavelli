#!/bin/bash
# Interrompe l'esecuzione in caso di errore
set -e

echo "[1/3] Creazione dell'ambiente virtuale Python..."
python3 -m venv venv

echo "[2/3] Attivazione ambiente e installazione dipendenze..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Controlla l'esistenza della cartella assets, se non esiste la crea
mkdir -p assets

echo "[3/3] Avvio dell'applicazione OpenCV..."
python3 main.py
