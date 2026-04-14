import os
import re
import subprocess
import zipfile
from typing import List

SYLLABUS_PATH = "syllabus-template.md"
LECTURES_DIRECTORY = "lectures"
COURSE_SKILL_ZIP = "course-assistant.skill"


def read_lines(path: str) -> List[str]:
    with open(path, encoding="utf-8") as reader:
        return [line.rstrip("\n") for line in reader]


def extract_course_title(lines: List[str]) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return "Course"


def extract_course_number(lines: List[str]) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("~ "):
            return stripped[2:].strip()
    return ""


def extract_section(lines: List[str], heading: str) -> str:
    target = heading.lower().strip()
    capturing = False
    section_lines: List[str] = []

    for line in lines:
        if capturing:
            if re.match(r"^##\s+", line):
                break
            section_lines.append(line)
        elif line.strip().lower().startswith(target):
            capturing = True

    section_lines = [line for line in section_lines if not line.strip().startswith("!INCLUDE")]
    while section_lines and not section_lines[0].strip():
        section_lines.pop(0)
    while section_lines and not section_lines[-1].strip():
        section_lines.pop()

    return "\n".join(section_lines).strip()


def get_lecture_url_base() -> str:
    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Unable to determine the lecture base URL from git remote origin."
        ) from exc

    remote_url = re.sub(r"\.git$", "", remote_url)
    if remote_url.startswith("git@github.com:"):
        path = remote_url.split(":", 1)[1]
    elif remote_url.startswith("ssh://git@github.com/"):
        path = remote_url.split("github.com/", 1)[1]
    elif re.match(r"https?://github.com/", remote_url):
        path = remote_url.split("github.com/", 1)[1]
    else:
        raise RuntimeError(
            "Git remote origin is not a recognized GitHub repository URL."
        )

    if "/" not in path:
        raise RuntimeError(
            "Git remote origin does not contain a valid owner/repository path."
        )

    owner, repo = path.split("/", 1)
    return f"https://{owner}.github.io/{repo}/lectures"


def build_skill_content(
    title: str,
    course_number: str,
    catalog_description: str,
    lecture_url_base: str,
) -> str:
    course_label = f"{title} ({course_number})" if course_number else title
    name_slug = course_number.lower().replace(" ", "-") if course_number else title.lower()
    name_slug = re.sub(r"[^a-z0-9-]", "-", name_slug)
    name_slug = re.sub(r"-+", "-", name_slug).strip("-")
    skill_name = f"{name_slug}-assistant"

    description = (
        f"Help students with labs, assignments, review, and troubleshooting for {course_label}."
    )

    catalog_block = (
        f"## Course description\n\n{catalog_description}" if catalog_description else ""
    )

    lecture_block = f"""## Lecture notes

Always check `references/lectures/` first. If the relevant concept is covered in a lecture file there, quote or paraphrase from it before going elsewhere. This reinforces the course material the student already encountered.

Lecture slides and notes are published online at {lecture_url_base}. Use the slide fragment after `#/` to jump directly to a specific slide. For example:

`lectures/26-lecture-slug.md` would become `{lecture_url_base}/26-lecture-slug.html#/slide-heading`

If available, use search to find appropriate documentation to assist with this issue. Whenever possible, include a link to both:

1. A related lecture, ideally with a direct link to a slide.
2. Helpful official documentation identified via web search.

## Images

If appropriate, include images that were used in slides. External images can be safely and appropriately hotlinked. Internal relative image paths can be translated to public urls as:

`media/5-2.png` becomes `{lecture_url_base}/media/5-2.png`

"""

    return f"""---
name: {skill_name}
description: {description}
---

# {title} Course Assistant

{catalog_block}

## How to request help

1. Identify the lab or assignment by name or number.
2. Describe the problem clearly.
3. Include error messages, unexpected output, or what you expected to happen.
4. Share the relevant code, configuration, or course material when available.
5. Tell what you have already tried.

## What this skill can help with

- Explaining course concepts and terminology.
- Reviewing lab requirements and assignment goals.
- Offering debugging strategies and troubleshooting common errors.
- Summarizing course material and guiding exam preparation.
- Helping students connect course topics to repository materials and lab exercises.

{lecture_block}

## What this skill will not do
- Complete assignments or lab work for students.
- Access external systems or private course platforms.
- Grade student work.
- Violate academic integrity policies.

## Notes for students
Provide the most context you can. The better the description and evidence of effort, the more useful the guidance will be.
"""


def build_skill_zip(skill_content: str, lecture_dir: str, output_path: str) -> None:
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("SKILL.md", skill_content)

        lecture_files = sorted(
            f
            for f in os.listdir(lecture_dir)
            if re.match(r"^[0-9].*\.md$", f)
        )
        for lecture_file in lecture_files:
            source_path = os.path.join(lecture_dir, lecture_file)
            arcname = os.path.join("references", "lectures", lecture_file)
            archive.write(source_path, arcname=arcname)


def main() -> None:
    lines = read_lines(SYLLABUS_PATH)
    title = extract_course_title(lines)
    course_number = extract_course_number(lines)
    catalog_description = extract_section(lines, "## Course Catalog Description")

    skill_content = build_skill_content(
        title,
        course_number,
        catalog_description,
        get_lecture_url_base(),
    )

    build_skill_zip(skill_content, LECTURES_DIRECTORY, COURSE_SKILL_ZIP)


if __name__ == "__main__":
    main()
