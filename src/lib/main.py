from lib.arg import CLIParser, ArgChecker, ArgAssembler
from lib.file import Writer, FileExecutor, RenpyReader
from lib.log import Log
from lib.narrator_handler import NarratorHandler
from lib.validator.speaker import ObjectStrategy


def run():
    parser = CLIParser()
    Log.wait("Parsing user input")
    arg_namespace = parser.parse_args()
    reader = RenpyReader()
    file_executor = FileExecutor()
    if arg_namespace.folder_or_file.is_file() and arg_namespace.folder_or_file.name == "errors.txt":
        Log.complete("Parsing")
        file_executor.fix_errors(arg_namespace.folder_or_file, reader)
        return
    ArgChecker.check_args(arg_namespace)
    ArgAssembler.assemble(arg_namespace)
    Log.complete("Parsing")
    writer = Writer()
    Log.wait("Extracting lines from .rpy files")
    file_infos = file_executor.file_lines(reader, arg_namespace)
    Log.complete("Extraction")
    Log.log("Getting ready for removal process")
    ObjectStrategy.define_speakers(file_infos)
    narrator_handler = NarratorHandler()
    Log.wait("Removing narration from files. This might take a while")
    file_infos = narrator_handler.remove(file_infos, arg_namespace)
    Log.complete("Narration removal")
    Log.wait("Writing modified lines to files")
    file_executor.write_files(writer, file_infos)
    Log.log("DONE! Enjoy!")


if __name__ == "__main__":
    run()
