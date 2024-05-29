from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
import os
import re

def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')
def create_receipt(file_name, receipt_data):
    # Set up the PDF
    pdf = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Register DejaVu Sans font
    font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    pdf.setFont("DejaVuSans", 24)

    # Define title and position
    pdf.drawString(1 * inch, height - 1 * inch, "Payment Receipt")

    # Draw a horizontal line
    pdf.line(1 * inch, height - 1.2 * inch, width - 1 * inch, height - 1.2 * inch)

    # Set up details section
    pdf.setFont("DejaVuSans", 12)
    pdf.drawString(1 * inch, height - 1.5 * inch, f"Receipt Number: {receipt_data['receipt_number']}")
    pdf.drawString(1 * inch, height - 1.7 * inch, f"Date: {receipt_data['date']}")
    pdf.drawString(1 * inch, height - 1.9 * inch, f"Customer Name: {receipt_data['customer_name']}")

    # Set up items section
    y = height - 2.2 * inch
    pdf.drawString(1 * inch, y, "Items:")
    y -= 0.2 * inch
    pdf.line(1 * inch, y, width - 1 * inch, y)
    y -= 0.2 * inch

    for item in receipt_data['items']:
        pdf.drawString(1 * inch, y, f"{item['name']} (Qty: {item['quantity']} @ ₹{item['unit_price']:.2f} each)")
        pdf.drawRightString(width - 1 * inch, y, f"₹{item['total_price']:.2f}")
        y -= 0.2 * inch

    # Draw a horizontal line
    y -= 0.1 * inch
    pdf.line(1 * inch, y, width - 1 * inch, y)
    y -= 0.2 * inch

    # Set up total section
    pdf.drawString(1 * inch, y, "Total Amount:")
    pdf.drawRightString(width - 1 * inch, y, f"₹{receipt_data['total_amount']:.2f}")

    # Save the PDF
    pdf.save()

# Example data for the receipt
receipt_data = {
    "receipt_number": "123456",
    "date": "2024-05-25",
    "customer_name": "John Doe",
    "items": [
        {"name": "Item A", "quantity": 2, "unit_price": 500.00, "total_price": 1000.00},
        {"name": "Item B", "quantity": 1, "unit_price": 1500.00, "total_price": 1500.00},
        {"name": "Item C", "quantity": 3, "unit_price": 750.00, "total_price": 2250.00}
    ],
    "total_amount": 4750.00
}

# Create the receipt
# Sanitize the customer name to use in the file name
sanitized_customer_name = sanitize_filename(receipt_data['customer_name'])

# Create the receipt file name
file_name = f"receipt_{sanitized_customer_name}.pdf"

create_receipt(file_name, receipt_data)
