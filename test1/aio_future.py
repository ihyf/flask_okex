import asyncio


async def slow_operation(future):
    await asyncio.sleep(5)
    future.set_result('Future is dong!')


async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y


async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))


async def print_1():
    print(1)


def got_result(future):
    f = future.result()
    print(f)
    loop.stop()


loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
future.add_done_callback(got_result)
asyncio.ensure_future(print_1())
asyncio.ensure_future(print_sum(1, 2))
try:
    loop.run_forever()
finally:
    loop.close()

