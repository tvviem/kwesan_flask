from flask_assets import Bundle

# Using for flask-assets extension
bundles = {
    # "home_js": Bundle("js/lib/jquery-1.10.2.js", "js/home.js", output="gen/home.js"),
    "home_css": Bundle(
        "sass/bulma.sass",
        filters="sass",
        output="gen/home.%(version)s.css",
    )
    # "admin_js": Bundle(
    #     "js/lib/jquery-1.10.2.js", "js/lib/Chart.js", "js/admin.js", output="gen/admin.js"
    # ),
    # "admin_css": Bundle(
    #     "css/lib/reset.css", "css/common.css", "css/admin.css", output="gen/admin.css"
    # ),
}

# assets = Environment(app)
# assets.debug = True
# assets.register(bundles)

# use them inside *.html which is template jinja2
#  {% assets "home_css" %}
#   <link rel="stylesheet" type="text/css" href="{{ ASSET_URL }}">
#   {% endassets %}
#   {% assets "home_js" %}
#   <script type="text/javascript" src="{{ ASSET_URL }}"></script>
#   {% endassets %}