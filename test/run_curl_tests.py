import sys


if __name__ == "__main__":
    # check arguments
    if len(sys.argv) < 3:
        print(
            "Usage: run_curl_tests.py <target_host:port> <api_key> [sleep_time_seconds]"
        )
        exit(1)

    # get target host and port from first argument in foprmat host:port
    _target_host = sys.argv[1]
    _api_key = sys.argv[2]

    # check if we have a third argument with time to sleep between tests
    _sleep_time = 0
    if len(sys.argv) > 3:
        _sleep_time = int(sys.argv[3])

    filetocheck = "@test_data/input/400files.epub"

    _tests = [
        [
            f"http://{_target_host}/metaguiding/epub/transform?api-key={_api_key}",
            filetocheck,
        ],
#        [
#            f"http://{_target_host}/metaguiding/epub/transform?api-key=badkey",
#            filetocheck,
#        ],
#        [f"http://{_target_host}/metaguiding/epub/transform", filetocheck],
    ]

    for _test in _tests:
        _url = _test[0]
        _file = _test[1]
        print(f"Testing {_url}")
        # run curl with the target url
        import subprocess

        # pylint: disable=subprocess-run-check
        _curl_process = subprocess.run(
            [
                "curl",
                "-X",
                "POST",
                _url,
                "-H",
                "Content-Type: multipart/form-data",
                "-H",
                "accept: application/json",
                "-F",
                f"file={_file};type=application/epub+zip",
                "--output",
                "output.epub",
                "-w",
                "\n\rx-response-time: %{time_total}s\n\rstatus-code: %{http_code}\n\r",
            ],
            capture_output=True,
        )
        # print the output
        print(_curl_process.stdout.decode("utf-8"))
        print(_curl_process.stderr.decode("utf-8"))
        print("----------------")
        # sleep if needed
        if _sleep_time > 0:
            import time

            print(f"Sleeping for {_sleep_time} seconds")
            time.sleep(_sleep_time)
