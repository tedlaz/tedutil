""" Requires reportlab (pip install reportlab)
for ttf fonts:
wget http://www.lucius-hartmann.ch/diverse/greekfonts/docs/alkaios_win.zip

http://www.polytoniko.org/fonts.php
https://www.keymangreek.gr/site/polytoniko.php?option=fonts
install fonts in ~/.local/share/fonts and run:
  $ fc_cache
"""
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
from reportlab.lib.pagesizes import portrait
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


pdfmetrics.registerFont(TTFont('fn', "Alkaios.ttf"))
pdfmetrics.registerFont(TTFont('fni', "Alkaios-Italic.ttf"))
pdfmetrics.registerFont(TTFont('fb', "Alkaios-Bold.ttf"))
pdfmetrics.registerFont(TTFont('fbi', "Alkaios-BoldItalic.ttf"))
fn, fni, fb, fbi = 'fn', 'fni', 'fb', 'fbi'


def parf(value, font=fn, align=1):
    """Δημιουργεί παράγραφο με γραμματοσειρά και ζύγισμα
    """
    alin = {1: TA_LEFT, 2: TA_CENTER, 3: TA_RIGHT, 4: TA_JUSTIFY}
    styles = getSampleStyleSheet()
    stylen = styles["BodyText"]
    stylen.alignment = alin[align]
    stylen.fontName = font
    return Paragraph(value, stylen)


def draw_footer(message, canvas, page_width, pagenum=True):
    canvas.saveState()
    canvas.setFont(fni, 10)
    canvas.drawString(cm+8, cm-3, message)
    if pagenum:
        pnumber = canvas.getPageNumber()
        canvas.drawString(page_width-cm, cm-3, "Σελίδα: %s" % pnumber)
    canvas.setLineWidth(0.01)
    # canvas.setDash(1, 3)
    canvas.line(cm, cm+8, page_width+cm+3, cm+8)
    canvas.restoreState()


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(fb, 14)
    canvas.drawCentredString(doc.width/2+20, doc.height+40, doc.title)
    canvas.setFont(fni, 9)
    draw_footer(doc.footer, canvas, doc.width)
    canvas.restoreState()


def render2pdf(filename, title, data, is_portrait=True, autoresize=True):
    tmargin = 60
    bmargin = 30
    lmargin = 30
    rmargin = 30
    width, height = A4
    if is_portrait:
        orientation = portrait
    else:
        width, height = height, width
        orientation = landscape
    column_sizes = [i * cm for i in data['szs']]
    tot_width = sum(column_sizes)
    allowed_width = width - lmargin - rmargin
    # Auto resize
    if autoresize:
        final_sizes = []
        for el in column_sizes:
            final_sizes.append(el/tot_width * allowed_width)
    else:
        final_sizes = column_sizes
    # print(width, height, allowed_width, tot_width, allowed_width - tot_width)
    # Δημιουργία γραμμών για πίνακα
    rdata = list()
    rdata.append([parf(i, fb, 2) for i in data['head']])
    for el in data['lns']:
        rdata.append([parf(i, fn, j) for i, j in zip(el, data['aln'])])
    rdata.append([parf(i, fb, j) for i, j in zip(data['sum'], data['aln'])])
    # Εισαγωγή γραμμών σε πίνακα
    table = Table(rdata, final_sizes, repeatRows=1)
    table.hAlign = 'CENTER'
    def_styles = [
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('INNERGRID', (0, 0), (-1, -2), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -2), 0.25, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE')
    ]
    table.setStyle(TableStyle(def_styles))
    elements = list()
    elements.append(table)
    doc = SimpleDocTemplate(filename,
                            pagesize=orientation(A4),
                            rightMargin=rmargin,
                            leftMargin=lmargin,
                            topMargin=tmargin,
                            bottomMargin=bmargin)
    doc._doSave = 0
    doc.title = title
    doc.footer = data.get('footer', title)
    doc.build(elements, onFirstPage=first_page, onLaterPages=first_page)
    canvas = doc.canv
    canvas.setTitle(doc.title)
    canvas.save()
