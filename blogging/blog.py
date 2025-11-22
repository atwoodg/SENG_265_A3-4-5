class Blog:
    """
    Blog domain class for Assignment 4
    (posts are stored externally via PostDAO).
    """

    def __init__(self, id, name, url, email):
        self.id = id
        self.name = name
        self.url = url
        self.email = email

    def __str__(self):
        return f"Blog ID: {self.id}\nName: {self.name}\nURL: {self.url}\nEmail: {self.email}"

    def __eq__(self, other):
        if not isinstance(other, Blog):
            return False
        return (
            self.id == other.id and
            self.name == other.name and
            self.url == other.url and
            self.email == other.email
        )
