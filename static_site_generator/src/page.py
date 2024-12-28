import os
import logging

from src.adapter import markdown_to_html_node
from src.extracter import extract_title


logger = logging.getLogger(__name__)


def generate_page(from_path: os.path,
                  template_path: os.path,
                  dest_path: os.path) -> None:
    logging.info(f"Generating page from {from_path} to "
                 f"{dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown: str = f.read()
    with open(template_path, "r") as f:
        template: str = f.read()
    page_title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", html)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    with open(os.path.join(dest_path, "index.html"), "w+") as f:
        f.write(template)


def generagete_pages_recursivly(dir_path_content: os.path,
                                template_path: os.path,
                                dest_dir_path: os.path
                                ) -> None:
    dirs: list[str] = os.listdir(dir_path_content)
    if not os.path.exists(dest_dir_path):
        logging.info(f"Made dir {dest_dir_path}")
        os.mkdir(dest_dir_path)
    logging.info(f"current dirs:{dirs}")
    for dir in dirs:
        current_dir = os.path.join(dir_path_content, dir)
        current_dest_dir = os.path.join(dest_dir_path, dir)
        logger.info(f"{current_dir=}")
        logger.info(f"{current_dest_dir=}")
        if os.path.isfile(current_dir) and str(current_dir).endswith(".md"):
            logger.info("We in.")
            generate_page(current_dir, template_path, dest_dir_path)
        elif os.path.isdir(current_dir):
            generagete_pages_recursivly(current_dir,
                                        template_path,
                                        current_dest_dir)
