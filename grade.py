from pathlib import Path
import sys
from collections import namedtuple
from subprocess import run, DEVNULL, PIPE
import tempfile
import shutil
import json
from subprocess import CalledProcessError
from json import JSONDecodeError
import argparse


# Usage:
#
#   python grade.py <test dir> <input dir> <report file>
#
# Assume the following input structure:
#   <input dir>/<analysis id>.dl
#
# Test directory structure:
#   <test dir>/<analysis id>/<test id>/program.c
#   <test dir>/<analysis id>/<test id>/positive.json
#   <test dir>/<analysis id>/<test id>/negative.json

analyses = [
    'dc_il1',
    'dc_il2',
    'dva_il1',
    'dva_il2',
    'nmoc_il1',
    'nmoc_il2',
    'rd_il1',
    'rd_il2',
    'uv_il1',
    'uv_il2'
]

Test = namedtuple('Test', 'file positive negative')

def load_tests(test_dir):
    '''returns analysis -> (test id -> Test)
    '''
    result = {}
    for analysis in analyses:
        tests = {}
        test_ids = load_test_ids(test_dir / analysis)
        for id in test_ids:
            test = load_test(test_dir / analysis, id)
            tests[id] = test
        result[analysis] = tests
    return result

def load_test_ids(test_dir):
    return [d.name for d in test_dir.iterdir() if d.is_dir()]

def load_test(analysis_dir, test_id):
    program_file = analysis_dir / test_id / 'program.c'
    positive_file = analysis_dir / test_id / 'positive.json'
    with positive_file.open() as f:
        positive = json.load(f)
    negative_file = analysis_dir / test_id / 'negative.json'
    with negative_file.open() as f:
        negative = json.load(f)
    return Test(program_file, positive, negative)
    
TestResult = namedtuple('TestResult', 'false_alarms missed_violations')

def is_passing(test_result):
    return len(test_result.missed_violations) == 0 and \
        len(test_result.false_alarms) == 0

def run_test(script, test):
    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            cmd = ['python3', 'analyse.py', '--analysis', str(script), str(test.file)]
            out = run(cmd, check=True, text=True, stdout=PIPE, stderr=DEVNULL)
            result = json.loads(out.stdout)
            false_alarms = []
            missed_violations = []
            for p in test.positive:
                if p not in result:
                    missed_violations.append(p)
            for n in test.negative:
                if n in result:
                    false_alarms.append(n)
            return TestResult(false_alarms, missed_violations)
        except (CalledProcessError, JSONDecodeError):
            return None

def evaluate(input_dir, tests):
    ''' returns analysis -> (test id -> TestResult)
    '''
    result = {}
    for analysis in analyses:
        analysis_file = input_dir / (analysis + '.dl')
        test_results = {}
        if not analysis_file.exists():
            for id, test in tests[analysis].items():
                test_results[id] = None
        else:
            for id, test in tests[analysis].items():
                test_results[id] = run_test(analysis_file, test)
        result[analysis] = test_results
    return result

def pprint(results):
    for analysis, test_results in results.items():
        for id, test_result in test_results.items():
            s = f"{analysis}\t{id}"
            if not test_result:
                s += "\tFAIL"
            else:
                if is_passing(test_result):
                    s += "\tOK"
                else:
                    if len(test_result.false_alarms) != 0:
                        s += f"\tFA: {test_result.false_alarms}"
                    if len(test_result.missed_violations) != 0:
                        s += f"\tMV: {test_result.missed_violations}"
            print(s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='COMP0174 Grader.')
    parser.add_argument('tests', metavar='DIR', help='test directory')
    parser.add_argument('submission', metavar='DIR', help='submission directory')
    parser.add_argument('--report', metavar='FILE', help='pdf report')
    args = parser.parse_args()
    test_dir = Path(args.tests)
    input_dir = Path(args.submission)
    tests = load_tests(test_dir)
    results = evaluate(input_dir, tests)
    pprint(results)
