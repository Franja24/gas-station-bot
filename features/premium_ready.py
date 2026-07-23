from features.normal_magna import prepare_product_selection
from features.premium import run as premium_run


def run():
    prepare_product_selection()
    return premium_run()


if __name__ == "__main__":
    run()
