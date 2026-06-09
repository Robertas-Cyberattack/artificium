from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_invoice_pdf(invoice):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "ARTIFICIUM INVOICE",
            styles['Title']
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Invoice Number: {invoice.invoice_number}",
            styles['Normal']
        )
    )

    elements.append(
        Paragraph(
            f"Client: {invoice.client.username}",
            styles['Normal']
        )
    )

    elements.append(
        Paragraph(
            f"Project: {invoice.project.title}",
            styles['Normal']
        )
    )

    elements.append(
        Paragraph(
            f"Amount: £{invoice.amount}",
            styles['Normal']
        )
    )

    elements.append(
        Paragraph(
            f"Status: {invoice.status}",
            styles['Normal']
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Thank you for your business.",
            styles['Normal']
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf