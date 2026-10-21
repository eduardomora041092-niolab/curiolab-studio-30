#!/usr/bin/env bash
# One-time setup for a fresh cloud session (all sources are free; network: PyPI + GitHub only).
set -euo pipefail
cd "$(dirname "$0")"
pip install --break-system-packages -q kokoro-onnx soundfile pillow numpy
mkdir -p models
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "models/$f" ] || curl -sSL -o "models/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done
which ffmpeg >/dev/null && python3 -c "import kokoro_onnx, PIL, numpy; print('setup ok')"
