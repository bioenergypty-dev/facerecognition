# Script de Deploy Automatizado para Render
# Verifica dependencias y hace push a GitHub

param(
    [string]$CommitMessage = "Fix: Actualizar dependencias para Python 3.11"
)

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  DEPLOY AUTOMATIZADO A RENDER" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# 1. Validar Python
Write-Host "`n[1/5] Verificando Python 3.11..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Versión instalada: $pythonVersion" -ForegroundColor Green

# 2. Validar requirements.txt
Write-Host "`n[2/5] Validando requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Get-Content requirements.txt | ForEach-Object { Write-Host "  ✓ $_" -ForegroundColor Green }
} else {
    Write-Host "❌ requirements.txt no encontrado" -ForegroundColor Red
    exit 1
}

# 3. Validar runtime.txt
Write-Host "`n[3/5] Verificando runtime.txt..." -ForegroundColor Yellow
$runtime = Get-Content runtime.txt
Write-Host "Runtime: $runtime" -ForegroundColor Green
if ($runtime -notmatch "3\.11") {
    Write-Host "⚠️  Se recomienda Python 3.11+ para compatibilidad" -ForegroundColor Yellow
}

# 4. Git commit y push
Write-Host "`n[4/5] Preparando push a GitHub..." -ForegroundColor Yellow
git add requirements.txt runtime.txt
git commit -m "$CommitMessage"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Cambios commiteados" -ForegroundColor Green
} else {
    Write-Host "⚠️  Sin cambios nuevos para commitear" -ForegroundColor Yellow
}

Write-Host "`n[5/5] Push a GitHub (main)..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Push completado exitosamente" -ForegroundColor Green
    Write-Host "`n✅ Deploy iniciado en Render" -ForegroundColor Green
    Write-Host "Monitorea el deploy en: https://dashboard.render.com" -ForegroundColor Cyan
} else {
    Write-Host "❌ Error en push" -ForegroundColor Red
    exit 1
}

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  ESTADO: COMPLETADO" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
