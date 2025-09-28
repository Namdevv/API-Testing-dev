# src.utils.preprocessing.section_preprocessing
import re
from typing import Optional

from src.utils.common import is_number
from src.utils.preprocessing.text_preprocessing import remove_extra_whitespace


def is_section_heading(line, extra_patterns: Optional[list[str]] = None) -> bool:
    """
    Check if a line is a valid section heading in a technical document.

    Section headings can be:
    - Numbered headings: e.g., "1. Title", "1.2) Subtitle", "3.1: Details", "2.1- Section"
    - Roman numeral headings: e.g., "II. Introduction", "IV) Results", "V: Discussion", "III- Analysis"
    - Uppercase headings: e.g., "KẾT LUẬN", "GIỚI THIỆU"
    """

    # Remove leading '#' characters and surrounding whitespace
    removed_sharp = re.sub(r"^\s*#+\s*", "", line)

    # Pattern for numbered section headings
    numbered_pattern = r"^\s*\d+(\.\d+)*[.\):\-]?\s+.+"
    is_matched_numbered = bool(re.match(numbered_pattern, removed_sharp))

    # Pattern for Roman numeral section headings, with ) or : or - after numerals
    roman_pattern = r"^\s*[IVXLCDM]+[.\):\-]?\s+.+"
    is_matched_roman = bool(re.match(roman_pattern, removed_sharp))
    # Pattern for uppercase headings (at least 5 letters and mostly uppercase)

    uppercase_pattern = r"^[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯẠ-ỹ ]{5,}$"
    is_matched_uppercase = bool(re.match(uppercase_pattern, removed_sharp))

    is_extra_pattern_matched = False
    if extra_patterns:
        for pattern in extra_patterns:
            if re.match(pattern, line):
                is_extra_pattern_matched = True
                break

    return (
        is_matched_numbered
        or is_matched_roman
        or is_matched_uppercase
        or is_extra_pattern_matched
    )


def pattern_mining(text, min_occurrences=3) -> dict:
    pattern = r"^([#\*]*\s*)([a-zA-Z0-9]+)([-:\.)]+)\s*([a-zA-Z0-9]+)\s*([#\*]*\s*)"

    lines = text.splitlines()
    prefix_counts = {}

    for line in lines:
        m = re.match(pattern, line)
        if m:
            separator = m.group(3).replace(".", r"\.")
            prefix = (
                rf"{m.group(1)}"
                + (r"\d+" if is_number(m.group(2)) else r"\w+")
                + rf"{separator}"
            )
            code = m.group(4)
            key = prefix + (r"\d+" if is_number(code) else r"\w+")

            if r"\d+" not in key:
                continue

            prefix_counts[key] = prefix_counts.get(key, 0) + 1

    prefix_counts = dict(
        sorted(
            [item for item in prefix_counts.items() if item[1] >= min_occurrences],
            key=lambda x: x[1],
            reverse=True,
        )
    )

    return prefix_counts


def get_all_section_headings(text: str, mine_pattern: bool = False) -> list[str]:
    """
    Extract all section headings from the given text.

    Args:
        text (str): The input text to search for section headings.

    Returns:
        list: A list of all section headings found in the text.
    """

    mined_patterns = list(pattern_mining(text).keys()) if mine_pattern else []

    lines = text.splitlines()

    section_headings = []
    for line in lines:
        if is_section_heading(line, extra_patterns=mined_patterns):
            pattern = r"\s*#*\s*(.*)\s*"
            match = re.match(pattern, line)
            section_heading = None
            if match:
                section_heading = match.group(1)
            else:
                section_heading = line.strip()

            section_headings.append(section_heading)

    return section_headings


def is_a_child_of(current_section: str, parent_section: str) -> bool:
    # Implement logic to determine if current_section is a child of parent_section
    curr_heading = re.sub(r"^\s*#+\s*", "", current_section)
    parent_heading = re.sub(r"^\s*#+\s*", "", parent_section)

    curr_heading = curr_heading.strip().split(" ")[0]
    parent_heading = parent_heading.strip().split(" ")[0]

    return curr_heading.startswith(parent_heading) and curr_heading != parent_heading


def extract_section_content(
    text: str, curr_section_heading: str, next_section_heading: Optional[str] = None
) -> str:
    """
    Extract the content of a section from the text.

    Args:
        text (str): The input text to search within.
        curr_section_heading (str): The heading of the current section.
        next_section_heading (str): The heading of the next section.

    Returns:
        str: The content of the current section.
    """

    # Check if current section heading exists in text
    if curr_section_heading not in text:
        return ""

    # Check if next section heading exists in text (if provided)
    if next_section_heading and next_section_heading in text:
        pattern = (
            rf"^\s*#*\s*{re.escape(curr_section_heading)}\s*\n(.*?)"
            rf"(?=^\s*#*\s*{re.escape(next_section_heading)}|\Z)"
        )
    else:
        pattern = rf"^\s*#*\s*{re.escape(curr_section_heading)}\s*\n(.*)"

    match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    if match:
        return remove_extra_whitespace(text=match.group(1), ignore_code_blocks=True)

    return ""


def extract_section_contents(text: str, section_headings: list[str]) -> dict[str, str]:
    """
    Extract contents for multiple sections based on their headings.
    Args:
        text (str): The input text to search within.
        section_headings (list[str]): List of section headings to extract content for.
    Returns:
        dict[str, str]: A dictionary mapping section headings to their extracted content.
    """

    section_to_content = {}

    # Extract content for each section
    for i, current_heading in enumerate(section_headings):
        next_heading = (
            section_headings[i + 1] if i + 1 < len(section_headings) else None
        )
        section_to_content[current_heading.strip()] = extract_section_content(
            text, current_heading, next_heading
        )

    return section_to_content


def create_parent_child_blocks(section_headings: list[str]) -> list[list[str]]:
    """
    Create blocks of parent-child section headings.

    Each block contains a parent section and one of its child sections.
    For example, "1. ABC" with subsections "1.1 ABC" and "1.2 ABC" will be split into
    separate blocks: [["1. ABC", "1.1 ABC"], ["1. ABC", "1.2 ABC"]]

    Args:
        section_headings (list[str]): List of section headings.

    Returns:
        list[list[str]]: List of blocks, each containing a parent section with one child section.
    """

    parent_child_blocks: list[list[str]] = []
    current_parent_child_group: list[str] = []

    for i, current_heading in enumerate(section_headings):
        current_parent_child_group.append(current_heading)
        # Find parent sections for current heading
        for previous_heading in section_headings[i::-1]:
            if is_a_child_of(current_heading, previous_heading):
                current_parent_child_group.append(previous_heading)

        parent_child_blocks.append(current_parent_child_group)
        current_parent_child_group = []

    # Filter blocks that have parent-child relationships (more than 1 section)
    parent_child_blocks = [block for block in parent_child_blocks if len(block) > 1]

    return parent_child_blocks


def create_hierarchical_section_blocks(
    section_to_content: dict[str, str], parent_child_blocks: list[list[str]]
) -> list[str]:
    """
    Create hierarchical section blocks containing parent-child relationships.

    Each block contains a parent section and one of its child sections with their content.
    For example, "1. ABC" with subsections "1.1 ABC" and "1.2 ABC" will be split into
    separate blocks: ["1. ABC\n1.1 ABC\n..."] and ["1. ABC\n1.2 ABC\n..."]

    Args:
        section_to_content (dict[str, str]): A dictionary mapping section headings to their content.
        parent_child_blocks (list[list[str]]): List of blocks, each containing a parent section with one child section.

    Returns:
        list[str]: List of text blocks, each containing a parent section with one child section.
    """

    # Generate text blocks with parent and child content
    hierarchical_text_blocks = []

    for parent_child_group in parent_child_blocks:
        combined_block_text = ""
        # Reverse to put parent first, then child
        for section_heading in parent_child_group[:2][::-1]:
            # Remove leading '#' if present
            clean_heading = section_heading
            combined_block_text += f"{clean_heading}"
            content = section_to_content[section_heading.strip()]
            if content:
                combined_block_text += f"\n{content}\n"
            else:
                combined_block_text += "\n"

        hierarchical_text_blocks.append(combined_block_text)

    return hierarchical_text_blocks
