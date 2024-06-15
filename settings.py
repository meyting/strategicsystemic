from os import environ

SESSION_CONFIGS = [
    dict(   
        name="stage2_minimal",
        display_name="stage2 (minimal)",
        num_demo_participants=20,
        app_sequence=["stage2_welcome",
                       "stage2_evaluations",
                       "stage2_survey",
                       "stage2_end",
                       ],
        framing="minimal"
        )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ROOMS = [
    dict(
        name='pilot',
        display_name='pilot',
        # participant_label_file='_rooms/your_study.txt',
        # use_secure_urls=True,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['profiles', 'treatment', 'control_answers', 'group',
                      #'order_beliefs'
                      ]
                    
SESSION_FIELDS = ['params']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'meyting_strategicsystemic'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'strategicsystemic'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5499396074809'
