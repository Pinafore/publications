
class LatexLine:
    def __init__(self, num, text, comment=False, commentary=False, environment=None):
        self.num = num
        self.text = text
        self.comment = comment
        self.environment = environment
        self.commentary = commentary
        self.length = len(text)

    def can_reflow(self):
        strip_text = self.text.strip()
        if strip_text[0] == r"\n" and strip_text[-1] == "}":
            return False
        elif self.comment or self.environment is not None:
            return False
        else:
            return True

def latex_lines(raw, comment = ["%"], environments=["tabular"],
                commentary = ["comment", "todo", "ignore", "author"]):
    commentary = 0
    environment = None
    comment_regexp = re.compile("|".join(r"\\.*(" + x + r"\{" for x in commentary))
    
    for num, line in enumerate(raw.split("\n")):
        comment = False
        if "%" in line and line[line.find("%") - 1] != "\\":
            comment = True

        if environment and ("\\end{%s}" % environment) in line:
            environment = None

        if comment_regexp

