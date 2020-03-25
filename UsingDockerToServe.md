What?
-----

Serve the content on this blog using a docker container.

How?
----

-	Docker images, and CI builders for Jekyll. [envygeeks/jekyll-docker](https://github.com/envygeeks/jekyll-docker)

### Changing to supported theme

create in `Gemfile`, use

```
source 'https://rubygems.org'

gem "github-pages", group: :jekyll_plugins
# following is a workaround for
#     jekyll 3.8.5 | Error:  uninitialized constant Faraday::Error::ClientError
#     Did you mean?  Faraday::ClientError

gem 'faraday', '0.17.3'
```

And in `_config.yml`

```yaml
# custom CSS overrides theme
theme: jekyll-theme-primer
```


### Commands

```bash
cd ~/projects/idcrook.github.io

# build docker container, caching gems to local directory
export JEKYLL_VERSION=3.8
sudo docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it jekyll/jekyll:$JEKYLL_VERSION \
  jekyll build

# ... Bundled gems are installed into `/usr/local/bundle`

# run as server (rebuilds after changes)
sudo docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it  -p 4000:4000 \
  jekyll/jekyll:$JEKYLL_VERSION \
  jekyll serve --force_polling


open http://0.0.0.0:4000
```
