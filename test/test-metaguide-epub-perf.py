from io import BytesIO
import os
import logging

from transforming.base import DocTransformer


def _perf_test_using_streams(transformer: DocTransformer):
    from utils.perftester import PerfTester

    _transformer_tester = PerfTester(transformer.transform_stream, "EpubTransformer")
    _warmup_iterations = 5
    _stress_iterations = 10

    _input_file_name = EPUB_LARGE_TEST_FILE
    with open(_input_file_name, "rb") as input_file:
        _input_stream = BytesIO(input_file.read())
        _output_stream = BytesIO()
        _transformer_tester.run(
            _warmup_iterations, _stress_iterations, _input_stream, _output_stream
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(name)-20s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S",
    )

    for _handler in logging.root.handlers:
        _handler.addFilter(logging.Filter("utils.perftester"))

    from transforming.epub import EpubTransformer
    from taskprocessing.iterablesprocessing import (
        SyncTaskProcessor,
        ProcessPoolTaskProcessor,
        DummyProcessPoolTaskProcessor,
    )
    from test_data import EPUB_LARGE_TEST_FILE

    _number_of_cores = os.cpu_count()
    _task_processors = [
        SyncTaskProcessor(),
        ProcessPoolTaskProcessor(_number_of_cores),
        ProcessPoolTaskProcessor(2),
        DummyProcessPoolTaskProcessor(_number_of_cores),
        DummyProcessPoolTaskProcessor(2),
    ]

    # print the number of cpu cores
    print("Number of cpu cores: ", os.cpu_count())
    # print the free memory
    print(
        "Free memory: ",
        os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_AVPHYS_PAGES") / (1024.0**3),
        "GB",
    )

    from transforming.metaguiding.lxmlboldmetaguider import LxmlBoldMetaguider
    from transforming.metaguiding.regex import RegExBoldMetaguider

    _metaguiders = [RegExBoldMetaguider(), LxmlBoldMetaguider()]

    for _metaguider in _metaguiders:
        print("--- metaguider: " + str(_metaguider) + " ---")
        for _task_processor in _task_processors:
            print("Testing task processor: " + str(_task_processor))
            _perf_test_using_streams(
                EpubTransformer(task_processor=_task_processor, metaguider=_metaguider)
            )
            print("")

        print(
            "Free memory: ",
            os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_AVPHYS_PAGES") / (1024.0**3),
            "GB",
        )
