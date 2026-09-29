#!/usr/bin/env bash
# macOS / Linux kurulumu: Python ortamı, model (4,7 GB) ve varsayılan referans ses.
# Tekrar çalıştırmak güvenlidir; var olan adımları atlar.
set -euo pipefail
cd "$(dirname "$0")"

MODEL_REPO="openbmb/VoxCPM2"
MODEL_REVIZYON="32279effe8c19989596f05d353d1447f51d9e915"  # test edilen sürüm (2026-09-29)
MODEL_DIZINI="models/VoxCPM2"

# Uzak (SSH) oturumlarda Homebrew PATH'te olmayabilir
for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  [ -x "$b" ] && eval "$("$b" shellenv)" && break
done

echo "==> 1/4 uv"
if ! command -v uv >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    brew install uv
  else
    echo "uv bulunamadı. Resmi kurulum betiği çalıştırılıyor (https://docs.astral.sh/uv/)."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
  fi
fi

echo "==> 2/4 Python ortamı (.venv, Python 3.12)"
[ -d .venv ] || uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt

echo "==> 3/4 Model: $MODEL_REPO @ ${MODEL_REVIZYON:0:7}"
.venv/bin/python - <<EOF
from huggingface_hub import snapshot_download
snapshot_download(repo_id="$MODEL_REPO", revision="$MODEL_REVIZYON", local_dir="$MODEL_DIZINI")
EOF

echo "==> 4/4 Varsayılan referans ses (Edge-TTS tr-TR-EmelNeural)"
if [ ! -f reference_female.wav ]; then
  .venv/bin/python -m edge_tts --voice tr-TR-EmelNeural \
    --text "Merhaba, ben Emel. Bu ses klonlama için kısa bir referans örneğidir." \
    --write-media .referans.mp3
  .venv/bin/python -c "
import librosa, soundfile as sf
y, sr = librosa.load('.referans.mp3', sr=None, mono=True)
sf.write('reference_female.wav', y, sr)
"
  rm -f .referans.mp3
fi

echo "==> Doğrulama"
.venv/bin/python -c "
import torch
cihaz = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
print('torch', torch.__version__, '| cihaz:', cihaz)
"
.venv/bin/python duygulu_tts.py ornekler/ornek_duygulu.txt --kuru >/dev/null
echo
echo "Kurulum tamam. Deneme:"
echo "  .venv/bin/python duygulu_tts.py ornekler/tam_ornek.txt -o tam_ornek.wav"
