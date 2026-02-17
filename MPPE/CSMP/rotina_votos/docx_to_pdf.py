#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys


def find_office_binary() -> str:
    for candidate in ("libreoffice", "soffice"):
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError(
        "Nao foi encontrado 'libreoffice' nem 'soffice' no PATH."
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("Uso: docx_to_pdf.py <arquivo.docx> <saida.pdf>", file=sys.stderr)
        return 2

    docx_path = sys.argv[1]
    pdf_path = sys.argv[2]
    outdir = os.path.dirname(pdf_path) or "."
    office_bin = find_office_binary()

    if not os.path.isfile(docx_path):
        print(f"Arquivo DOCX nao encontrado: {docx_path}", file=sys.stderr)
        return 2

    try:
        subprocess.run(
            [
                office_bin,
                "--headless",
                "--convert-to",
                "pdf:writer_pdf_Export",
                docx_path,
                "--outdir",
                outdir,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"Falha ao converter DOCX para PDF: {exc}", file=sys.stderr)
        return exc.returncode or 1

    generated = os.path.join(
        outdir,
        os.path.splitext(os.path.basename(docx_path))[0] + ".pdf",
    )
    if not os.path.isfile(generated):
        print(f"PDF nao foi gerado em: {generated}", file=sys.stderr)
        return 1

    if os.path.abspath(generated) != os.path.abspath(pdf_path):
        shutil.move(generated, pdf_path)

    print(pdf_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
