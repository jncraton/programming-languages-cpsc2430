import os
import re
import yaml

lectures = [f for f in os.listdir("lectures") if re.match("^\d\d.*html$", f)]
lectures.sort()


def get_reading(lecture):
    """Returns the url for any reading from yaml metadata in lecture"""

    with open(lecture) as f:
        md = "".join(f.readlines()[:10])

        matches = re.search(r"\-\-\-.*?\.\.\.", md, flags=re.M | re.DOTALL)

        if matches:
            yaml_block = matches.group(0)
            yaml_block = yaml_block[3:-3]
            meta = yaml.safe_load(yaml_block)

            return meta.get("reading", "")

        return ""


with open("lectures/index.md", "w") as out:
    out.write("# Lectures\n\n")

    out.write("Day|Slides|Reading\n")
    out.write(":--|:-----|:------\n")

    for lecture in lectures:
        day = re.search("\d\d", lecture).group(0)
        description = lecture[2:-5]
        description = description.replace("-", " ")
        description = description.title().strip()
        slides = lecture
        markdown = lecture.replace(".html", ".md")

        reading = get_reading("lectures/" + markdown)

        out.write(f"{int(day)}|[{description}]({lecture})|{reading}\n")

    out.write("\n[Combined Slides](all-slides.html)")
