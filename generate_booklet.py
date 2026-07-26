from pathlib import Path

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "haolin-baptism-program-booklet.pdf"
PHOTO = ROOT / "photos" / "IMG_0240.jpg"
W, H = letter

INK = HexColor("#163944")
BLUE = HexColor("#74B8CF")
BLUE_DARK = HexColor("#327F99")
BLUE_SOFT = HexColor("#E8F5F8")
CORAL = HexColor("#E78F7B")
CORAL_SOFT = HexColor("#FBE8E1")
GOLD = HexColor("#EACB77")
CREAM = HexColor("#FFFAF1")
WHITE = HexColor("#FFFFFF")
MUTED = HexColor("#607D84")


def register_fonts():
    candidates = {
        "Sans": "/System/Library/Fonts/Supplemental/Avenir Next.ttc",
        "Serif": "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "SerifItalic": "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    }
    for name, path in candidates.items():
        try:
            pdfmetrics.registerFont(TTFont(name, path))
        except Exception:
            pass


def font(name, fallback):
    return name if name in pdfmetrics.getRegisteredFontNames() else fallback


register_fonts()
SANS = font("Sans", "Helvetica")
SERIF = font("Serif", "Times-Roman")
SERIF_ITALIC = font("SerifItalic", "Times-Italic")


def fit_image(c, path, x, y, width, height):
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = max(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(image, x + (width - dw) / 2, y + (height - dh) / 2,
                width=dw, height=dh, preserveAspectRatio=True, mask="auto")


def rounded_label(c, text, x, y, width, fill, text_color=INK):
    c.setFillColor(fill)
    c.roundRect(x, y, width, 22, 11, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont(SANS, 7.2)
    c.drawCentredString(x + width / 2, y + 7.2, text.upper())


def draw_rainbow(c, cx, y, scale=1):
    c.saveState()
    c.setLineCap(1)
    for radius, color in [(54, CORAL), (44, GOLD), (34, BLUE)]:
        c.setStrokeColor(color)
        c.setLineWidth(6 * scale)
        c.arc(cx - radius * scale, y - radius * scale,
              cx + radius * scale, y + radius * scale, 0, 180)
    c.restoreState()


def draw_leaf(c, x, y, angle, size=1, color=HexColor("#739B78")):
    c.saveState()
    c.translate(x, y)
    c.rotate(angle)
    c.setFillColor(color)
    path = c.beginPath()
    path.moveTo(0, 0)
    path.curveTo(8 * size, 3 * size, 12 * size, 12 * size, 1 * size, 18 * size)
    path.curveTo(-7 * size, 11 * size, -6 * size, 4 * size, 0, 0)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.setStrokeColor(Color(1, 1, 1, alpha=.42))
    c.setLineWidth(.45)
    c.line(0, 2 * size, 1 * size, 14 * size)
    c.restoreState()


def draw_leaf_branch(c, x, y, height, mirror=False):
    direction = -1 if mirror else 1
    c.saveState()
    c.setStrokeColor(HexColor("#6E9575"))
    c.setLineWidth(1.4)
    path = c.beginPath()
    path.moveTo(x, y)
    path.curveTo(x + 12 * direction, y + height * .30,
                 x - 8 * direction, y + height * .70,
                 x + 7 * direction, y + height)
    c.drawPath(path, fill=0, stroke=1)
    leaves = [(.12, 18), (.25, -22), (.39, 24), (.54, -20), (.70, 22), (.84, -18)]
    greens = [HexColor("#86A989"), HexColor("#6F9878"), HexColor("#9BB89A")]
    for idx, (fraction, angle) in enumerate(leaves):
        yy = y + height * fraction
        xx = x + (7 if idx % 2 == 0 else -4) * direction
        draw_leaf(c, xx, yy, angle * direction, .78, greens[idx % len(greens)])
    c.restoreState()


def footer(c, page_num):
    c.setStrokeColor(Color(0.13, 0.31, 0.36, alpha=0.15))
    c.setLineWidth(0.5)
    c.line(42, 28, W - 42, 28)
    c.setFillColor(MUTED)
    c.setFont(SANS, 6.8)
    c.drawString(42, 16, "HAOLIN LUO'S BAPTISM  -  JULY 26, 2026")
    c.drawRightString(W - 42, 16, str(page_num))


def page_cover(c):
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(BLUE_DARK)
    c.setFont(SANS, 8.2)
    c.drawCentredString(W / 2, H - 58, "WITH JOYFUL HEARTS, WE CELEBRATE")
    c.setFillColor(CORAL)
    c.setFont(SERIF_ITALIC, 24)
    c.drawCentredString(W / 2, H - 94, "Haolin Luo's")
    c.setFillColor(INK)
    c.setFont(SERIF, 40)
    c.drawCentredString(W / 2, H - 136, "Baptism")

    photo_w, photo_h = 360, 270
    photo_x, photo_y = (W - photo_w) / 2, 292
    c.setFillColor(CREAM)
    c.roundRect(photo_x - 10, photo_y - 10, photo_w + 20, photo_h + 20, 18, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#C9DCCB"))
    c.setLineWidth(1.2)
    c.roundRect(photo_x - 5, photo_y - 5, photo_w + 10, photo_h + 10, 14, fill=0, stroke=1)

    c.saveState()
    clip = c.beginPath()
    clip.roundRect(photo_x, photo_y, photo_w, photo_h, 10)
    c.clipPath(clip, stroke=0, fill=0)
    fit_image(c, PHOTO, photo_x, photo_y, photo_w, photo_h)
    c.restoreState()

    draw_leaf_branch(c, photo_x - 18, photo_y - 8, 150, mirror=True)
    draw_leaf_branch(c, photo_x + photo_w + 18, photo_y + 185, 150, mirror=False)
    draw_leaf_branch(c, photo_x + 8, photo_y + photo_h - 32, 94, mirror=True)
    draw_leaf_branch(c, photo_x + photo_w - 5, photo_y - 30, 96, mirror=False)
    draw_leaf(c, photo_x - 2, photo_y + photo_h + 4, -55, .9, HexColor("#B4C9A8"))
    draw_leaf(c, photo_x + photo_w + 3, photo_y - 2, 120, .9, HexColor("#B4C9A8"))

    c.setStrokeColor(BLUE)
    c.setLineWidth(1)
    c.line(184, 208, W - 184, 208)
    c.setFillColor(INK)
    c.setFont(SANS, 10.5)
    c.drawCentredString(W / 2, 179, "SUNDAY  -  JULY 26, 2026  -  5:00 PM")
    c.setFillColor(MUTED)
    c.setFont(SANS, 7.1)
    c.drawCentredString(W / 2, 148, "THE CHURCH OF JESUS CHRIST OF LATTER-DAY SAINTS")
    draw_rainbow(c, W / 2, 101, .42)
    c.showPage()


PROGRAM = [
    ("Presiding", "Bishop Esplin"),
    ("Witnesses", "Jim Macdonald & Brooke Macdonald"),
    ("Pianist", "Stephen Jones"),
    ("Chorister", "Lindsey Darley"),
    ("Opening Song", "When I Am Baptized"),
    ("Opening Prayer", "Suzi Mageno"),
    ("Talk on Baptism", "Stephen Jones"),
    ("Baptism", "Xi Luo"),
    ("Restoration Presentation", "Sister Mower & Sister Kincaid"),
    ("Talk on the Holy Ghost", "Xi Luo"),
    ("Receiving the Gift of the Holy Ghost", "Alex Mageno"),
    ("Closing Song", "Holding Hands Around the World"),
    ("Closing Prayer", "Kaitlin Felsted"),
]


def page_program(c):
    c.setFillColor(BLUE_SOFT)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_rainbow(c, W - 78, H - 52, .55)
    rounded_label(c, "Order of service", 42, H - 72, 104, WHITE)
    c.setFillColor(INK)
    c.setFont(SERIF, 31)
    c.drawString(42, H - 116, "Baptism Program")
    c.setFillColor(MUTED)
    c.setFont(SANS, 9)
    c.drawRightString(W - 42, H - 105, "Sunday, July 26, 2026")
    c.setFillColor(BLUE_DARK)
    c.setFont(SANS, 10)
    c.drawRightString(W - 42, H - 120, "5:00 PM")

    top = H - 166
    col_w = 246
    gap = 34
    row_h = 73
    for idx, (role, name) in enumerate(PROGRAM):
        col = idx % 2
        row = idx // 2
        x = 42 + col * (col_w + gap)
        y = top - row * row_h
        special = role in ("Baptism", "Receiving the Gift of the Holy Ghost")
        if special:
            c.setFillColor(WHITE)
            c.roundRect(x, y - 57, col_w, 67, 12, fill=1, stroke=0)
        c.setFillColor(CORAL if "Song" in role else BLUE_DARK)
        c.circle(x + 13, y - 23, 11, fill=1, stroke=0)
        c.setFillColor(WHITE)
        if "Song" in role:
            c.circle(x + 10, y - 27, 2.6, fill=1, stroke=0)
            c.setStrokeColor(WHITE)
            c.setLineWidth(1.2)
            c.line(x + 12.4, y - 26, x + 12.4, y - 17)
            c.line(x + 12.4, y - 17, x + 17, y - 19)
        else:
            c.setFont(SANS, 6.5)
            c.drawCentredString(x + 13, y - 25.5, f"{idx + 1:02d}")
        c.setFillColor(MUTED)
        c.setFont(SANS, 6.4)
        c.drawString(x + 35, y - 12, role.upper())
        c.setFillColor(INK)
        c.setFont(SERIF, 11.3 if len(name) < 28 else 9.7)
        c.drawString(x + 35, y - 31, name)
        c.setStrokeColor(Color(0.13, 0.31, 0.36, alpha=0.15))
        c.line(x + 35, y - 53, x + col_w, y - 53)

    c.setFillColor(INK)
    c.setFont(SERIF_ITALIC, 13)
    c.drawCentredString(W / 2, 47, "Thank you for celebrating this special day with us.")
    footer(c, 2)
    c.showPage()


WHEN_BAPTIZED = [
    ("1", [
        "I like to look for rainbows whenever there is rain",
        "And ponder on the beauty of the earth made clean again.",
        "I want my life to be as clean as earth right after rain.",
        "I want to be the best I can and live with God again.",
    ]),
    ("2", [
        "I know when I am baptized I choose the Savior's way,",
        "And I will be forgiven as I turn to Him each day.",
        "I want my life to be as clean as earth right after rain.",
        "I want to be the best I can and live with God again.",
    ]),
]


HOLDING_HANDS = [
    ("1", [
        "We are children singing all around the world,",
        "Happy voices ringing out the joyful word.",
        "We are children glowing with the gospel light,",
        "Standing tall, walking strong, choosing right.",
        "",
        "We are children leading out in ev'ry land",
        "Who believe in keeping all the Lord's commands.",
        "Like the stripling warriors we go forth in faith,",
        "For we know that the Lord is our strength.",
    ]),
    ("2", [
        "We are children sharing all around the world,",
        "Leading other children to the gospel fold.",
        "With the strength of youth, we do the Savior's work.",
        "With our hearts and our hands we will serve.",
        "",
        "We are cov'nant children with a gift to give.",
        "We will teach the gospel by the way we live.",
        "With each word and action, we will testify:",
        "We believe, and we serve Jesus Christ.",
    ]),
]

CHORUS = [
    "We are children holding hands around the world,",
    "Like an army with the gospel flag unfurled.",
    "We are led by His light,",
    "And we love truth and right.",
    "We are building the kingdom of God.",
]


def song_header(c, kicker, title, author, color):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    rounded_label(c, kicker, 42, H - 72, 100, color, INK)
    c.setFillColor(INK)
    title_size = 30 if len(title) < 25 else 25
    c.setFont(SERIF, title_size)
    c.drawString(42, H - 117, title)
    c.setFillColor(MUTED)
    c.setFont(SANS, 8.5)
    c.drawString(42, H - 138, author)
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.line(42, H - 154, W - 42, H - 154)


def verse(c, number, lines, x, y, width, leading=21, size=11.5):
    c.setFillColor(BLUE_DARK)
    c.circle(x + 13, y - 8, 13, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(SANS, 8)
    c.drawCentredString(x + 13, y - 11, number)
    style = ParagraphStyle("lyrics", fontName=SERIF, fontSize=size,
                           leading=leading, textColor=INK, spaceAfter=0)
    text = "<br/>".join(line if line else "&nbsp;" for line in lines)
    p = Paragraph(text, style)
    _, ph = p.wrap(width - 44, 400)
    p.drawOn(c, x + 40, y - ph)
    return y - ph - 18


def page_song_one(c):
    song_header(c, "Opening song", "When I Am Baptized", "Words and music by Nita Dale Milner", BLUE_SOFT)
    draw_rainbow(c, W - 85, H - 80, .62)
    y = H - 190
    for number, lines in WHEN_BAPTIZED:
        y = verse(c, number, lines, 42, y, W - 84, leading=44, size=20)
        if number == "1":
            c.setStrokeColor(Color(0.13, 0.31, 0.36, alpha=0.12))
            c.line(82, y + 8, W - 42, y + 8)
            y -= 18
    footer(c, 3)
    c.showPage()


def draw_chorus(c, x, y, width):
    c.setFillColor(CORAL_SOFT)
    c.roundRect(x, y - 154, width, 162, 16, fill=1, stroke=0)
    c.setFillColor(CORAL)
    c.setFont(SANS, 7)
    c.drawString(x + 18, y - 15, "CHORUS")
    style = ParagraphStyle("chorus", fontName=SERIF_ITALIC, fontSize=12.4,
                           leading=21.5, textColor=INK, alignment=TA_CENTER)
    p = Paragraph("<br/>".join(CHORUS), style)
    _, ph = p.wrap(width - 30, 120)
    p.drawOn(c, x + 15, y - 27 - ph)


def page_song_two(c):
    song_header(c, "Closing song", "Holding Hands Around the World",
                "Words and music by Janice Kapp Perry", CORAL_SOFT)
    col_w = (W - 72) / 2
    top = H - 185
    verse(c, "1", HOLDING_HANDS[0][1], 24, top, col_w, leading=20.5, size=11.5)
    verse(c, "2", HOLDING_HANDS[1][1], 48 + col_w, top, col_w, leading=20.5, size=11.5)
    draw_chorus(c, 42, 220, W - 84)
    footer(c, 4)
    c.showPage()


def generate():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = Canvas(str(OUTPUT), pagesize=letter, pageCompression=1)
    c.setTitle("Haolin Luo's Baptism Program")
    c.setAuthor("The Luo Family")
    page_cover(c)
    page_program(c)
    page_song_one(c)
    page_song_two(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    generate()
