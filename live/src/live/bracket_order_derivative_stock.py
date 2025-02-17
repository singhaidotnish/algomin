from base.session import Session
import yaml
import os
from pathlib import Path

"""
    Pattern Type : Factory Pattern
    Description : If you want to dynamically call a class based on a parameter, 
    the Factory Design Pattern is the best approach. This pattern allows 
    selecting the appropriate class at runtime.
    
    The Factory Pattern is useful when you need to create objects dynamically based on 
    runtime parameters. If you have two or more parameters to decide at runtime, you 
    can implement a factory method that takes multiple arguments and returns the 
    appropriate instance.    
"""


from abc import ABC, abstractmethod

class LoadConf(ABC):
    def __init__(self, file_type_config):
        # Get the absolute path of the YAML file within the package
        _package_dir = Path(__file__).resolve().parent.parent
        self.config_file = os.path.join(_package_dir, "data", file_type_config)

    def load_config(self):
        """Load YAML configuration file."""
        with open(self.config_file, "r") as file:
            yaml_data = yaml.safe_load(file)

        result_dict = {}

        def flatten_dict(d, parent_key=""):
            """Recursively flatten nested YAML structures into a dictionary"""
            for key, value in d.items():
                new_key = f"{parent_key}.{key}" if parent_key else key
                if isinstance(value, dict):
                    flatten_dict(value, new_key)
                else:
                    result_dict[new_key] = value

        flatten_dict(yaml_data)
        return result_dict

    @abstractmethod
    def execute(self):
        pass


class MarketOrder(LoadConf):
    def execute(self):
        return "Executing Market Order"


class LimitOrder(LoadConf):
    def execute(self):
        return "Executing Limit Order"


class StopLossOrder(LoadConf):
    def execute(self):
        return "Executing Stop Loss Order"


class BracketOrderStock(LoadConf):
    def execute(self):
        return "Executing Bracket Order with config {self.config_file} "
        order_params = self.load_config()
        order_response = self.current_session.smart_api.placeOrder(order_params)
        return order_response


class BracketOrderDerivative(LoadConf):
    def execute(self):
        return "Executing Derivative Order with config {self.config_file}"
        order_params = self.load_config()
        order_response = self.current_session.smart_api.placeOrder(order_params)
        return order_response


class OrderFactory:
    @staticmethod
    def create_order(order_type, conf_type):
        orders = {
            "market": MarketOrder,
            "limit": LimitOrder,
            "stop_loss": StopLossOrder,
            "bostock": BracketOrderStock,
            "boderivative": BracketOrderDerivative
        }

        if order_type.lower() in orders:
            return orders[order_type.lower()](conf_type)
        else:
            raise ValueError(f"Unknown shape type: {order_type}")


if __name__ == "__main__":
    order_type = input("Enter Order type (stock/derivative/market/Limit/StopLoss): ").strip().lower()
    conf_type = input("Enter config type: ").strip().lower()

    try:
        order = OrderFactory.create_order(order_type, conf_type)
        print(order.execute())
    except ValueError as e:
        print(e)


def verify_login(self):
    # Step 1: Fetch User Profile to verify login
    _client_id = self.smart_api.cnf.CLIENT_ID
    profile = self.smart_api.getProfile(_client_id)
    return profile
