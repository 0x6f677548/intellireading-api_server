from transforming.metaguiding.regex import RegExBoldMetaguider

if __name__ == "__main__":
    _test_files = [
        "test/test_data/input/app01.xhtml",
        "test/test_data/input/document_file1.xhtml",
        "test/test_data/input/document_file1.1.xhtml",
        "test/test_data/input/document_file2.xhtml",
        "test/test_data/input/document_file2.1.xhtml",
        "test/test_data/input/document_file3.xhtml",
        "test/test_data/input/document_file4.xhtml",
    ]

    from utils import perftester

    def _test_with_file(test_file: str):
        def _metaguide(
            xhtml_document: bytes, use_lxml_as_encoding_detector: bool = False
        ) -> bytes:
            _metaguider = RegExBoldMetaguider(
                use_lxml_as_main_encoding_detector=use_lxml_as_encoding_detector
            )
            return _metaguider.metaguide_xhtml_document(xhtml_document)

        def _get_test_results(
            test1name, test2name, time_for_iteration1: float, time_for_iteration2: float
        ) -> list[str]:
            _out_result_strings = []
            _out_result_strings.append(
                f"Time for {test1name}: {time_for_iteration1} (per iteration)"
            )
            _out_result_strings.append(
                f"Time for {test2name}: {time_for_iteration2} (per iteration)"
            )
            _time_relation_percentage = time_for_iteration1 / time_for_iteration2 * 100
            _fastest_test_name = (
                test1name if time_for_iteration1 < time_for_iteration2 else test2name
            )
            _out_result_strings.append(
                f"Time relation: {_time_relation_percentage:.2f}%  (test1/test2*100) {_fastest_test_name} is faster"
            )

            return _out_result_strings

        def run_comparison_test(
            test1name,
            test2name,
            test1,
            test2,
            _input_file_filecontent,
            _warmup_iteration_count,
            _stress_iteration_count,
        ) -> list[str]:
            _tester = perftester.PerfTester(name=test1name, target=test1)
            _time_for_iteration1 = _tester.run(
                _warmup_iteration_count,
                _stress_iteration_count,
                _input_file_filecontent,
            )

            _tester = perftester.PerfTester(name=test2name, target=test2)
            _time_for_iteration2 = _tester.run(
                _warmup_iteration_count,
                _stress_iteration_count,
                _input_file_filecontent,
            )

            return _get_test_results(
                test1name, test2name, _time_for_iteration1, _time_for_iteration2
            )

        with open(test_file, "rb") as _f:
            _input_file_filecontent = _f.read()
            _warmup_iteration_count = 100
            _stress_iteration_count = 100

            print("----------------------------------------")
            print(f"File: {test_file}")
            print("")

            _out_result_strings = run_comparison_test(
                "metaguide: use_lxml_as_encoding_detector=False",
                "metaguide: use_lxml_as_encoding_detector=True",
                lambda x: _metaguide(x, False),
                lambda x: _metaguide(x, True),
                _input_file_filecontent,
                _warmup_iteration_count,
                _stress_iteration_count,
            )

            # print results but with a little bit of formatting
            for _result_string in _out_result_strings:
                print(f"    {_result_string}")

            print()

    import os

    # get the path of the current module
    _current_module_path = os.path.dirname(os.path.abspath(__file__))

    _base_dir = os.path.abspath(os.path.join(_current_module_path, "../"))

    for _test_file in _test_files:
        _test_file_path = os.path.join(_base_dir, _test_file)

        _test_with_file(_test_file_path)
        print()
