from reportlab.pdfgen import canvas


def generate_invoice(
    invoice_path,
    transaction_id,
    username,
    plan_name,
    price,
    start_date,
    end_date,
):
    pdf = canvas.Canvas(invoice_path)

    pdf.setTitle("Subscription Invoice")

    pdf.drawString(50, 800, "BLOG MANAGEMENT - SUBSCRIPTION INVOICE")
    pdf.drawString(50, 760, f"Transaction ID: {transaction_id}")
    pdf.drawString(50, 730, f"Username: {username}")
    pdf.drawString(50, 700, f"Plan: {plan_name}")
    pdf.drawString(50, 670, f"Price: Rs. {price}")
    pdf.drawString(50, 640, f"Start Date: {start_date}")
    pdf.drawString(50, 610, f"End Date: {end_date}")

    pdf.save()