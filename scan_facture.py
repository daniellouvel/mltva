import os
import re
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
from datetime import datetime

TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\Daniel\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
]

TVA_RATES = {"20": "20.00%", "10": "10.00%", "5.5": "5.50%", "5,5": "5.50%", "8.5": "8.50%", "0": "0.00%"}


def _find_tesseract():
    for path in TESSERACT_PATHS:
        if os.path.isfile(path):
            return path
    return None


def _pdf_to_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    mat = fitz.Matrix(2.0, 2.0)  # zoom x2 pour meilleure qualité OCR
    pix = page.get_pixmap(matrix=mat)
    img_path = pdf_path + "_ocr_tmp.png"
    pix.save(img_path)
    doc.close()
    return img_path


def _extract_text(file_path):
    tess = _find_tesseract()
    if tess is None:
        raise FileNotFoundError(
            "Tesseract non trouvé.\n\n"
            "Télécharger et installer :\n"
            "https://github.com/UB-Mannheim/tesseract/wiki\n"
            "(cocher 'French' pendant l'installation)"
        )
    pytesseract.pytesseract.tesseract_cmd = tess

    # Détecter les langues disponibles, préférer fra sinon eng
    try:
        langs_disponibles = pytesseract.get_languages()
        lang = "fra" if "fra" in langs_disponibles else "eng"
    except Exception:
        lang = "eng"

    ext = os.path.splitext(file_path)[1].lower()
    tmp_img = None

    if ext == ".pdf":
        tmp_img = _pdf_to_image(file_path)
        text = pytesseract.image_to_string(Image.open(tmp_img), lang=lang)
    else:
        text = pytesseract.image_to_string(Image.open(file_path), lang=lang)

    if tmp_img and os.path.exists(tmp_img):
        os.remove(tmp_img)

    return text


def _parse_date(text):
    patterns = [
        r"\b(\d{2})[/\-\.](\d{2})[/\-\.](\d{4})\b",  # DD/MM/YYYY
        r"\b(\d{2})[/\-\.](\d{2})[/\-\.](\d{2})\b",   # DD/MM/YY
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            j, mo, a = m.group(1), m.group(2), m.group(3)
            if len(a) == 2:
                a = "20" + a
            try:
                datetime.strptime(f"{j}/{mo}/{a}", "%d/%m/%Y")
                return f"{j}/{mo}/{a}"
            except ValueError:
                continue
    return ""


def _parse_montant_ttc(text):
    # Cherche TTC suivi ou précédé d'un montant
    patterns = [
        r"[Tt][Tt][Cc]\s*[:\s]*(\d+[\s,\.]\d{2})",
        r"(\d+[\s,\.]\d{2})\s*[€]\s*[Tt][Tt][Cc]",
        r"[Tt]otal\s+[Tt][Tt][Cc]\s*[:\s]*(\d+[\s,\.]\d{2})",
        r"[Mm]ontant\s+[Tt][Tt][Cc]\s*[:\s]*(\d+[\s,\.]\d{2})",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            val = m.group(1).replace(" ", "").replace(",", ".")
            try:
                return str(float(val))
            except ValueError:
                continue
    return ""


def _parse_tva_rate(text):
    patterns = [
        r"TVA\s*[àa]?\s*(\d+[,\.]\d+)\s*%",
        r"Taux\s+TVA\s*[:\s]*(\d+[,\.]\d+)\s*%",
        r"(\d+[,\.]\d+)\s*%\s*TVA",
        r"TVA\s+(\d+)\s*%",
        r"(\d+)\s*%\s*TVA",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            rate = m.group(1).replace(",", ".")
            return TVA_RATES.get(rate, TVA_RATES.get(rate.split(".")[0], "20%"))
    return ""


def _parse_montant_tva(text):
    patterns = [
        r"[Mm]ontant\s+TVA\s*[:\s]*(\d+[\s,\.]\d{2})",
        r"TVA\s*[:\s]*(\d+[\s,\.]\d{2})\s*[€]",
        r"(\d+[\s,\.]\d{2})\s*[€]\s*TVA",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(1).replace(" ", "").replace(",", ".")
            try:
                return str(float(val))
            except ValueError:
                continue
    return ""


def _parse_fournisseur(text):
    # Tente d'extraire le nom en haut du document (3 premières lignes non vides)
    lignes = [l.strip() for l in text.splitlines() if l.strip()]
    mots_cles = {"facture", "invoice", "avoir", "devis", "bon", "date", "n°", "numero", "total", "ttc", "tva"}
    for ligne in lignes[:6]:
        if len(ligne) > 2 and not any(k in ligne.lower() for k in mots_cles):
            return ligne[:50]
    return ""


def scan_facture(file_path):
    """
    Analyse une facture (PDF ou image) et retourne un dict avec les champs trouvés.
    Retourne un dict vide si l'analyse échoue.
    """
    text = _extract_text(file_path)

    return {
        "date":        _parse_date(text),
        "fournisseur": _parse_fournisseur(text),
        "montant":     _parse_montant_ttc(text),
        "tva_rate":    _parse_tva_rate(text),
        "montant_tva": _parse_montant_tva(text),
        "texte_brut":  text,
    }
