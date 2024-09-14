#!/bin/bash
#run all tests

echo "-- Running all tests --"
echo "Running test-epubtransformer.py"
python test-epubtransformer.py
echo "-----------------------------"
echo "Running test-metaguide-epub-perf.py"
python test-metaguide-epub-perf.py
echo "-----------------------------"
echo "Running test-metaguide-epub.py"
python test-metaguide-epub.py
echo "-----------------------------"
echo "Running test-metaguiders-perf.py"
python test-metaguiders-perf.py

echo "-----------------------------"
echo "Running test-metaguiders.py"
python test-metaguiders.py