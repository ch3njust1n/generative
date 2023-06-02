import time
import textwrap
from pprint import pprint
from model import gpt, claude


def test_generated_class():
    def my_func(self):
        return self.x * 2

    MyClass = type("MyClass", (object,), {"x": 10, "my_func": my_func})
    instance = MyClass()
    assert instance.x == 10
    assert instance.my_func() == 20


def test_generated_stringified_class():
    properties = textwrap.dedent(
        """
    {
        'x': 10, 
        'my_func': 
            '''def my_func(self):
                return self.x * 2
            '''
    }
    """
    )
    properties = eval(properties)
    pprint(properties)
    global_vars = {}
    func_source = properties["my_func"]
    exec(func_source, global_vars)
    properties["my_func"] = global_vars["my_func"]

    MyClass = type("MyClass", (object,), properties)
    instance = MyClass()

    assert instance.x == 10
    assert instance.my_func() == 20


def test_generated_stringified_class_with_gpt():
    retry_count = 3
    retry_delay = 5

    for _ in range(retry_count):
        try:
            prompt = """
            You are a stochastic parrot that only repeats back JSON.
            Repeat the following JSON back to me:
            ```
            {
                'x': 10, 
                'my_func': 
                    '''def my_func(self):
                        return self.x * 2
                    '''
            }
            ```

            Do not explain.
            Do not add any additional information.
            Just repeat the JSON back to me exactly.
            """
            properties = textwrap.dedent(gpt(prompt))
            properties = eval(properties)
            global_vars = {}
            func_source = properties["my_func"]
            exec(func_source, global_vars)
            properties["my_func"] = global_vars["my_func"]

            MyClass = type("MyClass", (object,), properties)
            instance = MyClass()

            assert instance.x == 10
            assert instance.my_func() == 20
            break
        except Exception as e:
            print(f"Test error: {e}. Retrying after delay...")
            time.sleep(retry_delay)
