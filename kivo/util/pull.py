from ..stage import theStage

def make_url(tspec,r):
    prefix,name,segment = tspec
    srckey = r.get('srckey')
    if srckey is None:
        raise ValueError(f'invlid config for {prefix}.{name} - no srckey')
    return f'https://data.cityofnewyork.us/api/views/{srckey}/rows.csv?accessType=DOWNLOAD'

def make_pull_command(tspec,r):
    prefix,name,segment = tspec
    if segment is not None:
        raise NotImplementedError("segments not supported in this operation")
    url = make_url(tspec,r)
    destfile = theStage.mkpath('incoming',prefix,name,autoviv=True)
    return "curl -o %s '%s'" % (destfile,url)



