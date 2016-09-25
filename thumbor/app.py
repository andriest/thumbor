#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com
import tornado.web
import tornado.ioloop

from thumbor.handlers.blacklist import BlacklistHandler
from thumbor.handlers.healthcheck import HealthcheckHandler
from thumbor.handlers.upload import ImageUploadHandler, ImagePublicUploadHandler
from thumbor.handlers.image_resource import ImageResourceHandler, ImagePublicResourceHandler
from thumbor.handlers.imaging import ImagingHandler, ImagingPublicHandler
from thumbor.url import Url


class ThumborServiceApp(tornado.web.Application):

    def __init__(self, context):
        self.context = context
        super(ThumborServiceApp, self).__init__(self.get_handlers())

    def get_handlers(self):
        handlers = [
            (r'/healthcheck', HealthcheckHandler),
        ]

        if self.context.config.UPLOAD_ENABLED:
            # Handler to upload images (POST).
            handlers.append(
                (r'/image', ImageUploadHandler, {'context': self.context})
            )

            # Handler to retrieve or modify existing images  (GET, PUT, DELETE)
            handlers.append(
                (r'/image/(.*)', ImageResourceHandler, {'context': self.context})
            )

            handlers.append(
                (r'/public', ImagePublicUploadHandler, {'context': self.context})
            )

            handlers.append(
                (r'/public/(.*)', ImagePublicResourceHandler, {'context': self.context})
            )

        if self.context.config.USE_BLACKLIST:
            handlers.append(
                (r'/blacklist', BlacklistHandler, {'context': self.context})
            )

        # Imaging handler (GET)
        handlers.append(
            (Url.regex(), ImagingHandler, {'context': self.context})
        )

        handlers.append(
            (Url.regex(), ImagingPublicHandler, {'context': self.context})
        )

        return handlers
