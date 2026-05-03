import os
import re
import fitz  # PyMuPDF
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


def _extract_text_direct(pdf_path):
    """Extraction directe du texte depuis un PDF numérique (sans OCR)."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def _extract_text_ocr(file_path):
    """Extraction par OCR Tesseract — fallback pour PDFs scannés ou images."""
    import pytesseract
    from PIL import Image

    tess = _find_tesseract()
    if tess is None:
        raise FileNotFoundError(
            "Tesseract non trouvé.\n\n"
            "Télécharger et installer :\n"
            "https://github.com/UB-Mannheim/tesseract/wiki\n"
            "(cocher 'French' pendant l'installation)"
        )
    pytesseract.pytesseract.tesseract_cmd = tess

    try:
        langs_disponibles = pytesseract.get_languages()
        lang = "fra" if "fra" in langs_disponibles else "eng"
    except Exception:
        lang = "eng"

    ext = os.path.splitext(file_path)[1].lower()
    tmp_img = None

    if ext == ".pdf":
        doc = fitz.open(file_path)
        page = doc[0]
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat)
        tmp_img = file_path + "_ocr_tmp.png"
        pix.save(tmp_img)
        doc.close()
        text = pytesseract.image_to_string(Image.open(tmp_img), lang=lang)
    else:
        text = pytesseract.image_to_string(Image.open(file_path), lang=lang)

    if tmp_img and os.path.exists(tmp_img):
        os.remove(tmp_img)

    return text


def _extract_text(file_path):
    """
    Stratégie : extraction directe en premier (PDFs numériques, fiable et rapide),
    OCR en fallback si le texte extrait est trop court (PDF scanné ou image).
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        direct = _extract_text_direct(file_path)
        if len(direct) > 50:
            return direct
    return _extract_text_ocr(file_path)


def _clean_montant(val: str) -> str:
    """
    Nettoie un montant extrait et le convertit en float string.
    Gère les formats français : '1 234,56', '1.234,56', '1234.56', '1234,56'.
    """
    val = val.strip().replace("\xa0", " ").replace(" ", "")
    if "," in val and "." in val:
        # Format européen : 1.234,56 — le point est séparateur de milliers
        val = val.replace(".", "").replace(",", ".")
    elif "," in val:
        # Format français standard : 1234,56
        val = val.replace(",", ".")
    # val est maintenant au format 1234.56
    try:
        return str(round(float(val), 2))
    except ValueError:
        return ""


def _parse_date(text):
    patterns = [
        r"\b(\d{2})[/\-\.](\d{2})[/\-\.](\d{4})\b",
        r"\b(\d{2})[/\-\.](\d{2})[/\-\.](\d{2})\b",
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


# Motif d'un montant monétaire : gère les séparateurs de milliers (espace, point)
# et la virgule/point comme séparateur décimal
_MONTANT_RE = r"([\d][\d\s .]*[\d][,\.][\d]{2}|[\d]{1,6}[,\.][\d]{2})"


def _parse_montant_ttc(text):
    patterns = [
        rf"[Tt][Oo][Tt][Aa][Ll]\s+[Tt][Tt][Cc]\s*:?\s*{_MONTANT_RE}",
        rf"[Mm]ontant\s+[Tt][Tt][Cc]\s*:?\s*{_MONTANT_RE}",
        rf"[Tt][Tt][Cc]\s*:?\s*{_MONTANT_RE}",
        rf"[Nn]et\s+[àa]\s+payer\s*:?\s*{_MONTANT_RE}",
        rf"[Tt]otal\s+[àa]\s+payer\s*:?\s*{_MONTANT_RE}",
        rf"[Tt]otal\s*:?\s*{_MONTANT_RE}",
        rf"{_MONTANT_RE}\s*€?\s*[Tt][Tt][Cc]",
        rf"{_MONTANT_RE}\s*€?\s*[Nn]et\s+[àa]\s+payer",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            result = _clean_montant(m.group(1))
            if result:
                return result
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
            return TVA_RATES.get(rate, TVA_RATES.get(rate.split(".")[0], "20.00%"))
    return ""


def _parse_montant_tva(text):
    patterns = [
        rf"[Mm]ontant\s+TVA\s*:?\s*{_MONTANT_RE}",
        rf"TVA\s*:?\s*{_MONTANT_RE}\s*€",
        rf"{_MONTANT_RE}\s*€?\s*TVA",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            result = _clean_montant(m.group(1))
            if result:
                return result
    return ""


def _parse_fournisseur(text):
    lignes = [l.strip() for l in text.splitlines() if l.strip()]
    mots_cles = {"facture", "invoice", "avoir", "devis", "bon", "date", "n°", "numero",
                 "total", "ttc", "tva", "siret", "siren", "iban", "bic"}
    for ligne in lignes[:6]:
        if len(ligne) > 2 and not any(k in ligne.lower() for k in mots_cles):
            return ligne[:50]
    return ""


def scan_facture(file_path):
    """
    Analyse une facture (PDF ou image) et retourne un dict avec les champs trouvés.
    Priorité : extraction texte direct (PDF numérique) → OCR Tesseract (PDF scanné/image).
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
