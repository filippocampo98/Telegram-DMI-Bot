import logging

from modules.dmibot.utils.lessons_utils import * 

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    scrape_lessons()

if __name__ == "__main__":
    main()