from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """
    
    id_param = args.get('id')
    name_param = args.get('name', '').lower()
    age_param = args.get('age')
    occupation_param = args.get('occupation', '').lower()

    results = []

    # Filter by ID with highest priority
    if id_param:
        for user in USERS:
            if user['id'] == id_param:
                results.append((user, 1))

    # Filter by Name with second priority
    if name_param:
        for user in USERS:
            if name_param in user['name'].lower():
                results.append((user, 2))

    # Filter by Age with third priority
    if age_param:
        try:
            age = int(age_param)
            for user in USERS:
                if age - 1 <= user['age'] <= age + 1:
                    results.append((user, 3))
        except ValueError:
            pass  # Invalid age parameter, skip age filtering

    # Filter by Occupation with fourth priority
    if occupation_param:
        for user in USERS:
            if occupation_param in user['occupation'].lower():
                results.append((user, 4))

    # Remove duplicates while preserving order and sorting by priority
    seen = set()
    final_results = []
    for user, priority in sorted(results, key=lambda x: x[1]):
        user_tuple = tuple(user.items())
        if user_tuple not in seen:
            seen.add(user_tuple)
            final_results.append(user)

    # If no filters are provided, return all users sorted by id
    if not any([id_param, name_param, age_param, occupation_param]):
        return sorted(USERS, key=lambda x: x['id'])

    return final_results
