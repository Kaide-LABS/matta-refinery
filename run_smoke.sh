#!/bin/bash
# Wrapper that normalizes CRLF and python alias before running the smoke test
cd /mnt/c/Users/hp/matta_demo

# Strip CRLF from all shell scripts (git on Windows writes CRLF which breaks WSL bash)
sed -i 's/\r//' scripts/phase_1_5_run.sh
sed -i 's/\r//' scripts/run_demo.sh

# Ensure 'python' resolves to python3 in this WSL session
if ! command -v python &>/dev/null && command -v python3 &>/dev/null; then
    ln -sf "$(which python3)" /tmp/python
    export PATH="/tmp:$PATH"
fi

bash scripts/phase_1_5_run.sh 1 > /mnt/c/Users/hp/matta_demo/PHASE_1_5_LOG.smoke.log 2>&1
echo "EXIT_CODE=$?" >> /mnt/c/Users/hp/matta_demo/PHASE_1_5_LOG.smoke.log
