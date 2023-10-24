# In this script we build the decorator and the function we want to transform into an API

def fast_api_decorator(func):
    def example(*param, **param2):
        print("Action avant")
        func(*param, **param2)
        print("Action après")

    return example


@fast_api_decorator
def function_to_transform(x, a):
    return x**a
