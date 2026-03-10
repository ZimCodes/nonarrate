import os
from concurrent.futures import ThreadPoolExecutor

from .reader import Reader
from .writer import Writer


class FileExecutor:
    """File operations handled by thread pool executors.

    Attributes:
        max_workers: Maximum threads to perform an operation or series of operations.
    """

    max_workers = (os.cpu_count() or 1) * 2 + 4

    @classmethod
    def file_lines(cls, reader: Reader, root_dir: str) -> list[dict[str, list[str]]]:
        files = reader.walk_files(root_dir)
        file_infos = None
        with ThreadPoolExecutor(cls.max_workers) as ex:
            results = ex.map(reader.read_lines, files)
            file_infos = [file_info for file_info in results]
        return file_infos

    @classmethod
    def write_files(cls, writer: Writer, file_info: dict[str, list[str]]):
        with ThreadPoolExecutor(cls.max_workers) as ex:
            ex.map(writer.write_lines, list(file_info), list(file_info.values()))
