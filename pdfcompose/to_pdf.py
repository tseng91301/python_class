from fpdf import FPDF
import json
import os
from io import BytesIO

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def check_ascii(inp:str,min=0,max=127):
    out=1
    for i in inp:
        if ord(i) not in range(min,max):
            out=0
            break
    return out

class PDF(FPDF):

    def __init__(self):
        super().__init__()  # 調用父類別的建構函式
        self.add_font('times new roman', '', 'fonts/times new roman.ttf', uni=True)
        self.add_font('times new roman', 'B', 'fonts/times new roman B.ttf', uni=True)
        self.add_font('times new roman', 'I', 'fonts/times new roman I.ttf', uni=True)
        self.add_font('Chinese Jenhei', '','fonts/R-PMingLiU-TW-2.ttf', uni=True) # The default non-ascii word definition
        self.add_font('Chinese Jenhei', 'B','fonts/R-PMingLiU-TW-2.ttf', uni=True) # The default non-ascii word definition
        self.add_font('Chinese Jenhei', 'I','fonts/R-PMingLiU-TW-2.ttf', uni=True) # The default non-ascii word definition
        self.set_font('times new roman', '', 10)  # 設置字體

    def cell_checkword(self, w,h=0,txt='',border=0,ln=0,align='',fill=0,link=''):
        if(check_ascii(txt)==0):
            self.set_font('Chinese Jenhei','',self.font_size_pt)
        self.cell(w,h,txt,border,ln,align,fill,link)

    def chapter_title(self, title):
        self.set_font('', 'BU', 10)
        self.cell_checkword(0, 10, title, 0, 1)

    def school_title(self, titles):
        self.set_font('times new roman', 'I', 10)
        for title in titles:
            self.cell_checkword(0, 10, title, 0, 1)

    def little_title(self, titles):
        self.set_font('times new roman', 'B', 10)
        for title in titles:
            self.cell_checkword(0, 10, title, 0, 1)

    def chapter_body(self, info):
        self.set_font('times new roman', '', 10)
        for item in info:
            self.cell_checkword(0, 10, item, 0, 1)


def gen(json_data,pdf_file_name="out.pdf"):
    pdf = PDF()
    pdf.add_page()

    # Basic Information
    basic_info = json_data['basic']
    pdf.set_font_size(22)
    pdf.cell_checkword(0, 10, f"{basic_info['name']}", ln=True, align='L')
    pdf.set_font_size(10)
    pdf.set_line_width(0.8)
    current_y = pdf.get_y()
    pdf.line(10, current_y, 190, current_y)
    
    pdf.chapter_body([f"Email: {basic_info['email']}    Phone: {basic_info['phone']}"])
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell_checkword(0,10,f"Address: {basic_info['address']}",0,1,'R')
    pdf.set_font("Arial", style='', size=10)

    # Education
    pdf.chapter_title('EDUCATION')
    for edu in json_data['education']['info']:
        pdf.little_title([f"{edu['un']}"])
        pdf.school_title([f"{edu['dn']}", f"{edu['ka']}"])
        pdf.set_font("Arial", style='B', size=10)
        pdf.cell_checkword(0, 10, f"{edu['cc']}, {edu['gmy']}", 0, 1, 'R')
        pdf.set_font("Arial", style='', size=10)

    # PRACTICAL EXPERIENCE  (if any)
    if json_data['professional']['num'] > 0:
        pdf.chapter_title('PRACTICAL EXPERIENCE')
        for job in json_data['professional']['info']:
            pdf.little_title([f"{job['p']}"])
            pdf.school_title([f"{job['on']}", f"Description: {job['ka']}"])
            pdf.set_font("Arial", style='B', size=10)
            pdf.cell_checkword(0, 10, f"{job['cc']}, {job['gmy']}", 0, 1, 'R')
            pdf.set_font("Arial", style='', size=10)

    # Leadership (if any)
    if json_data['leadership']['num'] > 0:
        pdf.chapter_title('LEADERSHIP EXPERIENCE')
        for lead in json_data['leadership']['info']:
            pdf.little_title([f"{lead['p']}"])
            pdf.school_title([f"{lead['on']}", f"Description: {lead['ka']}"])
            pdf.set_font("Arial", style='B', size=10)
            pdf.cell_checkword(0, 10, f"{lead['cc']}, {lead['gmy']}", 0, 1, 'R')
            pdf.set_font("Arial", style='', size=10)

    # Skill (if any)
    if json_data['skill']['num'] > 0:
        pdf.chapter_title('SKILL')
        for item in json_data['skill']['info']:
            pdf.little_title([f"{item['t']}"])
            if(item['description']!=""):
                pdf.chapter_body([f"Description: {item['description']}"])
            if(item['proficiency']!=""):
                pdf.chapter_body([f"Proficiency level: {item['proficiency']}"])
            
    # Additional (if any)
    if json_data['additional']['num'] > 0:
        pdf.chapter_title('ADDITIONAL')
        for item in json_data['additional']['info']:
            pdf.little_title([f"{item['t']}"])
            if(item['description']!=""):
                pdf.chapter_body([f"Description: {item['description']}"])

    # Certification (if any)
    if json_data['certification']['num'] > 0:
        pdf.chapter_title('CERTIFICATION')
        for item in json_data['certification']['info']:
            pdf.school_title([f"{item['t']}"])
            if(item['org']!=""):
                pdf.chapter_body([f"Issuing organization: {item['org']}"])
            if(item['date']!=""):
                pdf.chapter_body([f"Date of issue: {item['date']}"])
            if(item['validity']!=""):
                pdf.chapter_body([f"Validity: {item['validity']}"])

    # Return PDF as byteIO object
    outf=BytesIO()
    outf.write(pdf.output(dest='S').encode("latin1")) # Will return as string and encode as "latin1"
    outf.seek(0)
    return outf