from typing import Iterator, List


class Pagination:
    def __init__(self, text: str, symbols_on_page: int = 5):
        self._text = text
        self._symbols_on_page = symbols_on_page
        self._paginated_text = tuple(self.paginate_text(text, symbols_on_page))

    @staticmethod
    def paginate_text(text: str, symbols_on_page: int) -> Iterator[str]:
        temp = 0

        while temp < len(text):
            yield text[temp: temp + symbols_on_page]
            temp += symbols_on_page

    @property
    def page_count(self) -> int:
        return len(self._paginated_text)

    @property
    def item_count(self) -> int:
        return len(self._text)

    def count_items_on_page(self, page_number: int) -> int:
        try:
            return len(self._paginated_text[page_number])
        except IndexError:
            raise IndexError("Invalid index. Page is missing.")

    def display_page(self, page_number: int) -> str:
        try:
            return self._paginated_text[page_number]
        except IndexError:
            raise IndexError("Invalid index. Page is missing.")

    def find_page(self, str_to_search: str) -> List[int]:
        found_pages = []
        for i, page_text in enumerate(self._paginated_text):
            if str_to_search in page_text or page_text.replace(" ", "") in str_to_search:
                found_pages.append(i)

        if not found_pages:
            raise ValueError(f"'{str_to_search}' is missing on the pages")
        return found_pages


if __name__ == "__main__":
    pages = Pagination("Your beautiful text", 5)
    print(pages.page_count)
    print(pages.item_count)
    print(pages.count_items_on_page(0))
    print(pages.count_items_on_page(3))

    try:
        print(pages.count_items_on_page(4))
    except IndexError as e:
        print(f"{e.__class__.__name__}: {e}")

    print(pages.find_page("Your"))
    print(pages.find_page("e"))
    print(pages.find_page("beautiful"))
    try:
        print(pages.find_page("great"))
    except ValueError as e:
        print(f"{e.__class__.__name__}: {e}")
    print(pages.display_page(0))
