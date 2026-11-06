from django.core.exceptions import ValidationError
import os

EXTENSOES_PERMITIDAS_MOD = [
    ".jar", ".zip", ".rar", ".7z", ".litemod"
]

EXTENSOES_PERMITIDAS_IMAGEM = [
    ".jpg", ".jpeg", ".png", ".webp"
]

TAMANHO_MAXIMO_MOD_MB    = 200
TAMANHO_MAXIMO_IMAGEM_MB = 5


def validar_extensao_mod(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in EXTENSOES_PERMITIDAS_MOD:
        raise ValidationError(
            f"Extensão '{ext}' não permitida. "
            f"Use: {', '.join(EXTENSOES_PERMITIDAS_MOD)}"
        )


def validar_tamanho_mod(value):
    limite = TAMANHO_MAXIMO_MOD_MB * 1024 * 1024
    if value.size > limite:
        raise ValidationError(
            f"Arquivo muito grande. Tamanho máximo: {TAMANHO_MAXIMO_MOD_MB}MB."
        )


def validar_extensao_imagem(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in EXTENSOES_PERMITIDAS_IMAGEM:
        raise ValidationError(
            f"Extensão '{ext}' não permitida. "
            f"Use: {', '.join(EXTENSOES_PERMITIDAS_IMAGEM)}"
        )


def validar_tamanho_imagem(value):
    limite = TAMANHO_MAXIMO_IMAGEM_MB * 1024 * 1024
    if value.size > limite:
        raise ValidationError(
            f"Imagem muito grande. Tamanho máximo: {TAMANHO_MAXIMO_IMAGEM_MB}MB."
        )