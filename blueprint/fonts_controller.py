""" Fonts controller

Provides fonts REST API for Fontman client GUI

Created by Lahiru Pathirage @ Mooniak <lpsandaruwan@gmail.com> on 6/1/2017
"""

from service import FontFaceService
from service import FontService
from service import InstalledFontService
from service import LanguageService
from service import MetadataService
from utility import FontManager

from flask import Blueprint, jsonify, request

fonts_blueprint = Blueprint("fonts_blueprint", __name__)


@fonts_blueprint.route("/fonts")
def find_all_fonts():
    display_texts = [
        "Nymphs blitz quick vex dwarf jog.",
        "DJs flock by when MTV ax quiz prog.",
        "Big fjords vex quick waltz nymph.",
        "Junk MTV quiz graced by fox whelps.",
        "Vamp fox held quartz duck just by wing."
    ]
    response_data = []
    fonts = FontService().find_all()

    for font in fonts:
        metadata = MetadataService().find_by_font_id(font.font_id).first()
        fontfaces = FontFaceService().find_by_font_id(font.font_id)
        languages = LanguageService().find_by_font_id(font.font_id)

        fontfaces_list = []
        languages_list = []

        print(fontfaces.first())

        for fontface in fontfaces:
            fontfaces_list.append(
                {
                    "fontface": fontface.fontface,
                    "resource_path": fontface.resource_path
                }
            )

        for language in languages:
            languages_list.append(language.language)

        response_data.append(
            {
                "fontId": font.font_id,
                "defaultFontface": metadata.default_fontface,
                "displayText": display_texts[font.font_id // 5],
                "fontfaces": fontfaces_list,
                "isInstalled": font.is_installed,
                "isUpgradable": font.is_upgradable,
                "license": metadata.license,
                "name": font.name,
                "textSize": 25,
                "version": metadata.version,
                "viewId": {"id": 2}
            }
        )

    return jsonify(response_data)


@fonts_blueprint.route("/fonts/<font_id>/install")
def install_font_by_font_id(font_id):
    response = FontManager().install_font(font_id)
    return jsonify(response)


@fonts_blueprint.route("/fonts/<font_id>/remove")
def remove_font_by_font_id(font_id):
    FontManager().remove_font(font_id)

    return jsonify(True)


@fonts_blueprint.route("/fonts/<font_id>/update/installed")
def update_installed_font(font_id):
    FontManager().update_font(font_id)

    return jsonify(True)


@fonts_blueprint.route("/fonts/<font_id>/update", methods=["POST"])
def update_font_by_font_id(font_id):
    json_data = request.json
    FontService().update_by_font_id(font_id, json_data)

    return jsonify(True)


@fonts_blueprint.route("/fonts/")
def find_by_query():
    try:
        if request.args.get("upgradable"):
            upgradable_fonts = FontService().find_all_upgradable()
            response_data = []

            if upgradable_fonts.first() is None:
                return jsonify(False)

            for font in upgradable_fonts:
                fontfaces = FontFaceService().find_by_font_id(font.font_id)
                languages = LanguageService().find_by_font_id(font.font_id)
                metadata = MetadataService().find_by_font_id(font.font_id).first()

                default_resource = ""
                languages_list = []

                for fontface in fontfaces:
                    if "Regular" in fontface.fontface:
                        default_resource = fontface.resource_path

                for language in languages:
                    languages_list.append(language.language)

                response_data.append(
                    {
                        "fontId": font.font_id,
                        "defaultFontface": font.name + "-" + metadata.default_fontface,
                        "defaultResource": default_resource,
                        "installedVersion": InstalledFontService().find_by_font_id(font.font_id).first().version,
                        "latestVersion": metadata.version,
                        "name": font.name
                    }
                )

            return jsonify(response_data)

    except:
        return jsonify({"error": "Invalid request"})


@fonts_blueprint.route("/fonts/update", methods=["POST"])
def update_all_fonts():
    json_data = request.json
    FontService().update_all(json_data)

    return jsonify(json_data)
