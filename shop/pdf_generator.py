from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
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
