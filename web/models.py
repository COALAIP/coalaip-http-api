from web.utils import parse_model


user_model = parse_model(['publicKey', 'privateKey'])
public_user_model = parse_model(['publicKey'])
manifestation_model = parse_model(['name', 'datePublished', 'url'])
work_model = parse_model(['name', 'author'])
