import argparse
import asyncio
import aiodns
import tqdm
import sys

from operator import attrgetter
host_getter = attrgetter('host')

async def get_ip(sem, resolver, dname, wildcard=None):
    try:
        async with sem:
            result = await resolver.query(dname, 'A')
    except Exception as e:
        pass
    else:
        tmp = ','.join(sorted(map(host_getter, result)))
        if tmp == wildcard:
            pass
        else:
            tqdm.tqdm.write('\r' + dname + ' ' + tmp)

async def wait_with_progress(tasks):
    for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await f


def run(name, filename):
    loop = asyncio.get_event_loop()
    resolver = aiodns.DNSResolver(loop=loop)
    # detect wildcard ip
    try:
        ips = loop.run_until_complete(asyncio.ensure_future(
            resolver.query('donainxtstomei' + '.' + name, 'A')))
    except Exception as e:
        wildcard = None
    else:
        wildcard = ','.join(sorted(map(host_getter, ips)))
    sem = asyncio.Semaphore(512)
    tasks = []
    with open('./dict/' + filename) as f:
        for line in f:
            dname = line.strip() + '.' + name
            tasks.append(asyncio.ensure_future(
                get_ip(sem, resolver, dname, wildcard=wildcard)))
    loop.run_until_complete(wait_with_progress(tasks))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Subdomain Scan', usage='python3 %(prog)s [options]', prog='subscan.py')
    parser.add_argument('--version', action='version', version='%(prog)s 2.1')
    parser.add_argument('domain', help='domain name e.g. qq.com')
    parser.add_argument(
        '-f', '--file', help='dict file in ./dict', default='subnames.txt')
    args = parser.parse_args()
    run(args.domain, args.file)
