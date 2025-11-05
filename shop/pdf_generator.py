from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.contrib.staticfiles import finders
from shop.views import *


def generate_receipt_pdf_donation(donation):
    """
    Generates a PDF receipt for the given donation.
    Returns a BytesIO object containing the PDF.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 18)
    p.drawString(1 * inch, height - 1 * inch, "Payment Receipt")

    # Basic info
    p.setFont("Helvetica", 12)
    p.drawString(1 * inch, height - 1.5 * inch, f"Donation ID: {donation.id}")
    p.drawString(1 * inch, height - 1.8 * inch, f"Donor: {donation.full_name}")
    p.drawString(1 * inch, height - 2.1 * inch, f"Date: {donation.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(1 * inch, height - 2.4 * inch, f"Donation Type: {donation.donation_type}")

    # Total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(1 * inch, height - 3 * inch, f"Total: €{donation.donation_amount}")

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(1 * inch, 0.7 * inch, "Thank you for your donation!")
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


def generate_donation_receipt_pdf(donation):
    """
    Generates a professional PDF receipt for a donation.
    Returns a BytesIO buffer containing the PDF.
    """

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # === HEADER ===
    logo_path = finders.find("images/default_logo.jpg")  # adjust if your logo is in another folder
    if logo_path:
        try:
            p.drawImage(logo_path, 0.9 * inch, height - 1.4 * inch, width=1.2 * inch, preserveAspectRatio=True, mask=None)
        except Exception:
            pass  # Avoid breaking if logo not found

    # === HEADER ===
    p.setFillColorRGB(0.2, 0.4, 0.6)
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width / 2, height - 1 * inch, "ΑΠΟΔΕΙΞΗ ΔΩΡΕΑΣ/DONATION RECEIPT")
    p.setFillColor(colors.black)

    # === DONATION DETAILS BOX ===
    box_top = height - 1.5 * inch
    p.setStrokeColorRGB(0.8, 0.8, 0.8)
    p.setLineWidth(1)
    p.roundRect(0.8 * inch, box_top - 1.8 * inch, width - 1.6 * inch, 1.4 * inch, 10, stroke=1, fill=0)

    p.setFont("Helvetica", 12)
    p.drawString(1 * inch, box_top - 0.5 * inch, f"Αρ. Δωρεάς/Donation Number: {donation.id}")
    p.drawString(1 * inch, box_top - 0.9 * inch, f"Ονοματεπώνυμο/Full Name: {donation.full_name}")
    p.drawString(1 * inch, box_top - 1.3 * inch, f"Email: {donation.email}")

    p.drawRightString(width - 1 * inch, box_top - 0.5 * inch, f"Ημερομηνία/Date: {donation.created_at.strftime('%d/%m/%Y')}")
    p.drawRightString(width - 1 * inch, box_top - 0.9 * inch, f"Τύπος Δωρεάς/Donation Type: {donation.donation_type}")

    # === AMOUNT ===
    p.setFont("Helvetica-Bold", 18)
    p.setFillColorRGB(0.15, 0.4, 0.2)
    p.drawRightString(width - 1 * inch, box_top - 2.3 * inch, f"Ποσό/Amount: €{donation.donation_amount:.2f}")
    p.setFillColor(colors.black)

    # === THANK YOU SECTION ===
    p.setFont("Helvetica-Bold", 16)
    p.setFillColorRGB(0.2, 0.4, 0.6)
    p.drawCentredString(width / 2, height - 4.2 * inch, "Σας ευχαριστούμε για τη στήριξή σας!/Thank you for your support!")
    p.setFillColor(colors.black)

    # === FOOTER ===
    p.setStrokeColorRGB(0.8, 0.8, 0.8)
    p.line(1 * inch, 1.1 * inch, width - 1 * inch, 1.1 * inch)

    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width / 2, 0.9 * inch, "Σύνδεσμος Γονέων και Φίλων Παιδιών με Καρδιοπάθειες")
    p.drawCentredString(width / 2, 0.7 * inch, "Οδός Γράμμου 11, Διαμέρισμα 5, Στρόβολος, Λευκωσία, Κύπρος")
    p.drawCentredString(width / 2, 0.5 * inch, "Τηλ: 22315196 | Email: info@pediheart.org.cy | www.pediheart.org.cy")

    # Finalize
    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer