import asyncio
import argparse
from aiofile import async_open
from pathlib import Path


async def read_folder(source_path: Path): ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple program that processes numbers."
    )
    parser.add_argument(
        "source",
        type=str,
        help="source folder",
    )
    parser.add_argument(
        "dist",
        type=str,
        help="distination folder",
    )

    args = parser.parse_args()

    source_path = Path(f"./{args.source}")
    dist_path = Path(f"./{args.dist}")
    print(source_path)
