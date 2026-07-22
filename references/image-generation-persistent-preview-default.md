# Persistent Image Preview Default

For LALACHAN, every generated or edited still image should be saved to a stable
project path and opened in a persistent local desktop viewer. Rendering the
image only in the chat is not enough.

Default destination:

```text
artifacts/images/<descriptive-name>.png
```

Default workflow:

1. Keep the original image-generation output.
2. Copy the selected image into the project destination.
3. Verify that the destination is a non-empty image and inspect it visually.
4. Open it through the LazySkills helper so the viewer survives the launching
   command:

```bash
../LazySkills/skills/persistent-image-preview/scripts/open_image_persistent.sh \
  artifacts/images/<descriptive-name>.png
```

For a dedicated virtual desktop, pass its display explicitly, for example
`--display :98`. Do not claim the image was opened if no graphical display or
viewer was reachable.

This applies to character images, scene concepts, words cards, product images,
and other image-generation results unless the user explicitly asks not to open
the output.
