def approve_access(role, action):
    access_control_matrix = {
        'Admin': {
            'upload': True,
            'search': True,
            'admin': True,
            'criteria': True,
            'criteria_modification': True,
            'view': True,
            'update_evidence': True,
            'delete_evidence': True
        },
        'DEV': {
            'upload': True,
            'search': True,
            'criteria': True,
            'view': True,
            'update_evidence': True,
            'delete_evidence': True
        },
        'QA': {
            'search': True,
            'criteria': True,
            'view': True
        },
        'User': {
        }
    }

    return access_control_matrix[role][action] if action in access_control_matrix[role] else False
