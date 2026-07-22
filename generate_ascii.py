#!/usr/bin/env python3
"""
Gera um retrato em ASCII a partir de uma foto, pronto pra colar no README.

Uso:
    pip install pillow
    python generate_ascii.py avatar.jpg            # 80 colunas, tema escuro (GitHub)
    python generate_ascii.py avatar.jpg 100        # 100 colunas
    python generate_ascii.py avatar.jpg 80 --light # inverte pro tema claro

Dica: use uma foto com bom contraste e o rosto bem iluminado (nada de contraluz).
Recorte quadrado/vertical funciona melhor. O resultado sai em ascii.txt.
"""
import sys
from PIL import Image, ImageOps

# do mais "vazio" (fundo) ao mais "cheio" (claro). Em tema escuro do GitHub,
# caractere denso = área clara da foto.
RAMP = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def to_ascii(path, cols=80, light=False):
    img = Image.open(path).convert("L")
    img = ImageOps.autocontrast(img)          # melhora o contraste automaticamente
    w, h = img.size
    rows = max(1, int(cols * (h / w) * 0.5))   # caractere ~2x mais alto que largo
    img = img.resize((cols, rows))
    px = list(img.getdata())
    ramp = RAMP[::-1] if light else RAMP
    n = len(ramp)
    lines = []
    for r in range(rows):
        row = "".join(ramp[min(n - 1, px[r * cols + c] * n // 256)] for c in range(cols))
        lines.append(row.rstrip())
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    cols = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 80
    light = "--light" in sys.argv
    art = to_ascii(path, cols, light)
    with open("ascii.txt", "w", encoding="utf-8") as f:
        f.write(art)
    print(art)
    print("\n--> salvo em ascii.txt", file=sys.stderr)
