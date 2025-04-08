from pathlib import Path
from simple_file_checksum import get_checksum

algos = ['MD5', 'SHA256', 'SHA512']

def f(p):
    res = []
#    print(p.iterdir())
    for i in p.iterdir():
        if i.is_dir():
            res = res + f(i)
        else:
#            print(str(i))
            tmp = [(algo, get_checksum(str(i), algorithm=algo)) for algo in algos]
            res.append((str(i), tmp))

    return res

res = f(Path('.'))
res_str = ''
with open("checksums", "w") as f:
    for file in res:
        res_str += f"{file[0]:=^40}\n"
        for res in file[1]:
            res_str += f"Algorithm {res[0]}: {res[1]}\n"
        res_str += "=" * 40 + '\n'
    f.write(res_str)

