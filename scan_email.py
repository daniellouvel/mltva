import imaplib
import email
import os
import json
import tempfile
from email.header import decode_header

EMAIL_CONFIG_PATH = "data/email_config.json"


def load_email_config():
    if os.path.exists(EMAIL_CONFIG_PATH):
        with open(EMAIL_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "server": "imap.gmail.com",
        "port": 993,
        "email": "",
        "password": "",
        "dossier": "INBOX",
        "jours": 30,
    }


def save_email_config(config):
    with open(EMAIL_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def test_connection(server, port, email_addr, password):
    """Retourne (True, '') ou (False, message_erreur)."""
    try:
        conn = imaplib.IMAP4_SSL(server, int(port))
        conn.login(email_addr, password)
        conn.logout()
        return True, ""
    except imaplib.IMAP4.error as e:
        return False, f"Authentification refusée : {e}"
    except Exception as e:
        return False, str(e)


def fetch_invoice_pdfs(server, port, email_addr, password, dossier="INBOX", jours=30, temp_dir=None):
    """
    Télécharge les PDF en pièces jointes des emails reçus dans les <jours> derniers jours.
    Retourne (liste_pdf_paths, nombre_emails_analysés).
    """
    from datetime import datetime, timedelta

    if temp_dir is None:
        temp_dir = tempfile.mkdtemp(prefix="mltva_email_")

    date_depuis = (datetime.now() - timedelta(days=jours)).strftime("%d-%b-%Y")
    pdf_paths = []
    emails_count = 0

    conn = imaplib.IMAP4_SSL(server, int(port))
    try:
        conn.login(email_addr, password)
        conn.select(dossier)

        status, messages = conn.search(None, f"SINCE {date_depuis}")
        if status != "OK" or not messages[0]:
            return [], 0

        message_ids = messages[0].split()
        emails_count = len(message_ids)

        for msg_id in message_ids:
            status, msg_data = conn.fetch(msg_id, "(RFC822)")
            if status != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])

            for part in msg.walk():
                if part.get_content_type() != "application/pdf":
                    continue
                content_disp = str(part.get("Content-Disposition", ""))
                if "attachment" not in content_disp and "inline" not in content_disp:
                    continue

                raw_name = part.get_filename() or f"facture_{msg_id.decode()}.pdf"
                decoded = decode_header(raw_name)
                filename = decoded[0][0]
                if isinstance(filename, bytes):
                    filename = filename.decode(decoded[0][1] or "utf-8", errors="replace")

                safe = filename.replace("/", "_").replace("\\", "_").replace(":", "_")
                pdf_path = os.path.join(temp_dir, safe)

                base, ext = os.path.splitext(pdf_path)
                counter = 1
                while os.path.exists(pdf_path):
                    pdf_path = f"{base}_{counter}{ext}"
                    counter += 1

                with open(pdf_path, "wb") as f:
                    f.write(part.get_payload(decode=True))

                pdf_paths.append(pdf_path)
    finally:
        try:
            conn.logout()
        except Exception:
            pass

    return pdf_paths, emails_count
