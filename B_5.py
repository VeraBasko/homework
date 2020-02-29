import time
class Timing:
    def __init__(self, func):
        self.num_runs = 10
        self.func = func

    def __call__(self, *args, **kwargs):
        avg = 0
        function_name = self.func.__name__
        for _ in range(self.num_runs):
            t0 = time.time()
            self.func(*args, **kwargs)
            t1 = time.time()
            avg += (t1 - t0)
        avg /= self.num_runs
        print(f'Среднее время выполнения {function_name} для {self.num_runs} запусков составило {avg} секунд')
        return self.func(*args, **kwargs)

@Timing
def fib(N):
    a = 1
    b = 2
    for i in range(1, N):
        res = a + b
        a = b
        b = res
    return res

if __name__ == '__main__':
    fib(60000)