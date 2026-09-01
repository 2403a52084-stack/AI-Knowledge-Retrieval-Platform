from pathlib import Path
import pymupdf
from docx import Document
import pandas as pd


def load_document(file_path):
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        doc = pymupdf.open(file_path)
        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()
        return text

    elif extension == ".docx":
        doc = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
            if paragraph.text.strip()
        )

    elif extension == ".txt":
        return file_path.read_text(encoding="utf-8")

    elif extension == ".csv":
        dataframe = pd.read_csv(file_path)
        return dataframe.to_string(index=False)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )


if __name__ == "__main__":

    data_folder = Path("data")

    supported_extensions = {
        ".pdf",
        ".docx",
        ".txt",
        ".csv"
    }

    files = [
        file
        for file in data_folder.rglob("*")
        if file.is_file()
        and file.suffix.lower() in supported_extensions
    ]

    print("=" * 60)
    print("DOCUMENT LOADER TEST")
    print("=" * 60)

    print(f"Found {len(files)} documents.")

    for file in files:

        print("\n" + "=" * 60)
        print(f"FILE: {file}")
        print("=" * 60)

        try:
            text = load_document(file)

            print(f"Characters extracted: {len(text)}")
            print("\nPreview:")
            print(text[:500])

        except Exception as error:
            print(f"ERROR: {error}")