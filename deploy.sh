#!/bin/bash

# Script de déploiement automatisé - Team RobotMali
# Usage: ./deploy.sh [railway|render|heroku|local]

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement de l'API Prédiction Minéraux"
echo "=========================================="

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
check_prerequisites() {
    print_status "Vérification des prérequis..."
    
    # Vérifier Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 n'est pas installé"
        exit 1
    fi
    
    # Vérifier pip
    if ! command -v pip &> /dev/null; then
        print_error "pip n'est pas installé"
        exit 1
    fi
    
    # Vérifier git
    if ! command -v git &> /dev/null; then
        print_error "git n'est pas installé"
        exit 1
    fi
    
    # Vérifier les fichiers requis
    required_files=("api.py" "requirements_api.txt" "model_final_durete_densiter.h5" "scaler.pkl" "label_encoder.pkl")
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "Fichier manquant: $file"
            exit 1
        fi
    done
    
    print_success "Tous les prérequis sont satisfaits"
}

# Test local
test_local() {
    print_status "Test local de l'API..."
    
    # Installer les dépendances
    print_status "Installation des dépendances..."
    pip install -r requirements_api.txt
    
    # Tester l'API
    print_status "Démarrage de l'API en mode test..."
    python test_api.py
    
    print_success "Test local terminé"
}

# Déploiement Railway
deploy_railway() {
    print_status "Déploiement sur Railway..."
    
    # Vérifier Railway CLI
    if ! command -v railway &> /dev/null; then
        print_warning "Railway CLI non installé. Installation..."
        npm install -g @railway/cli
    fi
    
    # Login Railway
    print_status "Connexion à Railway..."
    railway login
    
    # Déployer
    print_status "Déploiement en cours..."
    railway up
    
    print_success "Déploiement Railway terminé"
}

# Déploiement Render
deploy_render() {
    print_status "Déploiement sur Render..."
    
    print_warning "Déploiement Render nécessite une configuration manuelle:"
    echo "1. Allez sur https://render.com"
    echo "2. Créez un nouveau Web Service"
    echo "3. Connectez votre repository GitHub"
    echo "4. Configurez:"
    echo "   - Build Command: pip install -r requirements_api.txt"
    echo "   - Start Command: uvicorn api:app --host 0.0.0.0 --port \$PORT"
    
    print_success "Instructions Render affichées"
}

# Déploiement Heroku
deploy_heroku() {
    print_status "Déploiement sur Heroku..."
    
    # Vérifier Heroku CLI
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI n'est pas installé"
        print_warning "Installez-le depuis: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Login Heroku
    print_status "Connexion à Heroku..."
    heroku login
    
    # Créer l'app si elle n'existe pas
    if ! heroku apps:info &> /dev/null; then
        print_status "Création de l'application Heroku..."
        heroku create mineral-prediction-api
    fi
    
    # Déployer
    print_status "Déploiement en cours..."
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku main
    
    print_success "Déploiement Heroku terminé"
}

# Configuration de l'application mobile
setup_mobile() {
    print_status "Configuration de l'application mobile..."
    
    if [ ! -d "mobile_app" ]; then
        print_error "Dossier mobile_app non trouvé"
        return
    fi
    
    # Demander l'URL de l'API
    read -p "Entrez l'URL de votre API déployée: " API_URL
    
    if [ -z "$API_URL" ]; then
        print_warning "URL non fournie, configuration mobile ignorée"
        return
    fi
    
    # Mettre à jour l'URL dans App.js
    sed -i "s|const API_BASE_URL = 'https://votre-api-deployee.com'|const API_BASE_URL = '$API_URL'|g" mobile_app/App.js
    
    print_success "Configuration mobile mise à jour avec l'URL: $API_URL"
    
    # Instructions pour l'application mobile
    print_status "Instructions pour l'application mobile:"
    echo "1. cd mobile_app"
    echo "2. npm install"
    echo "3. npm run android (ou npm run ios)"
}

# Menu principal
main() {
    case "${1:-local}" in
        "local")
            check_prerequisites
            test_local
            ;;
        "railway")
            check_prerequisites
            deploy_railway
            setup_mobile
            ;;
        "render")
            check_prerequisites
            deploy_render
            setup_mobile
            ;;
        "heroku")
            check_prerequisites
            deploy_heroku
            setup_mobile
            ;;
        "all")
            check_prerequisites
            test_local
            deploy_railway
            setup_mobile
            ;;
        *)
            echo "Usage: $0 [local|railway|render|heroku|all]"
            echo ""
            echo "Options:"
            echo "  local   - Test local uniquement"
            echo "  railway - Déploiement sur Railway"
            echo "  render  - Instructions pour Render"
            echo "  heroku  - Déploiement sur Heroku"
            echo "  all     - Test local + déploiement Railway + config mobile"
            exit 1
            ;;
    esac
}

# Exécution
main "$@" 