import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self._pageNumber = 0

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        self._pageNumber += 1

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        # Forcer l'ouverture à la première page avec une action plus spécifique
        self._doc.Catalog.OpenAction = f'<< /S /XYZ /Left 0 /Top 1000 /Zoom 1.0 /Page 1 >>'

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.drawRightString(7.5*inch, 0.5*inch, f"Page {self._pageNumber} sur {page_count}")

class PDFGenerator:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.mois_noms = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
            5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
            9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }

    def format_date(self, date_str):
        """Convertit une date au format YYYY-MM-DD en DD/MM/YYYY."""
        try:
            # Séparer les composants de la date
            year, month, day = date_str.split('-')
            # Retourner la date au format DD/MM/YYYY
            return f"{day}/{month}/{year}"
        except:
            return date_str  # Retourner la date originale si le format est incorrect

    def safe_float(self, value):
        """Convertit une valeur en float de manière sécurisée."""
        if value is None or value == '':
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def generate_ddf(self, mois, annee, output_path):
        """Génère un PDF pour les dépenses et recettes."""
        try:
            # Obtenir le chemin absolu du dossier du script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"Dossier du script : {script_dir}")
            
            # Créer le dossier data s'il n'existe pas
            data_dir = os.path.join(script_dir, "data")
            print(f"Dossier data : {data_dir}")
            
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print(f"Dossier 'data' créé à : {data_dir}")

            # Nom du fichier PDF
            nom_mois = self.mois_noms.get(mois, str(mois))
            pdf_filename = f"donnees_fiscales_{nom_mois}_{annee}.pdf"
            pdf_path = output_path  # Utiliser le chemin passé en argument
            print(f"Chemin complet du fichier PDF : {pdf_path}")

            # Créer le document PDF avec le canvas personnalisé
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30,
                pageCompression=1
            )

            # Récupérer les dépenses
            query_depenses = """
            SELECT date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire
            FROM depenses
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            ORDER BY date
            """
            depenses = self.db_manager.fetch_all(query_depenses, (f"{mois:02d}", annee))

            # Récupérer les recettes
            query_recettes = """
            SELECT date, client, montant, tva, montant_tva, commentaire
            FROM recettes
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            ORDER BY date
            """
            recettes = self.db_manager.fetch_all(query_recettes, (f"{mois:02d}", annee))

            # Calculer les totaux
            total_depenses_ttc = sum(self.safe_float(d['ttc']) for d in depenses)
            total_depenses_tva = sum(self.safe_float(d['montant_tva']) for d in depenses)
            total_recettes = sum(self.safe_float(r['montant']) for r in recettes)
            total_recettes_tva = sum(self.safe_float(r['montant_tva']) for r in recettes)

            styles = getSampleStyleSheet()
            elements = []

            # Style personnalisé pour le titre principal
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                spaceAfter=30,
                textColor=colors.HexColor('#1a237e'),  # Bleu foncé
                alignment=1,  # Centré
                fontName='Helvetica-Bold',
                leading=24
            )

            # Style personnalisé pour les sous-titres
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceBefore=20,
                spaceAfter=10,
                textColor=colors.HexColor('#283593'),  # Bleu plus clair
                alignment=0,  # Aligné à gauche
                fontName='Helvetica-Bold',
                leading=20
            )

            # En-tête avec logo et titre
            logo_path = os.path.join(data_dir, "logo.jpg")
            if os.path.exists(logo_path):
                # Créer un tableau pour l'en-tête
                header_data = [
                    [Image(logo_path, width=1.5*inch, height=1.5*inch), 
                     Paragraph(f"Document de Données Fiscales<br/>Période : {nom_mois} {annee}", title_style)]
                ]
                header_table = Table(header_data, colWidths=[2*inch, 4*inch])
                header_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
                ]))
                elements.append(header_table)
            else:
                # Si pas de logo, afficher juste le titre
                elements.append(Paragraph(f"Document de Données Fiscales<br/>Période : {nom_mois} {annee}", title_style))
            
            elements.append(Spacer(1, 20))

            # Tableau des dépenses
            depenses_data = [['Date', 'Fournisseur', 'TTC', 'Taux TVA', 'TVA']]
            for depense in depenses:
                depenses_data.append([
                    self.format_date(depense['date']),
                    depense['fournisseur'],
                    f"{self.safe_float(depense['ttc']):.2f} €",
                    f"{depense['tva_id']}%",
                    f"{self.safe_float(depense['montant_tva']):.2f} €"
                ])
            depenses_data.append(['', '', f"{total_depenses_ttc:.2f} €", '', f"{total_depenses_tva:.2f} €"])

            depenses_table = Table(depenses_data, colWidths=[1.2*inch, 2.5*inch, 1.2*inch, 1*inch, 1.2*inch])
            depenses_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),  # Bleu foncé pour l'en-tête
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8eaf6')),  # Bleu très clair pour le total
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (2, 0), (4, -1), 'RIGHT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(Paragraph("DÉPENSES", subtitle_style))
            elements.append(depenses_table)
            elements.append(PageBreak())

            # Tableau des recettes
            recettes_data = [['Date', 'Client', 'Montant', 'Taux TVA', 'TVA']]
            for recette in recettes:
                recettes_data.append([
                    self.format_date(recette['date']),
                    recette['client'],
                    f"{self.safe_float(recette['montant']):.2f} €",
                    f"{recette['tva']}%",
                    f"{self.safe_float(recette['montant_tva']):.2f} €"
                ])
            recettes_data.append(['', '', f"{total_recettes:.2f} €", '', f"{total_recettes_tva:.2f} €"])

            recettes_table = Table(recettes_data, colWidths=[1.2*inch, 2.5*inch, 1.2*inch, 1*inch, 1.2*inch])
            recettes_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),  # Bleu foncé pour l'en-tête
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8eaf6')),  # Bleu très clair pour le total
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (2, 0), (4, -1), 'RIGHT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(Paragraph("RECETTES", subtitle_style))
            elements.append(recettes_table)
            elements.append(PageBreak())

            # Tableau du bilan
            bilan_data = [
                ['Total Dépenses TTC', f"{total_depenses_ttc:.2f} €"],
                ['Total Dépenses TVA', f"{total_depenses_tva:.2f} €"],
                ['Total Recettes', f"{total_recettes:.2f} €"],
                ['Total Recettes TVA', f"{total_recettes_tva:.2f} €"],
                ['Solde', f"{(total_recettes - total_depenses_ttc):.2f} €"],
                ['TVA à payer', f"{(total_recettes_tva - total_depenses_tva):.2f} €"]
            ]

            bilan_table = Table(bilan_data, colWidths=[3*inch, 1.5*inch])
            bilan_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),  # Bleu foncé pour l'en-tête
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ]))
            elements.append(Paragraph("BILAN", subtitle_style))
            elements.append(bilan_table)

            # Créer le document avec le canvas personnalisé
            print("Début de la génération du PDF...")
            try:
                doc.build(elements, canvasmaker=NumberedCanvas)
                print("Génération du PDF terminée")
                
                # Vérifier que le fichier a bien été créé
                if os.path.exists(pdf_path):
                    print(f"Le fichier PDF a été créé avec succès à : {pdf_path}")
                    return pdf_path
                else:
                    print(f"Le fichier n'existe pas à l'emplacement attendu : {pdf_path}")
                    raise Exception("Le fichier PDF n'a pas été créé correctement")
            except Exception as build_error:
                print(f"Erreur lors de la création du PDF : {str(build_error)}")
                raise build_error
                
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {str(e)}")
            raise Exception(f"Erreur lors de la génération du PDF : {str(e)}")

    def generate_pdf(self, data, output_file):
        """Génère un PDF simple avec les données fournies."""
        try:
            # Créer le document PDF
            doc = SimpleDocTemplate(
                output_file,
                pagesize=A4,
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )

            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                spaceAfter=30,
                textColor=colors.HexColor('#1a237e'),
                alignment=1,
                fontName='Helvetica-Bold',
                leading=24
            )

            # Éléments du document
            elements = []

            # Titre
            title = Paragraph("Dépenses à Régler", title_style)
            elements.append(title)
            elements.append(Spacer(1, 20))

            # Tableau
            table = Table(data, colWidths=[50, 100, 185, 80])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))

            elements.append(table)

            # Construire le PDF
            doc.build(elements)
            return True

        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {str(e)}")
            return False 