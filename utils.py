def dictify(user_fields):
    labels = ['id', 'id_number', 'name', 'last_name', 'password', 'birth_date', 'balance']
    return dict(zip(labels, user_fields))


