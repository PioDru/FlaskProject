# manage_railway_volume.ps1

param (
    [Parameter(Mandatory=$true)]
    [ValidateSet('create', 'upload', 'list', 'login', 'link')]
    [string]$Action,

    [Parameter(Mandatory=$false)]
    [string]$ModelPath
)

# Sprawdź czy Node.js jest zainstalowany
function Test-NodeJS {
    try {
        $null = Get-Command node -ErrorAction Stop
        $nodeVersion = node -v
        Write-Host "Node.js $nodeVersion jest zainstalowane" -ForegroundColor Green
    }
    catch {
        Write-Host "Node.js nie jest zainstalowane. Zainstaluj Node.js ze strony: https://nodejs.org/" -ForegroundColor Red
        exit 1
    }
}

# Sprawdź czy Railway CLI jest zainstalowane
function Test-RailwayCLI {
    try {
        $null = Get-Command railway -ErrorAction Stop
        Write-Host "Railway CLI jest zainstalowane" -ForegroundColor Green
    }
    catch {
        Write-Host "Railway CLI nie jest zainstalowane. Instaluję..." -ForegroundColor Yellow
        npm install -g @railway/cli
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Błąd podczas instalacji Railway CLI" -ForegroundColor Red
            exit 1
        }
    }
}

# Sprawdź status logowania Railway
function Test-RailwayLogin {
    $output = railway whoami 2>&1
    if ($output -match "You are not logged in") {
        Write-Host "Nie jesteś zalogowany do Railway. Uruchom skrypt z parametrem -Action login" -ForegroundColor Red
        exit 1
    }
}

# Zaloguj do Railway
function Connect-Railway {
    Write-Host "Uruchamiam proces logowania do Railway..." -ForegroundColor Blue
    railway login
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Zalogowano pomyślnie do Railway" -ForegroundColor Green
    } else {
        Write-Host "Błąd podczas logowania do Railway" -ForegroundColor Red
        exit 1
    }
}

# Utwórz volume
function New-RailwayVolume {
    Write-Host "Tworzenie nowego volume..." -ForegroundColor Blue

    # Poprawna składnia dla tworzenia volume
    cmd /c "railway volume add -m /app/models 2>&1"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Volume został utworzony pomyślnie" -ForegroundColor Green

        # Wyświetl utworzone volumes
        Write-Host "`nLista dostępnych volumes:" -ForegroundColor Blue
        cmd /c "railway volume ls 2>&1"
    } else {
        Write-Host "Błąd podczas tworzenia volume" -ForegroundColor Red
        exit 1
    }
}

# Wgraj model do volume
function Upload-ModelToVolume {
    param (
        [string]$Path
    )
    if (-not (Test-Path $Path)) {
        Write-Host "Błąd: Plik modelu nie istnieje w podanej ścieżce: $Path" -ForegroundColor Red
        exit 1
    }

    # Konwertuj ścieżkę na format zgodny z Windows
    $WindowsPath = $Path -replace '/', '\'

    Write-Host "Wgrywanie modelu do volume..." -ForegroundColor Blue
    # Użyj komendy 'upload' zamiast 'push'
    cmd /c "railway volume upload `"$WindowsPath`" 2>&1"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Model został wgrany pomyślnie" -ForegroundColor Green

        # Pokaż zawartość po wgraniu
        Write-Host "`nZawartość volume po wgraniu:" -ForegroundColor Blue
        cmd /c "railway volume ls 2>&1"
    } else {
        Write-Host "Błąd podczas wgrywania modelu" -ForegroundColor Red
        exit 1
    }
}

# Połącz z projektem Railway
function Connect-RailwayProject {
    Write-Host "Uruchamiam proces łączenia z projektem Railway..." -ForegroundColor Blue
    Write-Host "Wybierz swój projekt z listy..." -ForegroundColor Yellow

    # Najpierw upewnijmy się, że użytkownik jest zalogowany
    Test-RailwayLogin

    # Połącz z projektem
    cmd /c "railway link 2>&1"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Połączono pomyślnie z projektem Railway" -ForegroundColor Green
    } else {
        Write-Host "Błąd podczas łączenia z projektem" -ForegroundColor Red
        exit 1
    }
}

# Sprawdź status linkowania projektu
function Test-RailwayLink {
    $output = railway whoami 2>&1
    if ($output -match "No linked project found") {
        Write-Host "Nie połączono z projektem Railway. Uruchom skrypt z parametrem -Action link" -ForegroundColor Red
        exit 1
    }
}



# Wyświetl zawartość volume
function Get-VolumeContent {
    Write-Host "Pobieranie listy plików z volume..." -ForegroundColor Blue
    cmd /c "railway volume ls 2>&1"
}

# Główna logika skryptu
switch ($Action) {
    'login' {
        Test-NodeJS
        Test-RailwayCLI
        Connect-Railway
    }
    'link' {
        Test-NodeJS
        Test-RailwayCLI
        Test-RailwayLogin
        Connect-RailwayProject
    }
    'create' {
        Test-NodeJS
        Test-RailwayCLI
        Test-RailwayLogin
        Test-RailwayLink
        New-RailwayVolume
    }
    'upload' {
        if (-not $ModelPath) {
            Write-Host "Błąd: Ścieżka do modelu jest wymagana dla akcji 'upload'" -ForegroundColor Red
            Write-Host "Użycie: .\manage_railway_volume.ps1 -Action upload -ModelPath C:\sciezka\do\modelu.h5" -ForegroundColor Yellow
            exit 1
        }
        Test-NodeJS
        Test-RailwayCLI
        Test-RailwayLogin
        Test-RailwayLink
        Upload-ModelToVolume -Path $ModelPath
    }
    'list' {
        Test-NodeJS
        Test-RailwayCLI
        Test-RailwayLogin
        Test-RailwayLink
        Get-VolumeContent
    }
}