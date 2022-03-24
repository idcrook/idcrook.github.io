What?
-----

Build and Serve this blog locally using a docker container.

How?
----

-	Docker images, and CI builders for Jekyll. [envygeeks/jekyll-docker](https://github.com/envygeeks/jekyll-docker)

### Using a supported theme

In `_config.yml`

```yaml
# custom CSS overrides theme
theme: jekyll-theme-primer
```

### `Gemfile` to support github-pages and theme

Create `Gemfile` (not committed to git clone)

```ruby
source 'https://rubygems.org'

# GH pages dependency (3.9.0)
#  BTW, using "3.9.1" here -> build dependency error, 3.9.0 does not
gem "jekyll", "~> 3.9"

# https://github.com/github/pages-gem
gem "github-pages", group: :jekyll_plugins
```

If `jekyll build` below has something like the following error, it's likely because you did not create your `Gemfile`

```
jekyll 3.8.6 | Error:  The jekyll-theme-primer theme could not be found.
```

There's still not a 3.9 image available, but using the jekyll-3.8 Docker image updated to 3.9 using Gemfile seems to work fine.

Commands
--------

-	assumes docker is installed and runnable by non-root user
-	assumes you created a `Gemfile` (see above)
-	assumes git clone at specified path

```bash
cd ~/projects/webdev/idcrook.github.io

# build docker container, caching gems to local directory
export JEKYLL_VERSION=3.8
docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it jekyll/jekyll:$JEKYLL_VERSION \
  jekyll build
```

Bundled gems are installed into `/usr/local/bundle` in container

```
# run as server (rebuilds after changes)
export JEKYLL_VERSION=3.8
docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it \
  -p 4000:4000 \
  -p 35729:35729 \
  jekyll/jekyll:$JEKYLL_VERSION \
  jekyll serve --incremental --force_polling --livereload
```

Now can open http://0.0.0.0:4000 to see the generated site.

Diagnostics
-----------

-	`bundle exec github-pages versions`

as in

```
# run as server (rebuilds after changes)
export JEKYLL_VERSION=3.8
docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it  -p 4000:4000 \
  jekyll/jekyll:$JEKYLL_VERSION \
bundle exec github-pages versions
```

See also: https://pages.github.com/versions/

-	`github-pages health-check`

https://github.com/github/pages-health-check
