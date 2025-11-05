from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime


def generate_donation_receipt_pdf(donation):
    """
    Generates a professional PDF receipt for a donation.
    Returns a BytesIO buffer containing the PDF.
    """

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # === HEADER ===
    p.setFillColorRGB(0.2, 0.4, 0.6)
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width / 2, height - 1 * inch, "DOANTION RECEIPT")
    p.setFillColor(colors.black)

    # === DONATION DETAILS BOX ===
    box_top = height - 1.5 * inch
    p.setStrokeColorRGB(0.8, 0.8, 0.8)
    p.setLineWidth(1)
    p.roundRect(0.8 * inch, box_top - 1.8 * inch, width - 1.6 * inch, 1.4 * inch, 10, stroke=1, fill=0)

    p.setFont("Helvetica", 12)
    p.drawString(1 * inch, box_top - 0.7 * inch, f"Donation Number: {donation.id}")
    p.drawString(1 * inch, box_top - 1.1 * inch, f"Full Name: {donation.full_name}")

    p.drawRightString(width - 1 * inch, box_top - 0.7 * inch, f"Date: {donation.created_at.strftime('%d/%m/%Y')}")
    p.drawRightString(width - 1 * inch, box_top - 1.1 * inch, f"Donation Type: {donation.donation_type}")

    # === AMOUNT ===
    p.setFont("Helvetica-Bold", 18)
    p.setFillColorRGB(0.15, 0.4, 0.2)
    p.drawRightString(width - 1 * inch, box_top - 2.4 * inch, f"Amount: €{donation.donation_amount:.2f}")
    p.setFillColor(colors.black)

    # === THANK YOU SECTION ===
    p.setFont("Helvetica-Bold", 16)
    p.setFillColorRGB(0.2, 0.4, 0.6)
    p.drawCentredString(width / 2, height - 4.4 * inch, "Thank you for your support!")
    p.setFillColor(colors.black)

    # === FOOTER ===
    p.setStrokeColorRGB(0.8, 0.8, 0.8)
    p.line(1 * inch, 1.1 * inch, width - 1 * inch, 1.1 * inch)

    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width / 2, 0.9 * inch, "Association of Parents and Friends of Heart Diseased Children")
    p.drawCentredString(width / 2, 0.7 * inch, "11 Grammou street, Apt 5, Strovolos, Nicosia, Cyprus")
    p.drawCentredString(width / 2, 0.5 * inch, "Tel: 22315196 | Email: info@pediheart.org.cy | www.pediheart.org.cy")

    # Finalize
    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer