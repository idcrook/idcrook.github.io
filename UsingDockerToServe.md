
## What?

Serve the content on this blog using a docker container that understand
github-pages flavor of jekyll.


### How?

[Docker jekyll](https://github.com/jekyll/docker-jekyll) at github.

Run on OS X

```bash
cd ~/projects/webdev/idcrook.github.io
docker run --rm --label=jekyll --volume=$(pwd):/srv/jekyll \
  -it -p 4000:4000 \
    jekyll/jekyll jekyll s
open http://0.0.0.0:4000
```


### Changing to supported theme

 - assumes `rbenv` already installed/configured

in `Gemfile`, use

```
gem "github-pages", group: :jekyll_plugins
```

then can install dependencies (via `rbenv`)

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
