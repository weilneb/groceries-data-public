const CONFIG = {
    'development': {
        'REST_BASE_URL': 'https://wzoujjhpbc.execute-api.ap-southeast-2.amazonaws.com/dev'
    },
    'production': {
        'REST_BASE_URL': 'https://wzoujjhpbc.execute-api.ap-southeast-2.amazonaws.com/prod'
    },
}

export default function getRestApiBaseUrl() {
    const env = process.env.NODE_ENV
    return CONFIG[env]['REST_BASE_URL']
}