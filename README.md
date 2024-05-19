# shakespeare.org

A collection of simple but very large [emacs org-mode](https://orgmode.org) files each comprised of the [collected plays of Shakespeare](./shakespeare.org).

The basic version has:
  - 32,120 headings
  - 147,582 lines
  - 946,282 words
  - 1,019 nested tags
  - 5,399,120 characters

Useful for performance and other testing of org.

Additional files include shallower headline nesting, `TODO`/`DONE` keywords, and list and heading statistics. 

<img width="660" alt="image" src="https://github.com/jdtsmith/shakespeare.org/assets/93749/07c093f5-4bdf-4019-a191-86b64d4fea45">

## Variants

- default: full (4-level) nesting, with tags
- `_depthN`: headline nesting limited to a maximum depth of `N`
- `_notags`: tags omitted
- `_todo`: include random `TODO`/`DONE` keywords on headings
- `_stats`: include `[/]` or `[%]` statistics markers on relevant headings and lists
- `_checkboxes`: include list checkboxes `[X]`, with random completion

## Updates

### **May, 2024**

- Added `--todo`,  `--stats`, and `--checkboxes` options, and associated files.

### **Mar, 2023**

- Added tags for all _titles_ (`:PLAY`, `:ACT`, `:SCENE`, etc.)
- Add separate headings for `INDUCT`, `INDUCTION`, `PROLOGUE`, `EPILOGUE`, `SUBTITLE1`
- Added `_notags` and `_depthN` variants

## Credits

[shakespeare-material](https://github.com/okfn/shakespeare-material)

