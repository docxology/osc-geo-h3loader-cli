#!/bin/bash
set -ex # Add -x for debugging

# Activate virtual environment
source /home/trim/Documents/GitHub/GEO-INFER/GEO-INFER-SPACE/repo/osc-geo-h3loader-cli/venv/bin/activate

# Add GEO-INFER-SPACE/src to PYTHONPATH for tests to find shared modules
export PYTHONPATH="/home/trim/Documents/GitHub/GEO-INFER/GEO-INFER-SPACE/src:$PYTHONPATH"

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install the current repository in editable mode
echo "Installing current repository in editable mode..."
pip install -e .

# Determine test directory and run tests
TEST_DIR=""
if [ -d "test" ]; then
    TEST_DIR="test/"
elif [ -d "tests" ]; then
    TEST_DIR="tests/"
fi

if [ -n "$TEST_DIR" ]; then
    echo "Running internal tests for osc-geo-h3loader-cli in $TEST_DIR..."
    # Use the venv's pytest
    /home/trim/Documents/GitHub/GEO-INFER/GEO-INFER-SPACE/repo/osc-geo-h3loader-cli/venv/bin/pytest $TEST_DIR
else
    echo "No 'test/' or 'tests/' directory found, skipping internal tests for osc-geo-h3loader-cli."
    exit 0 # Exit successfully if no tests to run
fi
