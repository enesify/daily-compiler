#!/usr/bin/env python3
"""Editör bulgu dosyasını denetler ve bildirim için tek satırlık özet üretir.

Kullanım: python3 tools/bulgular.py /tmp/dc/bulgular.json

Dosya biçimi (kurallar/EDITOR.md, 6. bölüm):
{"dogrulanan": 14, "bulgular": [{"onem": "KRİTİK|ÖNEMLİ|KÜÇÜK", "konum": "...", "sorun": "...",
  "kanit": "...", "oneri": "...", "karar": "düzeltildi | reddedildi: gerekçe | küçük, bırakıldı"}]}
"""
import json
import sys

ONEM = ("KRİTİK", "ÖNEMLİ", "KÜÇÜK")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    bs = d.get("bulgular") or []
    sorun = []
    say = {o: 0 for o in ONEM}
    duz = red = bos = 0
    gerek = []
    for i, b in enumerate(bs):
        o = str(b.get("onem", "")).upper().replace("KRITIK", "KRİTİK").replace("ONEMLI", "ÖNEMLİ").replace("KUCUK", "KÜÇÜK")
        if o not in say:
            sorun.append(f"bulgular[{i}]: önem {b.get('onem')!r} tanınmadı")
            continue
        say[o] += 1
        k = str(b.get("karar") or "").strip()
        if not k:
            bos += 1
            if o != "KÜÇÜK":
                sorun.append(f"bulgular[{i}] ({o}, {b.get('konum')}): karar yazılmamış")
        elif k.startswith("düzelt"):
            duz += 1
        elif k.startswith("reddedildi"):
            red += 1
            gerek.append(k.split(":", 1)[1].strip() if ":" in k else "gerekçe yok")
    n = d.get("dogrulanan")
    satir = (f"Editör: {n if n is not None else '?'} haber doğrulandı · {say['KRİTİK']} kritik, {say['ÖNEMLİ']} önemli, "
             f"{say['KÜÇÜK']} küçük bulgu · {duz} düzeltildi, {red} reddedildi")
    if gerek:
        satir += " (" + "; ".join(g[:80] for g in gerek) + ")"
    print(satir)
    for s in sorun:
        print("UYARI: " + s, file=sys.stderr)
    sys.exit(1 if sorun else 0)


if __name__ == "__main__":
    main()
