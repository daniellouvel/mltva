"""
Génère des factures de test au format PDF pour tester le scan OCR.
Lancer : venv\Scripts\python.exe generer_factures_test.py
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT

OUTPUT_DIR = "data/factures_test"
os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()
BLEU = colors.HexColor("#2C5F8A")
GRIS = colors.HexColor("#7F8C8D")
NOIR = colors.HexColor("#1A1A1A")

def style_titre():
    return ParagraphStyle("titre", fontSize=20, textColor=BLEU, fontName="Helvetica-Bold", spaceAfter=4)

def style_sous_titre():
    return ParagraphStyle("sous_titre", fontSize=10, textColor=GRIS, fontName="Helvetica")

def style_normal():
    return ParagraphStyle("normal", fontSize=9, textColor=NOIR, fontName="Helvetica", leading=14)

def style_bold():
    return ParagraphStyle("bold", fontSize=9, textColor=NOIR, fontName="Helvetica-Bold", leading=14)

def style_droite():
    return ParagraphStyle("droite", fontSize=9, textColor=NOIR, fontName="Helvetica", alignment=TA_RIGHT)


def generer_facture(filename, fournisseur, adresse_four, siret_four,
                    client, adresse_client,
                    numero_facture, date_facture,
                    lignes, tva_rate, mode_paiement="Virement"):
    """
    lignes : liste de (description, quantite, prix_unitaire_ht)
    """
    path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # ── En-tête fournisseur ──
    story.append(Paragraph(fournisseur, style_titre()))
    story.append(Paragraph(adresse_four, style_sous_titre()))
    story.append(Paragraph(f"SIRET : {siret_four}", style_sous_titre()))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=BLEU))
    story.append(Spacer(1, 0.4*cm))

    # ── Bloc facture + client ──
    tbl_header = Table([
        [
            Paragraph(f"<b>FACTURE N° {numero_facture}</b>", style_bold()),
            Paragraph(f"<b>Client :</b><br/>{client}<br/>{adresse_client}", style_normal()),
        ]
    ], colWidths=[9*cm, 8*cm])
    tbl_header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN",  (1, 0), (1, 0),  "RIGHT"),
    ]))
    story.append(tbl_header)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(f"Date : {date_facture}", style_normal()))
    story.append(Paragraph(f"Mode de règlement : {mode_paiement}", style_normal()))
    story.append(Spacer(1, 0.6*cm))

    # ── Tableau des lignes ──
    data = [["Description", "Qté", "Prix unitaire HT", "Total HT"]]
    total_ht = 0.0
    for desc, qte, pu_ht in lignes:
        total_ligne = qte * pu_ht
        total_ht += total_ligne
        data.append([desc, str(qte), f"{pu_ht:,.2f} €", f"{total_ligne:,.2f} €"])

    tva_amount = round(total_ht * tva_rate / 100, 2)
    total_ttc  = round(total_ht + tva_amount, 2)

    tbl_lignes = Table(data, colWidths=[9*cm, 2*cm, 4*cm, 3*cm])
    tbl_lignes.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  BLEU),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ALIGN",        (1, 0), (-1, -1), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EBF5FB")]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
    ]))
    story.append(tbl_lignes)
    story.append(Spacer(1, 0.4*cm))

    # ── Totaux ──
    data_totaux = [
        ["", "Total HT :",      f"{total_ht:,.2f} €"],
        ["", f"TVA {tva_rate}% :", f"{tva_amount:,.2f} €"],
        ["", "Total TTC :",     f"{total_ttc:,.2f} €"],
    ]
    tbl_totaux = Table(data_totaux, colWidths=[9*cm, 4*cm, 4*cm])
    tbl_totaux.setStyle(TableStyle([
        ("ALIGN",       (1, 0), (-1, -1), "RIGHT"),
        ("FONTNAME",    (1, 2), (-1, 2),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 2), (-1, 2),  colors.HexColor("#D6EAF8")),
        ("LINEABOVE",   (1, 2), (-1, 2),  1, BLEU),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    story.append(tbl_totaux)
    story.append(Spacer(1, 1*cm))

    # ── Pied de page ──
    story.append(HRFlowable(width="100%", thickness=1, color=GRIS))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        f"Merci de régler par {mode_paiement} sous 30 jours.",
        ParagraphStyle("pied", fontSize=8, textColor=GRIS, fontName="Helvetica-Oblique")
    ))

    doc.build(story)
    print(f"  OK {path}  (TTC={total_ttc:.2f} EUR, TVA {tva_rate}%={tva_amount:.2f} EUR)")
    return path


print("Génération des factures de test...\n")

generer_facture(
    filename="facture_electricite_20pct.pdf",
    fournisseur="EDF ENTREPRISES",
    adresse_four="22-30 avenue de Wagram, 75008 Paris",
    siret_four="552 081 317 00218",
    client="Daniel Louvel", adresse_client="12 rue de la Paix, 75001 Paris",
    numero_facture="EDF-2026-04521",
    date_facture="15/04/2026",
    lignes=[("Consommation électrique avril 2026", 1, 320.00)],
    tva_rate=20,
    mode_paiement="Prélèvement automatique",
)

generer_facture(
    filename="facture_restauration_10pct.pdf",
    fournisseur="LE BISTROT DU COIN",
    adresse_four="5 place de la République, 75011 Paris",
    siret_four="823 456 789 00012",
    client="MLTVA SARL", adresse_client="12 rue de la Paix, 75001 Paris",
    numero_facture="BC-2026-0089",
    date_facture="03/05/2026",
    lignes=[
        ("Repas d'affaires - 2 couverts", 2, 45.00),
        ("Boissons", 2, 12.50),
    ],
    tva_rate=10,
    mode_paiement="Chèque",
)

generer_facture(
    filename="facture_fournitures_20pct.pdf",
    fournisseur="BUREAU VALLÉE",
    adresse_four="45 avenue des Ternes, 75017 Paris",
    siret_four="412 987 654 00031",
    client="Daniel Louvel", adresse_client="12 rue de la Paix, 75001 Paris",
    numero_facture="BV-20260042",
    date_facture="28/04/2026",
    lignes=[
        ("Ramettes de papier A4 (carton de 5)", 3, 28.90),
        ("Cartouches imprimante HP 302XL", 2, 34.50),
        ("Stylos BIC (lot de 12)", 4, 5.80),
    ],
    tva_rate=20,
    mode_paiement="Carte bancaire",
)

generer_facture(
    filename="facture_loyer_exempt_tva.pdf",
    fournisseur="SCI IMMOBILIER PARIS",
    adresse_four="8 boulevard Haussmann, 75009 Paris",
    siret_four="789 123 456 00015",
    client="Daniel Louvel", adresse_client="12 rue de la Paix, 75001 Paris",
    numero_facture="SCI-2026-05",
    date_facture="01/05/2026",
    lignes=[("Loyer bureaux - Mai 2026", 1, 1200.00)],
    tva_rate=0,
    mode_paiement="Virement",
)

generer_facture(
    filename="facture_traiteur_55pct.pdf",
    fournisseur="MAISON DUPONT TRAITEUR",
    adresse_four="17 rue du Commerce, 75015 Paris",
    siret_four="654 321 987 00044",
    client="MLTVA SARL", adresse_client="12 rue de la Paix, 75001 Paris",
    numero_facture="MDT-0156",
    date_facture="22/04/2026",
    lignes=[
        ("Buffet déjeuner - 10 personnes", 1, 380.00),
        ("Location matériel (nappes, couverts)", 1, 45.00),
    ],
    tva_rate=5.5,
    mode_paiement="Virement",
)

print(f"\n5 factures generees dans : {OUTPUT_DIR}/")
print("Tu peux maintenant les tester avec le bouton 'Scanner facture' dans l'appli.")
