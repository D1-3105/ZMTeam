import logging

from .pool import PoolFactory
from typing import Callable

logger = logging.getLogger(__name__)


class PoolExecutor:
    pool_factory_class: 'Type | None'
    __fact_kwargs: 'dict | None' = None
    __factory_instance: 'PoolFactory | None' = None

    def __init__(
            self,
            pool_factory_class: 'Type | None' = PoolFactory,
            **factory_kwargs
    ):
        self.pool_factory_class = pool_factory_class
        self.__fact_kwargs = factory_kwargs or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._factory.close()

    def _init_factory(self):
        return self.pool_factory_class(**self.__fact_kwargs)

    @property
    def _factory(self):
        if not self.__factory_instance:
            self.__factory_instance = self._init_factory()
        return self.__factory_instance

    @staticmethod
    def default_callback(result):
        """
            Callback for target
        """
        return print(f"Process performed with result: {result}")

    @staticmethod
    def default_error_callback(target):
        target.close()

    def run(
            self,
            target: Callable,
            callback: 'Callable | None' = None,
            err_callback: 'Callable | None' = None,
            target_args: 'tuple|list' = tuple(),
            target_kwargs: 'dict|None' = None,
            **kwargs
    ):
        if not callback:
            callback = callback or self.default_callback

        if not err_callback:
            err_callback = lambda: self.default_error_callback(target)

        return self._factory.add_target(
            target,
            error_callback=err_callback,
            callback=callback,
            target_args=target_args,
            target_kwargs=target_kwargs or {},
            **kwargs
        )
