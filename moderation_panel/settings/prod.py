DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'goibibo_inventory',  # Or path to database file if using sqlite3.
        'USER': 'inventory',  # Not used with sqlite3.
        'PASSWORD': 'g0!b!b0in',  # Not used with sqlite3.
        'HOST': 'ingoibibo.mysql.master.goibibo.com',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
        # 'ATOMIC_REQUESTS':True,
        'CONN_MAX_AGE': 200,
    }
}
MONGODB_DATABASES = {
    "default": {
        "name": 'moderation_panel',  # TODO Change DB name
        "host": ['ingoibibomongo01.prod.goibibo.com', 'ingoibibomongo02.prod.goibibo.com'],
        "password": '',
        "username": '',
        "tz_aware": True,  # if you using timezones in django (USE_TZ = True)
        "retryWrites": True
    }
}
MODERATION_PANEL_KAFKA_SERVER_CONF = {
    'servers': {
        'moderation_panel_input': {
            'HOST': ['kafka04.prod.goibibo.com:9092'],
            'TOPIC': 'ingo_moderation_panel_input',
            'GROUP': 'ingo_moderation_panel'
        },
        'moderation_panel_output': {
            'HOST': ['kafka04.prod.goibibo.com:9092'],
            'TOPIC': 'ingo_moderation_panel_output',
            'GROUP': 'ingo_moderation_panel'
        }
    }
}
