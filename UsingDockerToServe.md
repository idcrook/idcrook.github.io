What?
-----

Build and Serve this blog locally using a docker container.

How?
----

-	Docker images, and CI builders for Jekyll. [envygeeks/jekyll-docker](https://github.com/envygeeks/jekyll-docker)

Consult also [Setting up a GitHub Pages site with Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)

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

# https://pages.github.com/versions/ - gem "jekyll", "~> 3.10.0"
#  BTW, using "3.9.1" here -> build dependency error, 3.9.0 does not
gem "jekyll", "~> 3.9"

# fix for ffi-1.17.1-x86_64-linux-musl requires rubygems version >= 3.3.22, which is incompatible with the current version, 3.0.6
# https://github.com/ffi/ffi/issues/1103#issuecomment-2617122261
gem "ffi", "< 1.17.0"

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

### build docker container, caching gems to local directory

```shell
cd ~/projects/webdev/idcrook.github.io

export JEKYLL_VERSION=3.8

docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it jekyll/jekyll:$JEKYLL_VERSION \
  bundle install

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
  jekyll serve --force_polling --livereload
```

Now can open http://0.0.0.0:4000 to see the generated site.

An explicit IP address for URL may be needed instead of `0.0.0.0`, in the case of running in WSL2 Docker on Windows, for example. The following command pipeline will output an URL for `eth0` device in Ubuntu (tested on *WSL2*).

```
echo http://$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1):4000
```

The `--incremental` option to the `jekyll serve` command can be tried to speedup successive site/page generation, but in my experience, it does not properly handle top-level site changes (adding or subtracting or renaming posts, for example)

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
