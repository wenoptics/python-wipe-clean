# ##############################################
#
# This module is are mostly borrowed from `rich`
#
# ##############################################

# `rich` is an excellent, feature-rich and well-maintained library. But here are some reasons of
#   extracting from `rich` (apart from pursuing 0-dep)
#
#   1. To achieve simple terminal drawing, we don't need most of the features from `rich`.
#   2. We don't want the dependencies brought by `rich` (although they are not a lot)
#   3. We want to be able to backport to python 2.7
