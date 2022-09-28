from inquirer import list_input, text, confirm

from .models import Vehicles, Product, DeliveryService
from .utils import unsigned_int_str, unsigned_float_str, red, yellow, green, cyan


def main() -> None:
    print()
    print(cyan("****** Transport Vehicle cyan ******"))
    print()
    try:
        transport = Vehicles(
            count=int(text(message=green("Enter number of Vehicles"), validate=unsigned_int_str)),
            speed=float(
                text(
                    message=green("Enter maximum speed of vehicle (km/hr)"),
                    validate=unsigned_float_str,
                )
            ),
            max_load=float(
                text(
                    message=green("Enter maximum load capacity of vehicle (kg)"),
                    validate=unsigned_float_str,
                )
            ),
        )
        print()
        print(cyan("****** Packages cyan ******"))
        print()
        packages_count = int(
            text(message=green("Enter number of Packages for delivery"), validate=unsigned_int_str)
        )
        cost = float(text(message=green("Enter Delivery Base Cost"), validate=unsigned_float_str))
        package_list = []
        for idx in range(1, packages_count + 1):
            print(f"*** Package {idx} ***")
            name = text(message=green("Enter the name of the package"))
            weight = float(
                text(
                    message=green(f"Enter the weight of Package - {name} (kg)"),
                    validate=unsigned_float_str,
                )
            )
            distance = float(
                text(
                    message=green(f"Enter the delivery distance of Package - {name} (km)"),
                    validate=unsigned_float_str,
                )
            )
            offer_choice = list_input(
                message=green("Choose an Offer code to apply"),
                carousel=True,
                choices=["OFR001", "OFR002", "OFR003", "None"],
                default="None",
            )
            package_list.append(
                Product(
                    name=name,
                    offer=offer_choice,
                    base_cost=cost,
                    weight=weight,
                    destination_distance=distance,
                )
            )
        service = DeliveryService(transport=transport, package_list=package_list)
        service.deliver()
        print(cyan("\n******** Delivery is Completed ********\n"))
        for package in package_list:
            print(cyan(f"**** Package {package.name} ****"))
            print(green("Offer Discount: "), package.discount(), "%")
            print(green("Total Cost: "), package.calculate_total_cost())
            print(green("Estimated Delivery Time: "), package.delivered_time, " hrs")
            print(cyan("--------------------------------------"))
    except Exception as err:
        # based on the validation setup in the inquire,
        # we would not reach here for any explicit errors
        # but to handle worst case, just in case, if any minimal bug missed
        print(red("Error: "), err)
