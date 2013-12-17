# -*- coding: utf-8 -*-

import sublime_plugin, re

class PlaceImageCommand(sublime_plugin.EventListener):
  def __init__(self):
    self.pi_snip = '<img src="http://placehold.it/${1:300x240}"${2: width="${1/^(?:[^\d]*)?([\d]*)x?.*$/$1/i}" height="${1/^(?:[^\d]*)([\d]*?)x?([\d]*)(?:[^x]*)?$/$+/i}"}${4: title="${3:PLACE.IT: [${1/^(?:[^\d]*)?([\d]*)x?.*$/$1/i} x ${1/^(?:[^\d]*)([\d]*?)x?([\d]*)(?:[^x]*)?$/$+/i}]}"} alt="${5:Edit Me}" />'
    self.placeit = '<img src="http://placehold.it/%sx%s"${1: width="%s" height="%s"}${3: title="${2:PLACE.IT: [%s x %s]}"} alt="${4:Edit Me}" />'
    self.kitten  = '<img src="http://placekitten.com/%s/%s"${1: width="%s" height="%s"} title="${2:KITTEN: [%s x %s]}" alt="${3:Edit Me}" />'
    self.pattern = r'^pi(?:(\d+)(?:(x|X)(\d+))?)?$'

  def on_query_completions(self, view, prefix, locations):
    match = re.match(self.pattern, prefix)

    if match:
      groups = match.groups()
      numNil = groups.count(None)

      # handle tab trigger: `pi`
      if numNil == 3:
        value = self.pi_snip

      # handle tab trigger: `pi{numbers}`
      elif numNil == 2:
        width  = groups[0]
        height = width
        value  = self.placeit % ((width, height) * 3)

      # handle tab trigger: `pi{width}(x|X){height}`
      else:
        width  = groups[0]
        height = groups[2]
        source = self.placeit if groups[1] == 'x' else self.kitten
        value  = source % ((width, height) * 3)
    else:
      value = None

    return [(prefix, prefix, value)] if value else []
