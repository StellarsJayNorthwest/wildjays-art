# wildjays-art

This is the repo for the Jekyll version of wildjays.art.

Currently publishing to https://wildjays.art and https://stellarsjaynorthwest.github.io/wildjays-art/

The old version is sort of working (admin is borked): at https://wildjaysblog.azurewebsites.net

## Local edit instructions
- Open WSL
- Run code from WSL to open the repo directory: code repos/wildjays-art
- From the VS Code terminal: bundle exec jekyll serve --livereload
- Use git from within VS Code (UI or terminal) for easier authentication
- Push to master to publish!

## Gallery instructions: two images side-by-side

This is a Poor Man's gallery. The images needs to be the same size as I'm not expert enough to figure out how to scale them.

Lightroom: Crop images to 4x6. Export using "Blog side by side 4x6 gallery".
```
<div class="galleryouter">
  <div class="galleryinner">
    <img src="{{ site.baseurl }}/assets/20231124/g1/NZ7_9578.jpg" alt="Mushroom">
  </div>
</div>
<div class="galleryouter">
  <div class="galleryinner">
    <img src="{{ site.baseurl }}/assets/20231124/g1/NZ7_9579.jpg" alt="Mushroom">
  </div>
</div>
<div class="endgallery"></div>
```

## Gallery instructions: three? images side-by-side

TODO: Might be nice to have a three-banger gallery for portrait images but I haven't added the CSS for that yet.
