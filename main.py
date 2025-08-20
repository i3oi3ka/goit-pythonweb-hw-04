import asyncio
import argparse
import logging
from aiofile import async_open
from aiopath import AsyncPath

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("copy.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


async def read_folder(source_path: AsyncPath, dist_path: AsyncPath) -> None:
    if not await source_path.exists():
        logger.error("Source folder does not exist: %s", source_path)
        return

    async for entry in source_path.iterdir():
        if await entry.is_file():
            try:
                await copy_file(entry, dist_path)
                logger.info("Copied: %s", entry)
            except (OSError, IOError) as e:
                logger.exception("Error copying %s: %s", entry, e)
        elif await entry.is_dir():
            await read_folder(entry, dist_path)


async def copy_file(file: AsyncPath, dist_path: AsyncPath) -> None:
    suffix = file.suffix[1:] if file.suffix else "no_suffix"
    suffix_dir = dist_path / suffix
    await suffix_dir.mkdir(exist_ok=True, parents=True)
    dest_file = suffix_dir / file.name
    async with async_open(file, "rb") as src, async_open(dest_file, "wb") as dst:
        while True:
            chunk = await src.read(64 * 1024)
            if not chunk:
                break
            await dst.write(chunk)


async def main():
    parser = argparse.ArgumentParser(description="Async folder copier")
    parser.add_argument("source", type=str, help="source folder")
    parser.add_argument("dist", type=str, help="destination folder")
    args = parser.parse_args()

    source_path = AsyncPath(args.source)
    dist_path = AsyncPath(args.dist)

    await read_folder(source_path, dist_path)


if __name__ == "__main__":
    asyncio.run(main())
