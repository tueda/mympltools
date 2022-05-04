# Changelog


<a name="22.5.1"></a>
## [22.5.1] (2022-05-04)
### Fixed
- Remove `print` for debugging.
  ([52a7926](https://github.com/tueda/mympltools/commit/52a7926730b71bcfde7b140ef5d7a236283688f5))


<a name="22.5.0"></a>
## [22.5.0] (2022-05-03)
### Added
- `fitting` module, a wrapper module for
  [scipy.optimize](https://docs.scipy.org/doc/scipy/reference/optimize.html).
  To use the `fit` function in this module, SciPy is required.
  One can specify the pip extra `#egg=mympltools[fitting]` to install SciPy as a dependency.
  ([9d71f6b](https://github.com/tueda/mympltools/commit/9d71f6bf345388bc75033eb873f8774e06275311))


<a name="21.11.0"></a>
## [21.11.0] (2021-11-16)
### BREAKING CHANGE
- We stop automatically changing the style when `mympltools` is imported.
  This change allows one to use some utility functions in this package without
  changing his/her style.
  To use the style sheet in this package, the user must explicitly call
  `use`.
  ([4aef33d](https://github.com/tueda/mympltools/commit/4aef33d578ed80a157f9de50a19ffbc232693d1a))

### Added
- `subcmap` to extract a part of a color map.
  ([e0a566d](https://github.com/tueda/mympltools/commit/e0a566d4e9e58db8a812ee0db2ee36547b376747))


<a name="21.10.1"></a>
## [21.10.1] (2021-10-24)
### Added
- `xytext` option to `line_annotate`.
  ([61404fd](https://github.com/tueda/mympltools/commit/61404fd4bd1be3c6fd57877bfee04a2a039013b0))

### Fixed
- `rotation` option in `line_annotate`.
  ([881d566](https://github.com/tueda/mympltools/commit/881d566728b6dcaee1305e24ba0fa654a472996a))


<a name="21.10.0"></a>
## 21.10.0 (2021-10-22)
- First release.


[22.5.1]: https://github.com/tueda/mympltools/compare/22.5.0...22.5.1
[22.5.0]: https://github.com/tueda/mympltools/compare/21.11.0...22.5.0
[21.11.0]: https://github.com/tueda/mympltools/compare/21.10.1...21.11.0
[21.10.1]: https://github.com/tueda/mympltools/compare/21.10.0...21.10.1
