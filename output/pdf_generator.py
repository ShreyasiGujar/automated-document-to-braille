from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def generate_pdf(text, filename="braille_output.pdf"):
    try:
        font_path = os.path.join(os.getcwd(), "fonts", "DejaVuSans.ttf")
        pdfmetrics.registerFont(TTFont('DejaVu', font_path))

        c = canvas.Canvas(filename)
        c.setFont("DejaVu", 12)

        width = 500   
        x = 50
        y = 800

        words = text.split(" ")
        line = ""

        for word in words:
            test_line = line + word + " "

            if pdfmetrics.stringWidth(test_line, "DejaVu", 12) < width:
                line = test_line
            else:
                c.drawString(x, y, line.strip())
                y -= 20
                line = word + " "

                if y < 50:
                    c.showPage()
                    c.setFont("DejaVu", 12)
                    y = 800

        if line:
            c.drawString(x, y, line.strip())

        c.save()

        return filename

    except Exception as e:
        print("PDF Error:", e)
        return None
    
