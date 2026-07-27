import logging
logger = logging.getLogger(__name__)

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        logger.info("=" * 60)
        logger.info(f"📝 {request.method} {request.path}")
        logger.info(f"📝 Headers: {dict(request.headers)}")
        logger.info(f"📝 GET: {dict(request.GET)}")
        logger.info(f"📝 POST: {dict(request.POST)}")
        logger.info(f"📝 COOKIES: {request.COOKIES}")
        logger.info("=" * 60)
        
        try:
            response = self.get_response(request)
            logger.info(f"✅ Response: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"❌ Erreur: {str(e)}", exc_info=True)
            raise