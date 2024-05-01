def lighten_color(color, amount=50):
    return [min(color[i] + amount, 255) for i in range(3)]

def split_words_into_lines(words, line_length):
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) <= line_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    lines.append(current_line.strip())
    return lines
