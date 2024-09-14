import importlib


def create_class_from_config(
    class_config,
    module_key_name: str = "module",
    class_key_name: str = "class",
    kwargs_key_name: str = "kwargs",
):
    """
    Creates a class instance from the given config.
    The config is a dictionary with the following keys:
    - module: the module name where the class is defined
    - class: the class name
    - kwargs: a dictionary with the arguments to pass to the class constructor
    This function supports arguments that are classes. In this case, the argument value is a dictionary
    with the same structure as the config dictionary.
    This function is  recursive, so it can create classes with arguments that are classes.
    """

    # dynamic import of the class to create and create an instance
    _class_to_create = getattr(
        importlib.import_module(class_config[module_key_name]),
        class_config[class_key_name],
    )

    _kwargs = class_config.get(kwargs_key_name, {})

    for _key, _value in _kwargs.items():
        # recursively create the class instances for the arguments that are classes
        # the arguments that are classes are defined in the config as a dictionary
        # with the same structure as the config dictionary
        # and that the dictionary has the keys 'module' and 'class'
        if (
            isinstance(_value, dict)
            and module_key_name in _value
            and class_key_name in _value
        ):
            _kwargs[_key] = create_class_from_config(_value)

    # create the class instance with the kwargs (including the arguments that are classes)
    return _class_to_create(**_kwargs)
