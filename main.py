import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, MAIN_DOC_URL
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session: requests_cache.CachedSession):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")

    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")

    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})
    sections_by_python = div_with_ul.find_all(
        "li", attrs={"class": "toctree-l1"}
    )
    results = [("Ссылка на статью", "Заголовок", "Редактор, автор")]
    for section in tqdm(sections_by_python, desc="Parsing versions"):
        version_a_tag = find_tag(section, "a")
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)

        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features="lxml")

        h1 = find_tag(soup, "h1")
        dl = find_tag(soup, "dl")
        dl_text = dl.text.replace("\n", " ")

        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session: requests_cache.CachedSession):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, features="lxml")

    sidebar = find_tag(soup, "div", attrs={"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")

    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
        else:
            raise Exception("Ничего не нашлось")

    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"
    results = [("Ссылка на документацию", "Версия", "Статус")]
    for a_tag in a_tags:
        link = a_tag.get("href")
        if match := re.match(pattern, a_tag.text):
            version, status = match.group("version"), match.group("status")
        else:
            version, status = a_tag.text, ""
        results.append((link, version, status))

    return results


def download(session: requests_cache.CachedSession):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")

    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")

    download_table = find_tag(soup, "table", attrs={"class": "docutils"})
    pdf_a4_tag = find_tag(
        download_table,
        "a",
        attrs={"href": re.compile(r".+pdf-a4\.zip$")},
    )
    archive_url = urljoin(downloads_url, pdf_a4_tag["href"])

    filename = archive_url.split("/")[-1]
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = get_response(session, archive_url)

    with open(archive_path, "wb") as file:
        file.write(response.content)

    logging.info(f"Архив был загружен и сохранён: {archive_path}")


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
}


def main():
    configure_logging()
    logging.info("Парсер запущен")

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode

    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)

    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
