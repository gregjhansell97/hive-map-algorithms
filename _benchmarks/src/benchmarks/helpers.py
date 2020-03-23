import inspect


def monitor(obj, attributes):
    """
    Given class and description of what is to be monitered return instance 
    wrapped with monitoring hooks
    """
    for attr, props in attributes.items():
        f = getattr(obj, attr)

        def function_wrapper(*args, **kwargs):
            stats = ", ".join([f"({p}: {getattr(obj, p)})" for p in props])
            try:
                r = f(*args, **kwargs)
            except Exception as e:
                print(e)
                raise e
            print(stats)
            return r

        async def coroutine_function_wrapper(*args, **kwargs):
            stats = ", ".join([f"({p}: {getattr(obj, p)})" for p in props])
            try:
                r = f(*args, **kwargs)
            except Exception as e:
                print(e)
                raise e
            print(f"{attr}: {stats}")
            return r
        if inspect.iscoroutinefunction(f):
            setattr(obj, attr, coroutine_function_wrapper)
        else:
            setattr(obj, attr, function_wrapper)
    return obj


