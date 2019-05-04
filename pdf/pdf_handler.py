from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os


class PdfHandler:
    def __init__(self, page_name: str, user_id: str):
        self._directory = 'user_files/user_id_{}'.format(user_id)
        self._create_directory()
        name = os.path.join(self._directory, page_name + '.pdf')
        #self._canvas = canvas.Canvas(name, pagesize=A5)
        #self._canvas.setLineWidth(.3)
        #self._canvas.setFont('Helvetica', 12)
        self.doc = SimpleDocTemplate(name, pagesize=A5,
                                     rightMargin=65, leftMargin=65,
                                     topMargin=50, bottomMargin=18)
        self.story = []
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    def _create_directory(self) -> None:
        try:
            if not os.path.exists(self._directory):
                os.makedirs(self._directory)
        except Exception as e:
            print('error')

    def set_document_title(self, title: str):
        title = '<font size=14>{}</font>'.format(title)
        self.story.append(Paragraph(title, self.styles['Title']))

    def write_document(self, text: str) -> bool:
        text = '<font size=12>{}</font>'.format(text)
        self.story.append(Paragraph(text, self.styles["Justify"]))
        self.story.append(Spacer(1, 12))
        return self.save()

    def save(self) -> bool:
        try:
            self.doc.build(self.story)
            return True
        except Exception as e:
            return False


if __name__ == '__main__':
    page = 'page_1'
    user_id = str(123)
    test = 'I am a test from the emergency broadcast system. This is only a test, but if it wasnt a test, this would be a message regarding some sort of zombie apocalypse, because zomies are real, and apocalypses are even more real. Dont take this lightly or you will get clamedya and die.'
    title = 'Acknowledgement'
    pdf_writer = PdfHandler(page, user_id)
    pdf_writer.set_document_title(title)
    success = pdf_writer.write_document(test)
    if success:
        print('success')