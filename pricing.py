from models import PrintType


class PrintingPrices:
    """Class to manage printing prices per page (in PHP)"""
    PRICES = {
        PrintType.BLACK_AND_WHITE: 2.00,
        PrintType.COLORED: 5.00,
        PrintType.PHOTO_PAPER: 20.00
    }


def calculate_order_cost(print_type: PrintType, num_pages: int) -> float:
    """
    Calculate the total cost of an order based on print type and number of pages.

    Args:
        print_type: Type of printing (black_and_white, colored, photo_paper)
        num_pages: Number of pages to print

    Returns:
        Total cost in PHP
    """
    price_per_page = PrintingPrices.PRICES.get(print_type, 0)
    return price_per_page * num_pages


def get_all_prices() -> dict:
    """Get all available printing prices"""
    return {
        "prices": [
            {
                "type": PrintType.BLACK_AND_WHITE,
                "price_per_page": PrintingPrices.PRICES[PrintType.BLACK_AND_WHITE],
                "currency": "PHP"
            },
            {
                "type": PrintType.COLORED,
                "price_per_page": PrintingPrices.PRICES[PrintType.COLORED],
                "currency": "PHP"
            },
            {
                "type": PrintType.PHOTO_PAPER,
                "price_per_page": PrintingPrices.PRICES[PrintType.PHOTO_PAPER],
                "currency": "PHP"
            }
        ]
    }
