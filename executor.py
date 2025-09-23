import argparse
import os
import numpy as np
from contextlib import closing
from datetime import datetime
from multiprocessing import Pool
from functools import partial

GPU2IDS = {
    0: [_ for _ in range(0, 12)],
    1: [_ for _ in range(12, 25)],
    2: [_ for _ in range(25, 37)],
    3: [_ for _ in range(37, 50)],
    4: [_ for _ in range(50, 62)],
    5: [_ for _ in range(62, 75)],
    6: [_ for _ in range(75, 87)],
    7: [_ for _ in range(87, 100)],
}

def run_compose(ids, output):
    for data_id in ids:
        cmd = f"bash scripts/run/sample_compose.sh {data_id} {output} > compose_{data_id:03}.log"
        print(cmd)
        os.system(cmd)
        #os.system(f"echo {data_id} > log_{data_id}.log")
    return

def run_eval(ids, output):
    for data_id in ids:
        cmd = f"bash scripts/run/eval_vina_full.sh {data_id} {output} > eval_{data_id:03}.log"
        print(cmd)
        os.system(cmd)
    return

def compose_candidates(run, workers, output):
    ids_list = np.array_split(
        np.array(GPU2IDS[run]),
        workers
    )
    f = partial(run_compose, output=output)
    with closing(Pool(workers)) as pool:
        pool.starmap(
            f,
            ([a.tolist(), ] for a in ids_list)
        )
    return

def eval_candidates(run, workers, output):
    ids_list = np.array_split(
        np.array(GPU2IDS[run]),
        workers
    )
    f = partial(run_eval, output=output)
    with closing(Pool(workers)) as pool:
        pool.starmap(
            f,
            ([a.tolist(), ] for a in ids_list)
        )
    return

def best_mol_candidates(run, output):
    for data_id in GPU2IDS[run]:
        cmd = f".venv/bin/python scripts/select_best_arm.py {output}/sampling_{data_id:03} > best_arm_{data_id:03}.log"
        print(cmd)
        #os.system(f"ls -larth {output}/sampling_{data_id:03}")
        os.system(cmd)
    return

def main(args):
    t0 = datetime.now()
    if args.compose:
         compose_candidates(
            run=args.run,
            workers=args.workers,
            output=args.output
         )
    elif args.eval:
        eval_candidates(
            run=args.run,
            workers=args.workers,
            output=args.output
        )
    elif args.best:
        best_mol_candidates(
            run=args.run,
            output=args.output
        )
    else:
        raise ValueError("Either `compose` or `eval` or `best` must be specified")
    t1 = datetime.now()
    print(f"Script {__name__} execution time: {t1 - t0}")
    return


def parse_input():
    parser = argparse.ArgumentParser(description='Process script input arguments.')
    parser.add_argument('--compose', action='store_true', help="Run compose bash script")
    parser.add_argument('--eval', action='store_true', help="Run evaluation bash script")
    parser.add_argument('--best', action='store_true', help="Select best mol script")
    parser.add_argument('--run', type=int, help="Specify the GPU Number", required=True)
    parser.add_argument('--workers', type=int, default=2, help="Specify the number of workers")
    parser.add_argument('--output', type=str, default="/home/root/DecompOpt/output", help="Specify the output directory")
    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_input()
    main(ARGS)
