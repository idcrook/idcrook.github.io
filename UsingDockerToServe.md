
## What?

Serve the content on this blog using a docker container that understand
github-pages flavor of jekyll.


### How?

[Docker jekyll](https://github.com/jekyll/docker-jekyll) at github.

Run on OS X

```bash
eval "$(docker-machine env default)"
docker run --rm --label=jekyll --label=pages --volume=$(pwd):/srv/jekyll   -t -p 4000:4000 jekyll/pages jekyll serve
```
