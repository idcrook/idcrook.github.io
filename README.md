
# GitHub Pages for account @idcrook

Lives at [https://idcrook.github.io/](https://idcrook.github.io/)  -\> [https://github.crookster.org/](https://github.crookster.org/)

Relies on GitHub infrastructure to generate the output from `jekyll` and serve.

## Building and generating locally

See [UsingDockerToServe.md](UsingDockerToServe.md)

## Resources

Used [jekyll-now](https://github.com/barryclark/jekyll-now/) as a starting point originally

<details>
  <summary>Details on running jekyll directly on macOS</summary>

**not recommended**

### macOS jekyll

```shell
brew install rbenv ruby-build
rbenv install 2.5.1
rbenv global 2.5.1
gem install bundler
# macOS Mojave: needed to rebuild native extensions on a couple gems
gem install jekyll
# jekyll serve
# ERROR: You have already activated jekyll 3.8.4, but your Gemfile requires jekyll 3.7.3. Prepending `bundle exec` to your command may solve this. (Gem::LoadError)

bundle exec jekyll serve
```


### On macOS Mojave, a hiccup to rebuild extensions

`gem install ...` actually provided the following caommands in warning to fix them

```shell
gem pristine commonmarker --version 0.17.9
gem pristine nokogiri --version 1.8.2
```

</details>
