from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate
from reportlab.lib.units import inch

# Sample data based on the image structure
data = {
    "name": "Name(22, 粗,底線)",
    "contact": "Email address(10, 細) | phone (10, 細)",
    "education": [
        ("學校名稱(10, 細)", "學位及所修科系 (10, 細)(第二條)", ["經歷或者演講(10, 細)"]),
        ("學校名稱(10, 細)", "學位及所修科系 (10, 細)(第二條)", ["經歷或者演講(10, 細)"]),
    ],
    "practical_experience": [
        ("機構名稱(10, 細)", "職位 (10, 細)(第二條)", ["經歷或者演講(10, 細)"]),
        ("機構名稱(10, 細)", "職位 (10, 細)(第二條)", ["經歷或者演講(10, 細)"]),
    ]
}

# Create PDF
pdf_path = "you_can_name_here.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Title
style = styles['Title']
story.append(Paragraph(data['name'], style))

# Spacer
story.append(Spacer(1, 0.25 * inch))

# Contact
style = styles['BodyText']
story.append(Paragraph(data['contact'], style))

# Education Header
story.append(Spacer(1, 0.25 * inch))
style = styles['Heading2']
story.append(Paragraph("EDUCATION", style))

# Education Details
style = styles['BodyText']
for school, degree, experiences in data['education']:
    story.append(Paragraph(school, style))
    story.append(Paragraph(degree, style))
    for experience in experiences:
        story.append(Paragraph(experience, style))
    story.append(Spacer(1, 0.1 * inch))

# Practical Experience Header
story.append(Spacer(1, 0.25 * inch))
style = styles['Heading2']
story.append(Paragraph("PRACTICAL EXPERIENCE", style))

# Practical Experience Details
for organization, position, experiences in data['practical_experience']:
    story.append(Paragraph(organization, style))
    story.append(Paragraph(position, style))
    for experience in experiences:
        story.append(Paragraph(experience, style))
    story.append(Spacer(1, 0.1 * inch))

# Build PDF
#print(story)
doc.build(story)


print(pdf_path)
