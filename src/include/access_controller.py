def approve_access(role, action):
    access_control_matrix = {
        'Admin': {
            'upload': True,
            'search': True,
            'admin': True
        },
        'DEV': {
            'upload': True,
            'search': True,
            'admin': False
        },
        'QA': {
            'upload': False,
            'search': False,
            'admin': False
        },
        'User': {
            'upload': False,
            'search': False,
            'admin': False
        }
    }

    return access_control_matrix[role][action]
