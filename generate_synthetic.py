import os, random
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

fake = Faker()

def make_receipt_pdf(path, fraud=False):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, fake.company())

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Address: {fake.address().replace(chr(10), ', ')}")
    c.drawString(50, height - 85, f"Date: {fake.date_this_year()}")

    # Line items
    y = height - 120
    total = 0.0
    for i in range(random.randint(3, 8)):
        desc = fake.word().capitalize() + " service"
        amt = round(random.uniform(10, 200), 2)
        total += amt
        c.drawString(50, y, f"{desc:30s}  ${amt:8.2f}")
        y -= 15

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 10, f"TOTAL: ${total:8.2f}")

    # Fraud “stamp”
    if fraud:
        c.setFont("Helvetica-Bold", 40)
        c.setFillColorRGB(1, 0, 0, alpha=0.5)
        c.saveState()
        c.translate(200, 300)
        c.rotate(30)
        c.drawCentredString(0, 0, "!!! FRAUD !!!")
        c.restoreState()

    c.save()

if __name__ == "__main__":
    os.makedirs("data/synth/pdfs/genuine", exist_ok=True)
    os.makedirs("data/synth/pdfs/fraud", exist_ok=True)

    N = 1000  # number per class
    for i in range(N):
        genuine_path = f"data/synth/pdfs/genuine/receipt_{i:04d}.pdf"
        fraud_path   = f"data/synth/pdfs/fraud/fake_{i:04d}.pdf"
        make_receipt_pdf(genuine_path, fraud=False)
        make_receipt_pdf(fraud_path,   fraud=True)
    print(f"Generated {N} genuine + {N} fraudulent PDFs")
