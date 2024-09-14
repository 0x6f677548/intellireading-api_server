import os


def _test_with_file(
    _current_test_path,
    _input_file_fullpath,
):
    with open(_input_file_fullpath, "rb") as _f:
        _input_file_filecontent = _f.read()

    _metaguiders_to_test = [RegExBoldMetaguider, LxmlBoldMetaguider]

    _output_dir = os.path.join(_current_test_path, EPUB_OUTPUT_DIR)
    _output_file_filename = os.path.basename(_input_file_fullpath)

    print(f" --- {_input_file_fullpath} --- ")

    for _metaguider in _metaguiders_to_test:
        _output_file_fullpath = os.path.join(
            _output_dir, f"{_output_file_filename}-{_metaguider.__name__}.xhtml"
        )
        print(
            f"Testing metaguider {_metaguider.__name__}. output:  {_output_file_fullpath}"
        )

        _metaguider_instance: Metaguider = _metaguider()
        with open(_output_file_fullpath, "wb") as _f:
            _f.write(
                _metaguider_instance.metaguide_xhtml_document(_input_file_filecontent)
            )

    print("")


if __name__ == "__main__":
    from transforming.metaguiding.lxmlboldmetaguider import LxmlBoldMetaguider
    from transforming.metaguiding.regex import RegExBoldMetaguider
    from transforming.metaguiding.base import Metaguider
    from test_data import (
        XHTML_TEST_FILE,
        EPUB_OUTPUT_DIR,
        XHTML_TEST_FILE_WITH_ENTITY,
        XHTML_TEST_FILE2,
    )

    _current_test_path = os.path.dirname(os.path.abspath(__file__))
    _files_to_test = [XHTML_TEST_FILE, XHTML_TEST_FILE_WITH_ENTITY, XHTML_TEST_FILE2]

    for _file_to_test in _files_to_test:
        _input_file_fullpath = os.path.join(_current_test_path, _file_to_test)
        _test_with_file(_current_test_path, _input_file_fullpath)

    exit()
