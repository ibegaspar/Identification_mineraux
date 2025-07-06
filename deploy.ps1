# Script de déploiement automatisé - Team RobotMali
# Usage: .\deploy.ps1 [railway|render|heroku|local]

param(
    [string]$Target = "local"
)

# Configuration
$ErrorActionPreference = "Stop"

Write-Host "🚀 Déploiement de l'API Prédiction Minéraux" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Fonction pour afficher les messages
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Vérification des prérequis
function Test-Prerequisites {
    Write-Status "Vérification des prérequis..."
    
    # Vérifier Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Success "Python trouvé: $pythonVersion"
    }
    catch {
        Write-Error "Python n'est pas installé ou n'est pas dans le PATH"
        exit 1
    }
    
    # Vérifier pip
    try {
        $pipVersion = pip --version 2>&1
        Write-Success "pip trouvé: $pipVersion"
    }
    catch {
        Write-Error "pip n'est pas installé"
        exit 1
    }
    
    # Vérifier git
    try {
        $gitVersion = git --version 2>&1
        Write-Success "git trouvé: $gitVersion"
    }
    catch {
        Write-Error "git n'est pas installé"
        exit 1
    }
    
    # Vérifier les fichiers requis
    $requiredFiles = @("api.py", "requirements_api.txt", "model_final_durete_densiter.h5", "scaler.pkl", "label_encoder.pkl")
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-Error "Fichier manquant: $file"
            exit 1
        }
    }
    
    Write-Success "Tous les prérequis sont satisfaits"
}

# Test local
function Test-Local {
    Write-Status "Test local de l'API..."
    
    # Installer les dépendances
    Write-Status "Installation des dépendances..."
    pip install -r requirements_api.txt
    
    # Tester l'API
    Write-Status "Démarrage de l'API en mode test..."
    python test_api.py
    
    Write-Success "Test local terminé"
}

# Déploiement Railway
function Deploy-Railway {
    Write-Status "Déploiement sur Railway..."
    
    # Vérifier Railway CLI
    try {
        $railwayVersion = railway --version 2>&1
        Write-Success "Railway CLI trouvé: $railwayVersion"
    }
    catch {
        Write-Warning "Railway CLI non installé. Installation..."
        npm install -g @railway/cli
    }
    
    # Login Railway
    Write-Status "Connexion à Railway..."
    railway login
    
    # Déployer
    Write-Status "Déploiement en cours..."
    railway up
    
    Write-Success "Déploiement Railway terminé"
}

# Déploiement Render
function Deploy-Render {
    Write-Status "Déploiement sur Render..."
    
    Write-Warning "Déploiement Render nécessite une configuration manuelle:"
    Write-Host "1. Allez sur https://render.com" -ForegroundColor White
    Write-Host "2. Créez un nouveau Web Service" -ForegroundColor White
    Write-Host "3. Connectez votre repository GitHub" -ForegroundColor White
    Write-Host "4. Configurez:" -ForegroundColor White
    Write-Host "   - Build Command: pip install -r requirements_api.txt" -ForegroundColor White
    Write-Host "   - Start Command: uvicorn api:app --host 0.0.0.0 --port `$PORT" -ForegroundColor White
    
    Write-Success "Instructions Render affichées"
}

# Déploiement Heroku
function Deploy-Heroku {
    Write-Status "Déploiement sur Heroku..."
    
    # Vérifier Heroku CLI
    try {
        $herokuVersion = heroku --version 2>&1
        Write-Success "Heroku CLI trouvé: $herokuVersion"
    }
    catch {
        Write-Error "Heroku CLI n'est pas installé"
        Write-Warning "Installez-le depuis: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    }
    
    # Login Heroku
    Write-Status "Connexion à Heroku..."
    heroku login
    
    # Créer l'app si elle n'existe pas
    try {
        heroku apps:info 2>&1 | Out-Null
    }
    catch {
        Write-Status "Création de l'application Heroku..."
        heroku create mineral-prediction-api
    }
    
    # Déployer
    Write-Status "Déploiement en cours..."
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku main
    
    Write-Success "Déploiement Heroku terminé"
}

# Configuration de l'application mobile
function Setup-Mobile {
    Write-Status "Configuration de l'application mobile..."
    
    if (-not (Test-Path "mobile_app")) {
        Write-Error "Dossier mobile_app non trouvé"
        return
    }
    
    # Demander l'URL de l'API
    $API_URL = Read-Host "Entrez l'URL de votre API déployée"
    
    if ([string]::IsNullOrEmpty($API_URL)) {
        Write-Warning "URL non fournie, configuration mobile ignorée"
        return
    }
    
    # Mettre à jour l'URL dans App.js
    $appJsPath = "mobile_app\App.js"
    $content = Get-Content $appJsPath -Raw
    $content = $content -replace "const API_BASE_URL = 'https://votre-api-deployee.com'", "const API_BASE_URL = '$API_URL'"
    Set-Content $appJsPath $content
    
    Write-Success "Configuration mobile mise à jour avec l'URL: $API_URL"
    
    # Instructions pour l'application mobile
    Write-Status "Instructions pour l'application mobile:"
    Write-Host "1. cd mobile_app" -ForegroundColor White
    Write-Host "2. npm install" -ForegroundColor White
    Write-Host "3. npm run android (ou npm run ios)" -ForegroundColor White
}

# Menu principal
switch ($Target.ToLower()) {
    "local" {
        Test-Prerequisites
        Test-Local
    }
    "railway" {
        Test-Prerequisites
        Deploy-Railway
        Setup-Mobile
    }
    "render" {
        Test-Prerequisites
        Deploy-Render
        Setup-Mobile
    }
    "heroku" {
        Test-Prerequisites
        Deploy-Heroku
        Setup-Mobile
    }
    "all" {
        Test-Prerequisites
        Test-Local
        Deploy-Railway
        Setup-Mobile
    }
    default {
        Write-Host "Usage: .\deploy.ps1 [local|railway|render|heroku|all]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Options:" -ForegroundColor White
        Write-Host "  local   - Test local uniquement" -ForegroundColor White
        Write-Host "  railway - Déploiement sur Railway" -ForegroundColor White
        Write-Host "  render  - Instructions pour Render" -ForegroundColor White
        Write-Host "  heroku  - Déploiement sur Heroku" -ForegroundColor White
        Write-Host "  all     - Test local + déploiement Railway + config mobile" -ForegroundColor White
        exit 1
    }
} 