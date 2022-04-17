class FipsSettings:
    """Object for storing FIPS settings provided in JSON file
    """

    def __init__(self, test_settings_json: dict):
        """Initialize FipsSettings class

        Args:
            test_settings_json (dict): Parsed test config JSON file

        Raises:
            RuntimeError: Throws when some invalid or incomplete settings were found
        """
        settings = test_settings_json.get("fips-settings")
        if not settings:
            raise RuntimeError(
                "Configuration 'fips-settings' was not specified")
        try:
            self.bytes_count = int(settings["defaults"]["bytes-count"])
        except:
            raise RuntimeError("FIPS settings contain invalid values")
