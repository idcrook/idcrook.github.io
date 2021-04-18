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

gem "github-pages", group: :jekyll_plugins
# following is a workaround for
#     jekyll 3.8.5 | Error:  uninitialized constant Faraday::Error::ClientError
#     Did you mean?  Faraday::ClientError

# gem 'faraday', '0.17.3'
```

If `jekyll build` below has the following error, it's likely because you did not create your `Gemfile`

    jekyll 3.8.6 | Error:  The jekyll-theme-primer theme could not be found.


## Commands

- assumes docker is installed and runnable by non-root user
- assumes you created a `Gemfile` (see above)
- assumes git clone at specified path

```bash
cd ~/projects/webdev/idcrook.github.io

# build docker container, caching gems to local directory
export JEKYLL_VERSION=3.8
docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it jekyll/jekyll:$JEKYLL_VERSION \
  jekyll build

# ... Bundled gems are installed into `/usr/local/bundle` in container

# run as server (rebuilds after changes)
export JEKYLL_VERSION=3.8
docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it  -p 4000:4000 \
  jekyll/jekyll:$JEKYLL_VERSION \
  jekyll serve --force_polling


```

now can open http://0.0.0.0:4000 to see the generated site.


#### Docker in macOS on Apple Silicon

**NOTE**: 2021-Apr-18 **::** Using `docker` from _Docker Desktop for Apple Silicon_ will display a warning like below about `jekyll` image architecture. It runs fine, albeit mucher slower than native, in emulation.

> Status: Downloaded newer image for jekyll/jekyll:3.8

> WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested


See [Docker Desktop for Apple silicon | Docker Documentation](https://docs.docker.com/docker-for-mac/apple-silicon/) page, which mentions its `--platform linux/amd64` option to run an Intel image under emulation.
