import multiprocessing as mp
from multiprocessing.pool import Pool, ApplyResult
from typing import Callable


class PoolFactory:
    max_processes: int
    _pool: Pool = None

    def __init__(self, max_processes=5):
        self.max_processes = max_processes

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.join()
        return self.pool.close()

    def __enter__(self):
        return self

    def close(self):
        return self.pool.close()

    @property
    def pool(self):
        if not self._pool:
            self._pool = mp.Pool(processes=self.max_processes)
        return self._pool

    def add_target(
            self,
            target: Callable,
            target_args: list = tuple(),
            target_kwargs: "dict|None" = None,
            **kwargs) -> Callable[['float|None'], ApplyResult]:
        pool = self.pool
        async_result = pool.apply_async(
            func=target,
            args=target_args,
            kwds=target_kwargs or {},
            callback=kwargs.get('callback'),
            error_callback=kwargs.get('error_callback')
        )
        return lambda timeout=None: async_result.get(timeout=timeout)

