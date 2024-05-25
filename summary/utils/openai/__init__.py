from __future__ import annotations

from muffin_apiclient import Plugin


class OpenAI(Plugin):
    name = "openai"
    root_url = "https://api.openai.com/v1"

    def setup(self, app, **options):
        super().setup(app, **options)

        @self.client.middleware
        async def authorize(method, url, options):
            options["headers"] = options.get("headers", {})
            options["headers"]["Authorization"] = f"Bearer {app.cfg.OPENAI_API_KEY}"
            return method, url, options
