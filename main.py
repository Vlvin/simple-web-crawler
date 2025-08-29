from selenium import webdriver
import sys
from selenium.common.exceptions import WebDriverException
import sqlalchemy
from sqlalchemy import Integer, String
import re

from sqlalchemy.orm import DeclarativeBase, MappedColumn, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Page(Base):
    __tablename__ = "page"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    url: MappedColumn[str] = mapped_column(String(255))
    title: MappedColumn[str] = mapped_column(String(255))
    contents: MappedColumn[str] = mapped_column(String)


class WebCrawler:
    DEFAULT_FIRST_PAGE = "https://thebestmotherfucking.website/"
    LINK_PATTERN = """["']http[s]{0,1}://[^"']*["']"""

    def __init__(self, database_name: str = "database.bd", *starting_urls: str):

        self.starting_urls = starting_urls
        self.gonna_crowl = [*starting_urls] or [self.DEFAULT_FIRST_PAGE]
        self._engine = sqlalchemy.create_engine(f"sqlite:///{database_name}")

        Base.metadata.create_all(self._engine)

    def start_crawl(self):
        self.db_session: Session = Session(self._engine)
        self.driver: webdriver.Chrome = webdriver.Chrome()
        try:
            for url in self.gonna_crowl:
                print(f"Crawling through { url }")
                try:
                    self.driver.get(url)
                except WebDriverException as e:
                    print(f"Error: { e.msg }")  # unsuccesfull
                    continue
                self.db_session.add(
                    Page(
                        url=url,
                        title=self.driver.title,
                        contents=self.driver.page_source,
                    )
                )
                self.db_session.commit()
                self.gonna_crowl.remove(url)
                urls = list(
                    map(
                        lambda x: x[1:-1],
                        re.findall(self.LINK_PATTERN, self.driver.page_source),
                    )
                )
                self.gonna_crowl.extend(urls)

        except KeyboardInterrupt:
            print("Crawler Shutting down...")
            with open("gonna_crawl.txt", "w+") as f:
                f.write("\n".join(self.gonna_crowl))
            self.driver.quit()
            self.db_session.close()


def main(*argv):
    crawler = WebCrawler("database.bd", *argv[1:])
    crawler.start_crawl()
    # driver = webdriver.Chrome()
    # GONNA_CROWL = [DEFAULT_FIRST_PAGE]
    # worker_session = Session(engine)
    # link_pattern = """["']http[s]{0,1}://[^"']*["']"""
    # i = 0
    # try:
    #     while i < 4:
    #         for url in GONNA_CROWL:
    #             print(url)
    #             try:
    #                 driver.get(url)
    #             except WebDriverException as e:
    #                 print(e.msg)
    #                 continue
    #             worker_session.add(
    #                 Page(url=url, title=driver.title, contents=driver.page_source)
    #             )
    #             worker_session.commit()
    #             GONNA_CROWL.remove(url)
    #             urls = list(
    #                 map(lambda x: x[1:-1], re.findall(link_pattern, driver.page_source))
    #             )
    #             GONNA_CROWL.extend(urls)
    # except KeyboardInterrupt:
    #     pass
    # print(len(GONNA_CROWL))
    # print(GONNA_CROWL)
    # driver.quit()
    # worker_session.close()
    #


if __name__ == "__main__":
    main(*sys.argv)
