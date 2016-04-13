
## What?

Serve the content on this blog using a docker container that understand
github-pages flavor of jekyll.


### How?

[Docker jekyll](https://github.com/jekyll/docker-jekyll) at github.

Run on OS X

```bash
cd ~/projects/webdev/dpcrook.github.io
eval "$(docker-machine env default)"
#docker run -i --rm --label=jekyll --label=pages \
# --volume=$(pwd):/srv/jekyll  \
# -t -p 4000:4000 jekyll/jekyll:pages jekyll serve
docker run --rm --label=jekyll --volume=$(pwd):/srv/jekyll \
  -it -p $(docker-machine ip `docker-machine active`):4000:4000 \
    jekyll/jekyll
open http://`docker-machine ip default`:4000
```
