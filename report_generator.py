from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(filename, content):
    pdf = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    for line in content.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    pdf.build(story)