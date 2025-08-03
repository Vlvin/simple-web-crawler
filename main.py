from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import re

from sqlalchemy.orm import DeclarativeBase, MappedColumn, Session, mapped_column

FIRST_PAGE = "https://thebestmotherfucking.website/"


class Base(DeclarativeBase):
    pass


class Page(Base):
    __tablename__ = "page"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    url: MappedColumn[str] = mapped_column(String(255))
    title: MappedColumn[str] = mapped_column(String(255))
    contents: MappedColumn[str] = mapped_column(String)


engine = sqlalchemy.create_engine("sqlite:///database.bd")

Base.metadata.create_all(engine)


def main():
    driver = webdriver.Chrome()
    GONNA_CROWL = [FIRST_PAGE]
    worker_session = Session(engine)
    link_pattern = """["']http[s]{0,1}://[^"']*["']"""
    i = 0
    try:
        while i < 4:
            for url in GONNA_CROWL:
                print(url)
                try:
                    driver.get(url)
                except WebDriverException as e:
                    print(e.msg)
                    continue
                worker_session.add(
                    Page(url=url, title=driver.title, contents=driver.page_source)
                )
                worker_session.commit()
                GONNA_CROWL.remove(url)
                urls = list(
                    map(lambda x: x[1:-1], re.findall(link_pattern, driver.page_source))
                )
                GONNA_CROWL.extend(urls)
    except KeyboardInterrupt:
        pass
    print(len(GONNA_CROWL))
    print(GONNA_CROWL)
    driver.quit()
    worker_session.close()


if __name__ == "__main__":
    main()
