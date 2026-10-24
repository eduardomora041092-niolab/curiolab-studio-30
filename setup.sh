#!/usr/bin/env bash
# Preparación de una sesión nueva. Solo instala lo autorizado (ver DEPENDENCIAS.md).
set -euo pipefail
cd "$(dirname "$0")"
pip install --break-system-packages -q --require-hashes --no-deps --only-binary=:all: -r requirements.txt
mkdir -p models
BASE="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
while read -r sum f; do
  [ -s "models/$f" ] || curl -sSL -o "models/$f" "$BASE/$f"
  echo "$sum  models/$f" | sha256sum -c --quiet || { echo "CHECKSUM FAIL $f"; exit 5; }
done <<'SUMS'
7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5 kokoro-v1.0.onnx
bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d voices-v1.0.bin
SUMS
which ffmpeg >/dev/null && python3 -c "import kokoro_onnx, PIL, numpy, soundfile; print('setup ok')"
