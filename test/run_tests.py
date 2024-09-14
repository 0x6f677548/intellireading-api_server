import runpy


if __name__ == "__main__":
    # check if have an argument with the test name
    import sys

    if len(sys.argv) > 1:
        _test_name = sys.argv[1]
    else:
        # ask the user wants to run all tests or a specific test
        _test_name = input("Enter test name (or 'all' to run all tests): ")

    if _test_name == "all":
        # echo the test name
        print("Running all tests")
        print("----------------")
        print("Running test-EpubTransformer.py")

        runpy.run_path("test-EpubTransformer.py")

        print("----------------")
        print("Running test-metaguide-epub-perf.py")
        runpy.run_path("test-metaguide-epub-perf.py")

        print("----------------")
        print("Running test-metaguide-epub.py")
        runpy.run_path("test-metaguide-epub.py")

        print("----------------")
        print("Running test-metaguiders-perf.py")
        runpy.run_path("test-metaguiders-perf.py")

        print("----------------")
        print("Running test-metaguiders.py")
        runpy.run_path("test-metaguiders.py")
    else:
        print(f"Running test {_test_name}")
        runpy.run_path(f"{_test_name}")
