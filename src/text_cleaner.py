import re


def clean_text(text):
    """
    Clean and normalize extracted document text.
    """

    if not text:
        return ""

    # Replace multiple spaces/tabs with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning/end of each line
    lines = [line.strip() for line in text.splitlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    # Join lines back together
    text = "\n".join(lines)

    # Remove unnecessary spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    return text.strip()


if __name__ == "__main__":

    sample_text = """
    This   is     a sample document.


    It contains     extra spaces.


    The text   needs cleaning.
    """

    print("BEFORE CLEANING:")
    print(sample_text)

    cleaned = clean_text(sample_text)

    print("\nAFTER CLEANING:")
    print(cleaned)