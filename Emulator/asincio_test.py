# -*- coding: UTF-8 -*-
import asyncio

async def set_after(fut, delay, value):
    # Sleep for *delay* seconds.
    await asyncio.sleep(delay)
    # Set *value* as a result of *fut* Future.
    fut.set_result(value)

#async def fut_self():
#    return "...world"

async def main():
    # Get the current event loop.
    loop = asyncio.get_running_loop() # Это, если запускать через asyncio.run(main()), тогда можно получить этим методом текущий цикл

    # Create a new Future object.
    fut = loop.create_future()

    # Run "set_after()" coroutine in a parallel Task.
    # We are using the low-level "loop.create_task()" API here because
    # we already have a reference to the event loop at hand.
    # Otherwise we could have just used "asyncio.create_task()".
    loop.create_task(
        set_after(fut, 1, '... world'))

    print('hello ...')

    # Wait until *fut* has a result (1 second) and print it.
    print(await fut)

async def some_async():
    fut = loop.create_future()


def main2():
    # Get the current event loop.
    loop = asyncio.get_event_loop() # Это, если запускать через asyncio.run(main()), тогда можно получить этим методом текущий цикл

    # Create a new Future object.
    fut = loop.create_future()

    # Run "set_after()" coroutine in a parallel Task.
    # We are using the low-level "loop.create_task()" API here because
    # we already have a reference to the event loop at hand.
    # Otherwise we could have just used "asyncio.create_task()".
    #loop.create_task(
    #    set_after(fut, 1, '... world'))

    fut.set_result("1232323")
    print('hello ...')
    l = loop.run_until_complete(fut)
    print(l)
    # Wait until *fut* has a result (1 second) and print it.
    #print(await fut)


main2()
#asyncio.run(main())