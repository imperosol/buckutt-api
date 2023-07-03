from django.core.management import call_command
from django.test.runner import DiscoverRunner


class BuckuttTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        res = super().setup_databases(**kwargs)
        call_command("loaddata", "fixtures.json")
        return res
