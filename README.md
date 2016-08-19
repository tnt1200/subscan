# subscan
Subdomain brute force based on Python 3.5

## Requirement

* [aiodns](https://github.com/saghul/aiodns)
* [tqdm](https://github.com/noamraph/tqdm)

## Usage

```
usage: python3 subscan.py [options]

Subdomain Scan

positional arguments:
  domain                domain name e.g. qq.com

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -f FILE, --file FILE  dict file in ./dict
```

## TODO

- [x] DNS Wild Card checks
- [ ] DNS Zone Transfer checks
- [ ] customizable dns server
- [ ] customizable semaphore