import logging
import os
import shutil
from datetime import datetime

from src.page import generagete_pages_recursivly

logger = logging.Logger(__name__)
logging.basicConfig(filename="static_site_generator.log", level=logging.INFO)

__PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def copy_files(source: os.path, destination: os.path) -> None:
    logging.info("=================================================")
    logging.info(f"Started copy_files: {datetime.now().timestamp()}")
    logging.debug(f"Current source: {source}")
    logging.debug(f"Current destination: {destination}")
    if not os.path.exists(source):
        raise FileNotFoundError("Source must be a valid path!")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    dirs = os.listdir(source)
    for dir in dirs:
        current_source = os.path.join(source, dir)
        current_destination = os.path.join(destination, dir)
        logging.debug(f"Inside for loop, current_source:{current_source}")
        logging.debug("Inside for loop, "
                      f"current_destinatnion:{current_destination}")
        if os.path.isfile(current_source):
            shutil.copy(current_source, current_destination)
        else:
            copy_files(current_source, current_destination)


def main() -> int:
    logging.info(f"Started: {datetime.now().timestamp()}")
    source_copy = os.path.join(__PROJECT_DIR, "static")
    destination_copy = os.path.join(__PROJECT_DIR, "public")
    copy_files(source_copy, destination_copy)
    source_generate = os.path.join(__PROJECT_DIR, "content")
    dest_generate = os.path.join(__PROJECT_DIR, "public")
    template_path = os.path.join(__PROJECT_DIR, "template.html")
    generagete_pages_recursivly(source_generate, template_path, dest_generate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
