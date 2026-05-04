from concurrent.futures import ThreadPoolExecutor
import pathlib

from lib.log import Log

from ..error_fixer import ErrorFixer

from .deleter import Deleter

from .reader import Reader
from .writer import Writer
from lib.custom_types import FileInfo, RenpyError
from typing import final


@final
class FileExecutor:
    """File operations handled by thread pool executors.

    Attributes:
        max_workers: Maximum threads to perform an operation or series of operations.
    """

    max_workers = 4

    @classmethod
    def file_lines(cls, reader: Reader, arg_namespace) -> list[FileInfo]:
        files = reader.walk_files(arg_namespace.folder_or_file, arg_namespace.file_filter)
        if arg_namespace.backup:
            Writer.backup_dir(files, arg_namespace.backup)
        file_infos = None
        with ThreadPoolExecutor(cls.max_workers) as ex:
            results = ex.map(reader.read_lines, files)
            file_infos = [file_info for file_info in results]
        return file_infos

    @classmethod
    def write_files(cls, writer: Writer, file_infos: list[FileInfo]):
        with ThreadPoolExecutor(cls.max_workers) as ex:
            ex.map(writer.write_lines, file_infos)

    @classmethod
    def fix_errors(cls, error_txt: pathlib.Path, reader: Reader):
        Log.wait(f"Parsing errors from {error_txt}")
        errors = ErrorFixer.get_errors(error_txt, reader)
        with ThreadPoolExecutor(cls.max_workers) as ex:
            Log.wait("Fixing errors")
            ex.map(cls.__fix_func, errors.values())
        Log.mark("DONE! Enjoy!")

    @classmethod
    def __fix_func(cls, errors: list[RenpyError]):
        try:
            reader = Reader()
            writer = Writer()
            deleter = Deleter()
            fixer = ErrorFixer()
            fixer.fix(errors, reader, writer, deleter)
        except Exception as e:
            Log.log(f"[Error] in fix_func: {e}")
            raise
