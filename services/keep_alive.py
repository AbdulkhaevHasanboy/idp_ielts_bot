"""
Keep-Alive Web Server and Self-Pinger for Render 24/7 Deployment.
Runs a lightweight HTTP server on $PORT and automatically pings https://idp-ielts-bot-3421.onrender.com/
every 5 minutes so Render free tier never sleeps.
"""
import os
import asyncio
import logging
import aiohttp
from aiohttp import web

logger = logging.getLogger(__name__)

# Target Render URL to ping every 5 minutes
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", "https://idp-ielts-bot-3421.onrender.com/")
PING_INTERVAL_SECONDS = 300  # 5 minutes

async def handle_root(request):
    """Health check endpoint responding 200 OK to Render and monitoring services."""
    return web.json_response({
        "status": "healthy",
        "bot": "IDP IELTS Uzbekistan AI Telegram Bot",
        "service": "24/7 Active",
        "timestamp": asyncio.get_event_loop().time()
    })

async def ping_render_loop():
    """Background task that sends an HTTP GET request every 5 minutes to keep Render alive."""
    await asyncio.sleep(10)  # Wait 10s after startup before first ping
    logger.info(f"Keep-Alive loop started. Pinging {RENDER_URL} every {PING_INTERVAL_SECONDS} seconds.")
    
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(RENDER_URL, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        logger.info(f"✅ Keep-Alive ping to {RENDER_URL} successful (Status 200).")
                    else:
                        logger.warning(f"⚠️ Keep-Alive ping received status {resp.status}.")
        except Exception as e:
            logger.debug(f"Keep-Alive ping attempt notice: {e}")
            
        await asyncio.sleep(PING_INTERVAL_SECONDS)

async def start_keep_alive_server():
    """Starts the aiohttp web server on PORT and launches the ping background task."""
    port = int(os.getenv("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/health", handle_root)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"🌐 Keep-Alive HTTP health check server running on 0.0.0.0:{port}")
    
    # Launch background self-pinger
    asyncio.create_task(ping_render_loop())
