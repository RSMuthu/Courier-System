import json
import click

from pydantic import ValidationError

from .models import Vehicles, Product, DeliveryService
from .utils import red, yellow, green, cyan


@click.command()
@click.option(
    "--file",
    "-f",
    "file_name",
    prompt=f"[{ yellow('?') }] {green('Enter JSON input file path')}",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def main(file_name):
    try:
        with open(file_name, "r") as file:  # load from inp json file
            data = json.load(file)
        print(cyan("\n******** Data has been Loaded ********\n"))
        # Create necessary instances
        transport = Vehicles.parse_obj(data["transport"])
        package_list = [Product.parse_obj(item) for item in data["products"]]
        service = DeliveryService(transport=transport, package_list=package_list)
        # Delivery trigger
        service.deliver()
        print(cyan("\n******** Delivery is Completed ********\n"))
        # Display all product info after delivery
        for package in package_list:
            print(cyan(f"**** Package {package.name} ****"))
            print(green("Offer Discount: "), package.discount(), "%")
            print(green("Total Cost: "), package.calculate_total_cost())
            print(green("Estimated Delivery Time: "), package.delivered_time, " hrs")
            print(cyan("--------------------------------------"))
    except (ValidationError) as e:
        print(red("Error: Model Validation Failed"))
        # One Validation err can have multiple (type) errors occured in different fields
        for err in e.errors():
            print(f'{yellow(err["type"])} - Field \'{err["loc"][0]}\' - {err["msg"]}')
    except Exception as e:
        # Unknown exceptions need detailed error info dump
        print(red("Error: "), e, repr(e))
