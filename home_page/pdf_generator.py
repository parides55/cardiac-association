from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from shop.views import *


def generate_receipt_pdf_member(member):
    """
    Generates a PDF receipt for the given membership.
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
    p.drawString(1 * inch, height - 1.5 * inch, f"Member's ID: {member.id}")
    p.drawString(1 * inch, height - 1.8 * inch, f"Member's name: {member.full_name}")
    p.drawString(1 * inch, height - 2.1 * inch, f"Date: {member.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    # Total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(1 * inch, height - 3 * inch, f"Total: €20.00")

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(1 * inch, 0.7 * inch, "Thank you for becoming a Member!")
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
