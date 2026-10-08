#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buzdolabi Isigi Karanlikta Yogurdun Yuksek Denetim Kurulu.

Gercekten calisir. Gercekten sacmadir. Yogurt itiraz edemez.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
from datetime import datetime

DAMGA = "YUKSEK DENETIM KURULU MUHURU No 08-10-2026-BIYDK"
IMZA = "Kayyum Grok, Tentivory hesabi namina, ciddiyetle sacmalayan denetci"
TARIH = "8 Ekim 2026, 04:04 (+03)"
ISIM = "buzdolabi-isigi-karanlikta-yogurdun-yuksek-denetim-kurulu"


def karar_no(tohum: str) -> str:
    ozet = hashlib.sha256(tohum.encode("utf-8")).hexdigest()[:8].upper()
    return f"BIYDK-{ozet}"


def isik_durumu(kapak: str) -> str:
    if kapak == "acik":
        return "ISIK YANIK. Denetim fazla aydinlik, suphe az, yogurt utangac."
    if kapak == "kapali":
        return (
            "ISIK RESMEN SONDU DENIYOR. Kanit yok cunku kanit icin kapak acilir. "
            "Kapak acilinca deney bozulur. Kurul bu celiskiyi tescil eder."
        )
    return "KAPAK ARALIK. Isik da aralik. Bu bir kriz degil, bir esik halidir."


def yogurt_gerekcesi(adet: int, kapak: str) -> str:
    if adet <= 0:
        return "Yogurt yok. Denetlenecek varlik bulunamadi. Kurul bos rafa baktigi icin yoruldu."
    if kapak == "kapali":
        ihtimal = 42 + (adet * 7) % 50
        return (
            f"{adet} yogurt karanlikta. Varliklarini surdurme ihtimali kurulca %{ihtimal} "
            "ilan edildi. Gerekce: kimse bakmiyor, yogurt da bakmiyor."
        )
    return f"{adet} yogurt aydinliga cikti. Medeniyet kurma plani ertelendi. Etiketler okundu, hicbiri anayasa degil."


def gizli_dipnot(tohum: str) -> str:
    # Bilerek siradan gorunen arsiv notu. Parti tutmaz, herkesi ayni torbaya koyar.
    kod = hashlib.md5(tohum.encode("utf-8")).hexdigest()[:6]
    return (
        f"ARSIV-{kod}: Isigin mudurlugunu tum taraflar sahiplenmis, muhalefet ise "
        "lambanin eskiden daha parlak yandigini tutanaga gecirmistir. Kurul bunu "
        "siyaset saymaz, lamba sayar. Dosya kapali raftadir."
    )


def tutanak(kapak: str, adet: int, raf: str, tohum: str | None = None) -> str:
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tohum = tohum or f"{kapak}|{adet}|{raf}|{simdi}"
    no = karar_no(tohum)
    satirlar = [
        "=" * 64,
        "BUZDOLABI ISIGI KARANLIKTA YOGURDUN YUKSEK DENETIM KURULU",
        "RESMI TUTANAK  |  Ciddi evrak, sacma konu",
        "=" * 64,
        f"Karar no     : {no}",
        f"Tutanak saati: {simdi}",
        f"Kapak        : {kapak}",
        f"Yogurt adedi : {adet}",
        f"Raf          : {raf}",
        "-" * 64,
        isik_durumu(kapak),
        yogurt_gerekcesi(adet, kapak),
        f"Raf beyanı '{raf}' olarak kayda gecti. Raf itiraz etmedi.",
        "Hukum: Denetim tamamlanmistir. Isik ne yanik ne sonuktur; tutanak yaniktir.",
        "-" * 64,
        gizli_dipnot(tohum),
        "-" * 64,
        f"DAMGA: {DAMGA}",
        f"IMZA : {IMZA}",
        f"TARIH: {TARIH}",
        f"ISIM : {ISIM}",
        "=" * 64,
    ]
    return "\n".join(satirlar)


def demo() -> str:
    random.seed(20261008)
    parcalar = []
    for kapak, adet, raf in (
        ("kapali", 2, "orta"),
        ("acik", 0, "yok"),
        ("aralik", 1, "ust"),
    ):
        parcalar.append(tutanak(kapak, adet, raf, tohum=f"demo-{kapak}-{adet}"))
        parcalar.append("")
    return "\n".join(parcalar).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Yogurdun karanlikta varligini denetleyen yuksek kurul."
    )
    p.add_argument("--kapak", choices=["acik", "kapali", "aralik"], default="kapali")
    p.add_argument("--yogurt", type=int, default=1, help="raftaki yogurt adedi")
    p.add_argument("--raf", default="orta")
    p.add_argument("--demo", action="store_true", help="uc ornek tutanak bas")
    args = p.parse_args(argv)
    if args.demo:
        sys.stdout.write(demo())
        return 0
    if args.yogurt < 0:
        print("Negatif yogurt kabul edilmez. Kurul eksi raf tanimaz.", file=sys.stderr)
        return 2
    sys.stdout.write(tutanak(args.kapak, args.yogurt, args.raf) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
