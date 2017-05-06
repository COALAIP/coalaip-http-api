"""Transformations going on between COALA IP and OMI data models"""

mappings = {
        'Recording->CreativeWork': {
            'title': 'name',
            '@delete': ['X-OMI-PUBLIC-KEY', 'X-OMI-PRIVATE-KEY']
        },
        'CreativeWork->Recording': {
            'name': 'title',
            '@delete': ['@type', '@context', '@id']
        },
        'Composition->AbstractWork': {
            'title': 'name',
            '@delete': ['X-OMI-PUBLIC-KEY', 'X-OMI-PRIVATE-KEY']
        },
        'AbstractWork->Composition': {
            'name': 'title',
            '@delete': ['@type', '@context', '@id']
        },
}

def transform(model, direction):
    new_model = {}
    mapping = mappings[direction]
    to_delete = mapping.get('@delete', [])

    for k, v in model.items():
        try:
            replacement = mapping[k]
        except KeyError:
            if k not in to_delete:
                new_model[k] = v
        else:
            new_model[replacement] = v

    return new_model
