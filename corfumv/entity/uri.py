from typing import Optional, NamedTuple


class URI(NamedTuple):
    drivername: Optional[str]
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]
    options: Optional[dict]


    @classmethod
    def create(cls,
               drivername: Optional[str] = 'mongodb',
               username: Optional[str] = None,
               password: Optional[str] = None,
               host: Optional[str] = None,
               port: Optional[int] = 27017,
               options: Optional[dict] = None
              ):
        return cls(
            drivername,
            username,
            password,
            host,
            port,
            options
        )


    def _options_to_string(self):
        options_string = ''
        for el in self.options.items():
            options_string += f"&{el[0]}={el[1]}"
        return options_string[1:]


    def to_string(self):
        uri_string = ''
        if self.drivername:
            uri_string += f"{self.drivername}://"
        if (self.username and self.password):
            uri_string += f"{self.username}:{self.password}@"
        if self.host:
            uri_string += f"{self.host}"
        if self.port:
            uri_string += f":{self.port}"
        if self.options:
            uri_string += self._options_to_string()
        return uri_string
