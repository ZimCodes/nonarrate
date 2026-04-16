from lib.arg import CLIParser, ArgChecker, ArgAssembler
from lib.file import Writer, FileExecutor, RenpyReader
from lib.log import Log
from lib.narrator_handler import NarratorHandler
from lib.validator.speaker import ObjectStrategy


def run():
    parser = CLIParser()
    arg_namespace = parser.parse_args()
    reader = RenpyReader()
    file_executor = FileExecutor()
    FileExecutor.max_workers = arg_namespace.jobs
    if arg_namespace.folder_or_file.is_file() and arg_namespace.folder_or_file.name == "errors.txt":
        file_executor.fix_errors(arg_namespace.folder_or_file, reader)
        return
    ArgChecker.check_args(arg_namespace)
    ArgAssembler.assemble(arg_namespace)
    writer = Writer()
    Log.wait("Extracting lines from .rpy files")
    file_infos = file_executor.file_lines(reader, arg_namespace)
    Log.info("Files detected", len(file_infos))
    Log.log("Getting ready for removal process")
    ObjectStrategy.define_speakers(file_infos)
    narrator_handler = NarratorHandler()
    Log.wait("Removing narration from files. This might take a while")
    file_infos = narrator_handler.remove(file_infos, arg_namespace)
    Log.wait("Writing modified lines to files")
    file_executor.write_files(writer, file_infos)
    Log.mark("DONE! Enjoy!")
    total_cleaned_lines, total_lines = narrator_handler.line_stats()
    Log.log(f"""Stats:
        [Code Removed]: {total_lines - total_cleaned_lines} lines
        [Code Removed (%)]: {(total_lines - total_cleaned_lines) / total_lines * 100} %
        [Code Remaining (%)]: {(total_cleaned_lines / total_lines) * 100} %""")


if __name__ == "__main__":
    run()
