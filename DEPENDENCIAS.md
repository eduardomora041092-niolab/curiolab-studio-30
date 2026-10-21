# Dependencias autorizadas — CurioLab Studio 30

**Autorización del dueño (2026-10-21, 14:30 America/New_York, literal):**
"Autorizo que las ejecuciones de CurioLab Studio 30 instalen las dependencias necesarias del proyecto y
descarguen los modelos de voz Kokoro desde sus fuentes oficiales, sin gasto adicional y únicamente para este
experimento."

Esta autorización se limita a lo que aparece en esta lista. No modifica ningún control de seguridad. Si una
instalación se deniega, la ejecución se detiene en ese paso y lo informa; no se intenta otra vía.

## Paquetes Python (origen: PyPI, https://pypi.org) — `requirements.txt`
| Paquete | Versión | Uso |
|---|---|---|
| kokoro-onnx | 0.6.1 | Síntesis de voz local (TTS) |
| espeakng-loader | 0.2.4 | Fonemas de espeak-ng (dependencia de kokoro-onnx) |
| onnxruntime | 1.29.0 | Ejecución del modelo ONNX |
| phonemizer | 3.4.0 | Conversión texto→fonemas |
| soundfile | 0.14.0 | Lectura y escritura de WAV |
| pillow | 12.3.0 | Dibujo de los fotogramas |
| numpy | 2.5.3 | Cálculo numérico y audio |
| Transitivas | flatbuffers 25.12.19, packaging 26.3, protobuf 7.36.1, joblib 1.6.0, cloudpickle 3.1.2, attrs 26.1.0, dlinfo 2.0.0, typing_extensions 4.16.0, cffi 2.1.1, pycparser 3.0 | Instaladas por pip |

## Modelos de voz (origen oficial: release `model-files-v1.0` de https://github.com/thewh1teagle/kokoro-onnx)
| Archivo | Tamaño | SHA-256 |
|---|---|---|
| kokoro-v1.0.onnx | 325 532 387 B | 7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5 |
| voices-v1.0.bin | 28 214 398 B | bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d |

`setup.sh` comprueba ambas sumas SHA-256 y se detiene si no coinciden.

## Ya presentes en la imagen (no se instalan)
Python 3.13, ffmpeg 6.1.1 (libx264, aac).
