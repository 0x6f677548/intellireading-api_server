if __name__ == "__main__":
    from transforming.metaguiding.lxmlboldmetaguider import LxmlBoldMetaguider
    from transforming.metaguiding.regex import RegExBoldMetaguider
    from utils.perftester import PerfTester
    from test_data import XHTML_TEST_FILE

    with open(XHTML_TEST_FILE, "rb") as f_:
        _file_content = f_.read()

    _metaguiders_to_test = [LxmlBoldMetaguider(), RegExBoldMetaguider()]

    _warmup_iterations = 10
    _stress_iterations = 50

    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(name)-20s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S",
    )

    for _handler in logging.root.handlers:
        _handler.addFilter(logging.Filter("utils.perftester"))

    for _metaguider in _metaguiders_to_test:
        _tester = PerfTester(
            _metaguider.metaguide_xhtml_document, _metaguider.__class__.__name__
        )
        _tester.run(_warmup_iterations, _stress_iterations, _file_content)
