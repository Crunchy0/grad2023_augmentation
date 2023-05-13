def apply_transform(source_list, transform):
    if not callable(transform):
        return source_list
    modified_list = []
    for samples, sr in source_list:
        modified_list.append((transform(samples, sr), sr))
    return modified_list
