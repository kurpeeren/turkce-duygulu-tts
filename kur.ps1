# Windows kurulumu (NVIDIA GPU, CUDA 12.4): Python ortamı, model (4,7 GB) ve varsayılan referans ses.
# Gereken: Python 3.12 (python komutu PATH'te). Tekrar çalıştırmak güvenlidir.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$ModelRepo = "openbmb/VoxCPM2"
$ModelRevizyon = "32279effe8c19989596f05d353d1447f51d9e915"  # test edilen sürüm (2026-09-29)
$ModelDizini = "models/VoxCPM2"
$Py = ".venv\Scripts\python.exe"

Write-Host "==> 1/4 Python ortamı (.venv)"
if (-not (Test-Path $Py)) { python -m venv .venv }
& $Py -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip güncellenemedi" }

Write-Host "==> 2/4 Paketler (önce CUDA'lı torch, sonra geri kalanı)"
& $Py -m pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
if ($LASTEXITCODE -ne 0) { throw "torch kurulamadı" }
& $Py -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "paketler kurulamadı" }

Write-Host "==> 3/4 Model: $ModelRepo @ $($ModelRevizyon.Substring(0, 7))"
& $Py -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='$ModelRepo', revision='$ModelRevizyon', local_dir='$ModelDizini')"
if ($LASTEXITCODE -ne 0) { throw "model indirilemedi" }

Write-Host "==> 4/4 Varsayılan referans ses (Edge-TTS tr-TR-EmelNeural)"
if (-not (Test-Path reference_female.wav)) {
    & $Py -m edge_tts --voice tr-TR-EmelNeural --text "Merhaba, ben Emel. Bu ses klonlama için kısa bir referans örneğidir." --write-media .referans.mp3
    & $Py -c "import librosa, soundfile as sf; y, sr = librosa.load('.referans.mp3', sr=None, mono=True); sf.write('reference_female.wav', y, sr)"
    Remove-Item .referans.mp3 -ErrorAction SilentlyContinue
}

Write-Host "==> Doğrulama"
$env:PYTHONIOENCODING = "utf-8"
& $Py -c "import torch; print('torch', torch.__version__, '| cuda:', torch.cuda.is_available())"
& $Py duygulu_tts.py ornekler/ornek_duygulu.txt --kuru | Out-Null
Write-Host ""
Write-Host "Kurulum tamam. Deneme:"
Write-Host "  .venv\Scripts\python.exe duygulu_tts.py ornekler\tam_ornek.txt -o tam_ornek.wav"
