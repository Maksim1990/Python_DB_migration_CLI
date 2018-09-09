class Config:

    def __getattr__(self, item):
        if item == "config_origin":
            config_origin={
                'hostname':'localhost',
                'username':'username',
                'password':'pass',
                'database':'python_origin'
            }
            config=config_origin
        elif item == "config_destination":
            config_destination={
                'hostname':'localhost',
                'username':'username',
                'password':'pass',
                'database':'python_destination'
            }
            config=config_destination
        elif item == "linked_tables":
            # Tables to be linked when migration is performed
            linked_tables=(
                "customers",
                "posts",
                "users"
            )
            config=linked_tables

        return config
