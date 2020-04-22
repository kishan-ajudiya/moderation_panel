DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'goibibo_inventory',  # Or path to database file if using sqlite3.
        'USER': 'gouser',  # Not used with sqlite3.
        'PASSWORD': 'gi@G0u8eR',  # Not used with sqlite3.
        'HOST': 'pp.mysql.goibibo.dev',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {"autocommit": True}
    }
}
MONGODB_DATABASES = {
    "default": {
        "name": 'moderation_panel',  # TODO Change DB name
        "host": 'gocashmongo.pp.goibibo.dev:27017',
        "password": '',
        "username": '',
        "tz_aware": True,  # if you using timezones in django (USE_TZ = True)
        "retryWrites": False
    }
}
MODERATION_PANEL_KAFKA_SERVER_CONF = {
    'servers': {
        'moderation_panel_input': {
            'HOST': ['kafkapp01.goibibo.dev:9092'],
            'TOPIC': 'ingo_moderation_panel_input',
            'GROUP': 'ingo_moderation_panel'
        },
        'moderation_panel_output': {
            'HOST': ['kafkapp01.goibibo.dev:9092'],
            'TOPIC': 'ingo_moderation_panel_output',
            'GROUP': 'ingo_moderation_panel'
        }
    }
}