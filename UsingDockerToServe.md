What?
-----

Serve the content on this blog using a docker container that understand github-pages flavor of jekyll.

### How?

[Docker jekyll](https://github.com/jekyll/docker-jekyll) at github.

Run on OS X

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

# server (rebuilds after changes)
sudo docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it  -p 4000:4000 \
  jekyll/jekyll:$JEKYLL_VERSION \
  jekyll serve --force_polling


open http://0.0.0.0:4000
```

### Changing to supported theme

-	assumes `rbenv` already installed/configured

in `Gemfile`, use

```
gem "github-pages", group: :jekyll_plugins
```

then can install dependencies (via `rbenv`\)

```shell
gem install bundler
bundle install
jekyll serve
```

And in `_config.yml`

```yaml
# custom CSS overrides theme
theme: jekyll-theme-primer
```
