def variables_dict_to_options(variables):
    values = [f'"{key}={value}"' for key, value in variables.items()]
    flags = ["-var"] * len(values)
    return " ".join([arg for tup in zip(flags, values) for arg in tup])


def variables_dict_to_tfvars(variables, path="terraform.tfvars"):
    with open(path, "w") as f:
        for key, value in variables.items():
            # TODO: will need to extend this logic for other types
            if isinstance(value, str):
                f.write(f'{key}="{value}"\n')
