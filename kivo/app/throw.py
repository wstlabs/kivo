import os
import argparse
from collections import namedtuple
import kivo.fcache
from kivo.fcache.utils import is_valid_source
import ioany

# location of the deployment dir
DEPLOY = 'deploy'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", type=str, required=False, default="current", help="issue")
    parser.add_argument("--force", action="store_true", help="override default protections")
    parser.add_argument("--dry", action="store_true", help="dry run, do nothing invasive (overrides --force)")
    return parser.parse_args()

def derive(srcobj,source):
    assert srcobj is not None
    assert is_valid_source(source)
    root,ext = os.path.splitext(srcobj)
    print(f"root = '{root}', ext = '{ext}'")
    return f"{source}{ext}"


RStat = namedtuple('RStat',['family','source','label','version','found','srcpath','dstpath'])
def resolve(journal,issue,inrecs):
    for r in inrecs:
        family = None
        source,version,label = r['source'],r['version'],r['phase']
        # print(f"source = {source}, version = {version}, phase = {label}")
        trunk = journal.locate_distinct(source)
        # print(f"trunk = {trunk}")
        found,srcpath,dstpath = False,None,None
        if trunk:
            family = trunk.family
            phase = trunk.phase(label=label)
            # print(f"phase = {phase}")
            if phase.is_active:
                srcobj = phase.locate_distinct(version)
                # print(f"srcobj = {srcobj}")
                if srcobj is not None:
                    found = True
                    srcpath = phase.fullpath(srcobj)
                    # print(f"srcpath = {srcpath}")
                    dstobj = derive(srcobj,source)
                    # print(f"dstobj = {dstobj}")
                    dstpath = issue.fullpath(dstobj)
                    # print(f"dstpath = {dstpath}")
        yield RStat(
            family=family,
            source=source,
            label=label,
            version=version,
            found=found,
            srcpath=srcpath,
            dstpath=dstpath)

def setup(args):
    stage = kivo.fcache.stage.instance()
    journal = kivo.fcache.journal.instance()
    issuetag = args.issue
    print(f"issuetag = {issuetag}")
    issuedir = stage.resolve(issuetag)
    print(f"issuedir = {issuedir} = {issuedir.path}")
    infile = f"{DEPLOY}/{issuetag}.csv"
    if not os.path.exists(infile):
        raise RuntimeError("can't fine deployment schedule '{infile}'")
    inrecs = ioany.slurp_recs(infile)
    n = len(inrecs)
    print(f"that be {n} deployment recs.")
    return journal,issuedir,inrecs


def main():
    args = parse_args()
    journal,issue,inrecs = setup(args)
    status = list(resolve(journal,issue,inrecs))
    nifty = [r for r in status if r.found]
    n = len(nifty)
    print(f"that be {n} nifty recs.")
    for r in nifty:
        print(r)
    print("all done.")


if __name__ == '__main__':
    main()


"""
    if issuetag == 'current':
        # if the 'current' alias is invoked, we require it to be a symbolic link (and already present as such). 
        if not issuedir.is_active:
            raise ValueError("the 'current' issue directory, unlike the others, cannot be auto-instantiated")
        if not issuedir.islink:
            raise ValueError("the 'current' issue needs to exist as a symbolic link, not an actual directory")
    else:
        # otherwise, we go ahead and autovivify.
        if not issuedir.is_active:
            issuedir.vivify()
"""
