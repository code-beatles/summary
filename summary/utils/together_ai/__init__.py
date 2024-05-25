from __future__ import annotations

from muffin_apiclient import Plugin


class TogetherAI(Plugin):
    name = "together_ai"
    root_url = "https://api.together.xyz/v1"

    def setup(self, app, **options):
        super().setup(app, **options)

        @self.client.middleware
        async def authorize(method, url, options):
            options["headers"] = options.get("headers", {})
            options["headers"][
                "Authorization"
            ] = f"Bearer {app.cfg.TOGETHER_AI_API_KEY}"
            return method, url, options
