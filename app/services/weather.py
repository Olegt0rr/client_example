import asyncio
import ssl
from typing import Optional

from aiohttp import ClientSession, TCPConnector


class HTTPMethod:
    POST = "post"
    GET = "get"


class WeatherClient:
    """Represents weather service client."""

    host = "https://api.weather.com"

    def __init__(self):
        self._session: Optional[ClientSession] = None

    async def _get_session(self) -> ClientSession:
        """Get session with cache."""
        if self._session and not self._session.closed:
            return self._session

        connector = TCPConnector(ssl_context=ssl.SSLContext())
        self._session = ClientSession(base_url=self.host, connector=connector)

        return self._session

    async def _request(self, method: str, path: str):
        """Make request."""
        session = await self._get_session()
        async with session.request(method, path) as response:
            return await response.json()

    async def get_current_weather(self):
        return await self._request(HTTPMethod.GET, "/")

    async def close(self):
        """Close the client (and the session) gracefully."""
        if self._session is None:
            return

        if self._session.closed:
            return

        await self._session.close()
        await asyncio.sleep(0.2)


if __name__ == "__main__":

    async def main():
        client = WeatherClient()
        current_weather = await client.get_current_weather()
        print(current_weather)
        await client.close()

    asyncio.run(main())
