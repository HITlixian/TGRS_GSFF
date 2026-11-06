#!/usr/bin/env python3
import argparse
import hashlib
import importlib
import json
import platform
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-root')
    parser.add_argument('--data-name', default='ZJK_10')
    args = parser.parse_args()
    failures = []
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        failures.append('需要 Linux x86_64')
    if sys.version_info[:2] != (3, 9):
        failures.append('需要 Python 3.9，当前是 ' + platform.python_version())
    for name in ('torch', 'torch_scatter', 'numpy', 'scipy', 'sklearn', 'pandas', 'matplotlib', 'seaborn', 'tqdm', 'cryptography'):
        try:
            module = importlib.import_module(name)
            print('[OK]', name, getattr(module, '__version__', 'installed'))
        except Exception as exc:
            failures.append(name + ': ' + str(exc))
    package = Path(__file__).resolve().parent
    try:
        import secure_runner
        print('[OK] 编译核心版本', secure_runner.VERSION)
        root = secure_runner._find_data_root(args.data_root, args.data_name)
        scene = root / args.data_name
        for part in ('ply_ori/' + args.data_name + '_ori.ply',
                     'ply_sub/' + args.data_name + '_sub.ply',
                     'input_ori/' + args.data_name + '_KDTree.pkl',
                     'input_ori/' + args.data_name + '_sub_proj.pkl'):
            if not (scene / part).is_file():
                failures.append('缺少文件: ' + str(scene / part))
        print('[信息] 数据目录', scene)
        from vault_reader import verify_models
        for seed, digest in verify_models().items():
            print('[OK] 加密模型校验 seed=' + seed, digest)
    except Exception as exc:
        failures.append(str(exc))
    try:
        import torch
        print('[信息] CUDA:', torch.cuda.is_available())
        if torch.cuda.is_available():
            print('[信息] GPU:', torch.cuda.get_device_name(0))
    except Exception:
        pass
    for error in failures:
        print('[失败]', error)
    print('环境检查通过。' if not failures else '环境检查未通过。')
    print('数据字段/点顺序深度校验请使用 main.py --grid --check-data。')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
