
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
    jekyll/jekyll
open http://0.0.0.0:4000
```

