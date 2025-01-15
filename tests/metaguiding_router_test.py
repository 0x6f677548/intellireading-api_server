from fastapi.testclient import TestClient
from intellireading.api_server.app import app
from intellireading.client.metaguiding import _METAGUIDED_FLAG_FILENAME
import os

client = TestClient(app)


def test_metaguiding_epub_transform():

    # get the epub test file path from the tests folder
    epub_test_filename = os.path.join(os.path.dirname(__file__), "test_files", "input.epub")

    # Open the file in binary mode for uploading
    with open(epub_test_filename, "rb") as f:

        # Prepare headers with a valid API key from the environment
        headers = {"X-API-Key": os.environ.get("API_SERVER_API_KEY")}

        # Use the valid EPUB file for upload
        response = client.post(
            "metaguiding/epub/transform", headers=headers, files={"file": ("test.epub", f, "application/epub+zip")}
        )

        # Check if the response status code is 201 (OK)
        assert response.status_code == 201

        # create a byte stream from the response content
        import io

        output_stream = io.BytesIO(response.content)
        import zipfile

        with zipfile.ZipFile(output_stream, "r") as zip_ref:
            # check if the flag file exists in the zip file
            exists = False
            for file in zip_ref.filelist:
                if file.filename == _METAGUIDED_FLAG_FILENAME:
                    exists = True
                    break

            assert exists


def test_metaguiding_xhtml_transform_simpleinput():

    # get the xhtml test file path from the tests folder
    xhtml_test_filename = os.path.join(os.path.dirname(__file__), "test_files", "simpleinput.xhtml")

    # Open the file in binary mode for uploading
    with open(xhtml_test_filename, "rb") as f:

        # Prepare headers with a valid API key
        headers = {"X-API-Key": os.environ.get("API_SERVER_API_KEY")}

        # Use the valid XHTML file for upload
        response = client.post(
            "metaguiding/xhtml/transform", headers=headers, files={"file": ("test.xhtml", f, "application/xhtml+xml")}
        )

        # Check if the response status code is 201 (OK)
        assert response.status_code == 201

        # create a byte stream from the response content
        import io

        output_stream = io.BytesIO(response.content)

        xhtml_assertion_filename = os.path.join(os.path.dirname(__file__), "test_files", "simpleinput-result.xhtml")
        with open(xhtml_assertion_filename, "rb") as xhtml_assertion_file:
            output_stream.seek(0)

            # check if the content of the file is the same as the input file
            assert output_stream.read() == xhtml_assertion_file.read()


def test_metaguiding_xhtml_transform():

    # get the xhtml test file path from the tests folder
    xhtml_test_filename = os.path.join(os.path.dirname(__file__), "test_files", "input.xhtml")

    # Open the file in binary mode for uploading
    with open(xhtml_test_filename, "rb") as f:

        # Prepare headers with a valid API key
        headers = {"X-API-Key": os.environ.get("API_SERVER_API_KEY")}

        # Use the valid XHTML file for upload
        response = client.post(
            "metaguiding/xhtml/transform", headers=headers, files={"file": ("test.xhtml", f, "application/xhtml+xml")}
        )

        # Check if the response status code is 201 (OK)
        assert response.status_code == 201
