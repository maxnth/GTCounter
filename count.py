from src.Counter import Counter
import src.utils as utils

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Counts the amount of Ground Truth lines in a PAGE XML file or a "
                                                 "directory")

    parser.add_argument("-d", "--directory", help="Directory containing PAGE XML files", default=Path.cwd())
    parser.add_argument("-i", "--index", help="Index marking ground truth TextEquiv elements", default=0, type=int)
    parser.add_argument("-s", "--stats", help="Output detailed stats into csv file.",
                        action="store_true")
    parser.add_argument("-so", "--stats-out", help="Output directory for stats csv file.", default=Path.cwd())

    args = vars(parser.parse_args())

    return args


if __name__ == "__main__":
    args = main()

    utils.cprint("Counting ground truth…")
    counter = Counter(path=Path(args["directory"]), index=args["index"])
    input_type = "directory" if Path(args["directory"]).is_dir() else "file"
    utils.cprint(f"\nThis {input_type} contains {counter.get_count()} lines of ground truth.\n", style="b")

    if args["stats"]:
        counter.export_stats(Path(args["stats_out"]))
        utils.cprint("Stats exported!", fg="g")
