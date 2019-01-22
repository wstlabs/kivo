import argparse
import kivo.fcache

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tempo", type=str, required=False, default="monthly", help="tempo")
    parser.add_argument("--source", type=str, required=False, help="source")
    return parser.parse_args()

def do_source(journal,tempo,source):
    trunk = journal.trunk(tempo,source)
    print(trunk)
    for root,dirs,files in trunk.walk():
        print(f"root = {root}, dirs = {dirs}, files = {files}")
    dirs = trunk.getdirs()
    files = trunk.getfiles()
    print(f"dirs = {dirs}, files = {files}")


def main():
    args = parse_args()
    tempo = args.tempo
    source = args.source
    journal = kivo.fcache.journal.instance()
    print(journal)
    print(list(journal.sources(tempo)))
    if source is not None:
        print("do {source} ...")
        do_source(journal,tempo,source)
    else:
        print("do all ..")
        for source in journal.sources(tempo):
            do_source(journal,tempo,source)


if __name__ == '__main__':
    main()
