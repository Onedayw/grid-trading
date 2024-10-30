from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

class RestClient(ABC):
    _ENDPOINT = "https://"

    @abstractmethod
    def get_markets(self) -> List[dict]:
        pass

    @abstractmethod
    def get_orderbook(self, market: str, depth: int = None) -> dict:
        pass

    @abstractmethod
    def get_trades(self, market: str, start_time: float = None, end_time: float = None) -> dict:
        pass

    @abstractmethod
    def get_account_info(self) -> dict:
        pass

    @abstractmethod
    def get_open_orders(self, market: str = None) -> List[dict]:
        pass 

    @abstractmethod
    def get_order_history(
        self, market: str = None, side: str = None, order_type: str = None,
        start_time: float = None, end_time: float = None
    ) -> List[dict]:
        pass

    @abstractmethod
    def modify_order(
        self, existing_order_id: Optional[str] = None,
        existing_client_order_id: Optional[str] = None, price: Optional[float] = None,
        size: Optional[float] = None, client_order_id: Optional[str] = None,
    ) -> dict:
        pass

    @abstractmethod
    def place_order(self, market: str, side: str, price: float, size: float, type: str = 'limit',
                    reduce_only: bool = False, ioc: bool = False, post_only: bool = False,
                    client_id: str = None, reject_after_ts: float = None) -> dict:
        pass

    @abstractmethod
    def cancel_order(self, market: str, order_id: int = None) -> dict:
        pass

    @abstractmethod
    def cancel_orders(self, market: str) -> dict:
        pass

    @abstractmethod
    def get_fills(
        self, market: str = None, start_time: float = None,
        end_time: float = None, min_id: int = None, order_id: int = None) -> List[dict]:
        pass

    @abstractmethod
    def get_balances(self) -> List[dict]:
        pass

    @abstractmethod
    def get_all_balances(self) -> List[dict]:
        pass

    @abstractmethod
    def get_positions(self, show_avg_price: bool = False) -> List[dict]:
        pass

    @abstractmethod
    def get_position(self, name: str, show_avg_price: bool = False) -> dict:
        pass

    @abstractmethod
    def get_all_trades(self, market: str, start_time: float = None, end_time: float = None) -> List:
        pass
