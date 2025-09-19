# ryland-blog-template
a template for a blog built using Ryland


Install `requirements.txt` in a virtualenv and run `./build.py`.

The workflow in `.github` will also build on push.

To locally serve up your site, run `(cd output; python -m http.server)`.


## Customization

You **will definitely** need to change:
 - `pages`
 - `posts`
 - `site_data.yaml`
 - `templates/_sidebar.html` (until I factor out the content)

You **will probably** need to change:
 - `pantry/styles.css`

You **may** need to change:
 - some of the `templates/`

You **probably don't** need to change:
 - `build.py` (although let me know if you do!)


## url-root

By default, it is assumed your site is served up at the root `/`. If it is under a different path (as is the case with default GitHub Pages not using a custom domain), you will need to pass `--url-root` to `build.py`.

For example, for `https://jtauber.github.io/ryland-blog-template/` to work, the build was done (automatically by the workflow) with `python build.py --url-root "/ryland-blog-template/"`.

Note: if you don't want to have to `cd output` to locally serve up your site, `python build.py --url-root "/output/"` would work.
