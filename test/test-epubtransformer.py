from io import BytesIO
import os
import warnings


def _execute_metaguider(input_file_name, metaguider):
    from transforming.epub import EpubTransformer
    from time import perf_counter
    from test_data import EPUB_OUTPUT_DIR

    _metaguider_type_name = metaguider.__class__.__name__
    print(f"Starting transforming with {_metaguider_type_name}...")
    _transformer = EpubTransformer(metaguider=metaguider)
    _t0 = perf_counter()

    _output_file_name = os.path.join(
        EPUB_OUTPUT_DIR,
        f"{os.path.basename(input_file_name)}-{_metaguider.__name__}.epub",
    )

    _test_path = os.path.dirname(os.path.abspath(__file__))
    _input_file_fullpath = os.path.join(_test_path, input_file_name)
    _output_file_name = os.path.join(_test_path, _output_file_name)

    with open(_input_file_fullpath, "rb") as _input_zip_file:
        with open(_output_file_name, "wb") as _output_zip_file:
            _output_stream = BytesIO()
            _transformer.transform_stream(_input_zip_file, _output_stream)
            _output_zip_file.write(_output_stream.getbuffer())

    print(f"{_metaguider_type_name} transforming time: {perf_counter() - _t0}")

    return True


if __name__ == "__main__":
    from transforming.metaguiding.lxmlboldmetaguider import LxmlBoldMetaguider
    from transforming.metaguiding.regex import RegExBoldMetaguider
    from test_data import (
        EPUB_TEST_FILE,
        EPUB_LARGE_TEST_FILE,
        EPUB_NON_ENGLISH_TEST_FILE,
    )

    # warnings.warn("parallel transforming is disabled")

    _metaguiders_to_test = [LxmlBoldMetaguider, RegExBoldMetaguider]
    for _metaguider in _metaguiders_to_test:
        print(f"-------------------{_metaguider.__name__}-------------------")
        print(f"Testing with {EPUB_TEST_FILE}")
        if not _execute_metaguider(EPUB_TEST_FILE, _metaguider()):
            warnings.warn(f"Execution with {_metaguider.__name__} failed")
        print(f"Testing with {EPUB_NON_ENGLISH_TEST_FILE}")
        if not _execute_metaguider(EPUB_NON_ENGLISH_TEST_FILE, _metaguider()):
            warnings.warn(f"Execution with {_metaguider.__name__} failed")
        print(f"Testing  with {EPUB_LARGE_TEST_FILE}")
        if not _execute_metaguider(EPUB_LARGE_TEST_FILE, _metaguider()):
            warnings.warn(f"Execution with {_metaguider.__name__} failed")
        print("")

    exit()
