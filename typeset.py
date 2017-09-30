from PIL import Image
from PIL import ImageDraw
from ocr import TranslatedBlurb


def flow_into_box(text, w, min_word_on_line=.3):
    dimg = Image.new("RGB", (100, 100))
    d = ImageDraw.Draw(dimg)
    lines = []
    idx = 0
    line = ""
    while idx < len(text):
        if not line and text[idx] == " ":
            idx += 1
        running_width = d.textsize(line)[0]
        next_token = text.find(" ", idx + 1)
        if next_token != -1:
            c_text = text[idx:next_token]
        else:
            c_text = text[idx:]
        c_width = d.textsize(c_text)[0]
        proportion_of_fit = float(w - running_width) / c_width
        if proportion_of_fit > .95:
            line += c_text
            idx += len(c_text)
        elif proportion_of_fit > min_word_on_line:
            split = max(int(proportion_of_fit * len(c_text)), 1)
            c_text = c_text[:split] + "-"
            line += c_text
            idx += len(c_text) - 1
        else:
            if line:
                lines.append(line)
                line = ""
            else:
                split = max(int(proportion_of_fit * len(c_text)), 1)
                c_text = c_text[:split] + "-"
                lines.append(c_text)
                idx += len(c_text) - 1

    if line:
        lines.append(line)

    return "\n".join(lines)


def typeset_blurb(img, blurb):
    if isintance(blurb, TranslatedBlurb):
        text = blurb.translated
    else:
        text = blurb.text

    flowed = flow_into_box(text, blurb.w)
    