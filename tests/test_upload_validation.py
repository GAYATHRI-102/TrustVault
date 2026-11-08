from io import BytesIO
from werkzeug.datastructures import FileStorage

from routes.documents import validate_file_content


def test_fake_pdf_is_rejected():
    fake_file = FileStorage(
        stream=BytesIO(b"This is only a text file."),
        filename="fake.pdf"
    )

    assert validate_file_content(fake_file) is False


def test_genuine_pdf_is_accepted():
    genuine_pdf = FileStorage(
        stream=BytesIO(
            b"%PDF-1.4\n"
            b"1 0 obj\n"
            b"<< /Type /Catalog >>\n"
            b"endobj\n"
            b"%%EOF"
        ),
        filename="genuine.pdf"
    )

    assert validate_file_content(genuine_pdf) is True