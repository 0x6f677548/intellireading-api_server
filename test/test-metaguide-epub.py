from io import BytesIO
import os

from transforming.epub import EpubTransformer
from transforming.base import DocTransformer


def _test_epub_transformer(transformer: EpubTransformer, output_to_console=False):
    # for each file in the test_data/input directory
    # run the transformer on it
    for _file in os.listdir("test_data/input"):
        if _file.endswith(".epub"):
            _input_file_name = os.path.join(EPUB_INPUT_DIR, _file)
            _output_file_name = os.path.join(EPUB_OUTPUT_DIR, _file)

            if output_to_console:
                print(f"Processing {_input_file_name} to {_output_file_name}")
            transformer.transform_file(_input_file_name, _output_file_name)
        elif output_to_console:
            print(f"Skipping {_file}")


def _test_epub_transformer_using_streams(
    transformer: DocTransformer, _output_to_console=False
):
    # for each file in the test_data/input directory
    # run the transformer on it
    for _file in os.listdir("test_data/input"):
        if _file.endswith(".epub"):
            _input_file_name = os.path.join(EPUB_INPUT_DIR, _file)
            _output_file_name = os.path.join(EPUB_OUTPUT_DIR, _file)

            if _output_to_console:
                print(f"Processing {_input_file_name} to {_output_file_name}")

            with open(_input_file_name, "rb") as _input_file:
                _input_stream = BytesIO(_input_file.read())
                _output_stream = BytesIO()
                transformer.transform_stream(_input_stream, _output_stream)
                _output_stream.seek(0)
                return _output_stream
        elif _output_to_console:
            print(f"Skipping {_file}")


if __name__ == "__main__":
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-20s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
    )

    for _handler in logging.root.handlers:
        _handler.addFilter(logging.Filter("transforming.epub"))

    from test_data import EPUB_INPUT_DIR, EPUB_OUTPUT_DIR

    _task_processor = EpubTransformer()

    for _i in range(10):
        print(f"Test {_i}")
        _test_epub_transformer(_task_processor, output_to_console=True)
        _output_stream = _test_epub_transformer_using_streams(_task_processor)
