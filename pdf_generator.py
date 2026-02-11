from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(curriculum, filename="curriculum.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    for week in curriculum:
        c.drawString(40, y, week["title"])
        y -= 20

        for topic in week["topics"]:
            c.drawString(60, y, f"- {topic}")
            y -= 15

        c.drawString(60, y, f"Outcome: {week['outcome']}")
        y -= 30

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
