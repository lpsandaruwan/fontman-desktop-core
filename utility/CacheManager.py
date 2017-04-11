""" Cache Manager

This module covers initializing system, install update fonts, database
manipulation like operations.

Created by Lahiru Pathirage @ Mooniak <lpsandaruwan@gmail.com> on 2/12/2016
"""

from consumer import FontIndexConsumer
from service import FontFaceService
from service import FontService
from service import InstalledFontService
from service import LanguageService
from service import MetadataService


class CacheManager:

    def __init__(self):
        self.__font_index = FontIndexConsumer().load_font_index()

    def add_new_font(self, __font):
        FontService().add_new(
            __font["font_id"],
            __font["name"]
        )

        MetadataService().add_new(
            __font["font_id"],
            __font["default_fontface"],
            __font["download_url"],
            __font["license"],
            __font["version"]
        )

        for key, value in __font["fontfaces"].items():
            FontFaceService().add_new(
                __font["font_id"],
                key,
                value
            )

        for __language in __font["languages"]:
            LanguageService().add_new(
                __font["font_id"],
                __language
            )

    def update_font_cache(self):
        print(self.__font_index)
        for __font in self.__font_index:
            if FontService().is_exists_by_font_id(__font["font_id"]):
                MetadataService().update_by_font_id(
                    __font["font_id"],
                    {
                        "download_url": __font["download_url"],
                        "version": __font["version"]
                    }
                )

                installed_font = InstalledFontService().find_by_font_id(
                    __font["font_id"]
                ).first()

                if installed_font is not None:
                    if installed_font.version != __font["version"]:
                        FontService().update_by_font_id(
                            __font["font_id"],
                            {
                                "is_upgradable": True
                            }
                        )
                continue

            self.add_new_font(__font)
