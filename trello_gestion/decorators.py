from functools import wraps


def debug_verbose(keep_verbose_kwargs=True, output_function=lambda x: x):

    def _debug_verbose(f):
        @wraps(f)
        def _wrapped(*args, **kwargs):

            if keep_verbose_kwargs:
                verbose = kwargs.get("verbose", False)
            
            else:
                verbose = kwargs.pop("verbose", False)

            if verbose:
                print("CALL {}(*{}, **{})".format(f.__name__, args, kwargs))

            r = f(*args, **kwargs)

            if verbose:
                print("RESULT[{}] {}".format(f.__name__, output_function(r)))

            return r
        
        return _wrapped
    return _debug_verbose
