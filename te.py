from src.file import *

infos = (
    FileProcessChain()
    .path("..")
    .exclude("node_modules")
    .min_size("10m")
    .use_yield()
    .safe_collect()
)
cnt = 0
for info in infos:
    print(info)
    cnt += 1

print(cnt)
