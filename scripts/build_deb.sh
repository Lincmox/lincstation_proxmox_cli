#!/bin/bash
# Script pour recompiler et réinstaller le paquet Debian lincmox
set -e

# Chemin racine du projet (depuis scripts/)
PROJECT_ROOT=$(dirname "$0")/..

# Aller dans le dossier racine
cd ../

# Récupérer la version depuis le package Python
FULL_VERSION=$(python3 -c "import sys; sys.path.insert(0,'src'); from lincmox_cli import __version__; print(__version__)")
MAIN_VERSION="${FULL_VERSION%%-*}"

echo "Version complète : $FULL_VERSION"
echo "Version principale : $MAIN_VERSION"

cd ../

# Nettoyer les anciens builds
rm -rf build *.deb *.changes *.dsc *.tar.* .pybuild
rm -rf lincmox-cli.egg-info
find lincstation_proxmox_cli/src/ -name "__pycache__" -type d -exec rm -rf {} +

# Créer l'archive .orig.tar.gz propre
# Debian attend le .orig.tar.gz dans le dossier racine du projet
# Ici, l'archive existe déjà mais on la recrée pour être sûr qu'elle est propre

rm -f lincmox-cli_${MAIN_VERSION}.orig.tar.gz

# Créer le tarball à partir du dossier source "propre"
tar czf lincmox-cli_${MAIN_VERSION}.orig.tar.gz \
    --exclude='lincstation_proxmox_cli/debian' \
    --exclude='lincstation_proxmox_cli/*.pyc' \
    --exclude='lincstation_proxmox_cli/__pycache__' \
    --exclude='lincstation_proxmox_cli/.gitignore' \
    lincstation_proxmox_cli

# Aller dans le dossier source pour le build Debian
cd ./lincstation_proxmox_cli/src

# Build du paquet Debian
debuild --check-dirname-level=0 -us -uc

cd ../../

# Réinstaller le paquet
sudo dpkg -i lincmox-cli_${FULL_VERSION}_amd64.deb

cp lincmox-cli_${FULL_VERSION}_*.deb ./lincstation_proxmox_repo/packages/

echo "Paquet Debian reconstruit et réinstallé !"
