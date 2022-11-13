import nimpy
from std/sequtils import newSeqWith
from std/strutils import toLowerAscii, contains
from std/editDistance import editDistance


func maybeLower(s: string, lower: bool): string =
  if lower:
    return toLowerAscii(s)
  else:
    return s

func contains_one_of(x: string, y: seq[string], toLower: bool = true): bool {.exportpy.} =
  let str = maybeLower(x, toLower)
  for i in y:
    if str.contains(maybeLower(i, toLower)):
      return true
  return false

func contains_constant(x: seq[string], toLower: bool = true): bool {.exportpy.} =
  const name = "constant"
  for i in x:
    if maybeLower(i, toLower).contains(name):
      return true
  return false

func levenshtein_distance(x, y: string, toLower: bool = true): int {.exportpy.} =
  return editDistance(maybeLower(x, toLower), maybeLower(y, toLower))

func find_common_substring(x, y: string,
    toLower: bool = true): string {.exportpy.} =
  # mostly stolen from rosettacode.org
  let a = maybeLower(x, toLower)
  let b = maybeLower(y, toLower)

  var lengths = newSeqWith(a.len, newSeq[int](b.len))
  var greatestLength = 0
  for i, x in a:
    for j, y in b:
      if x == y:
        lengths[i][j] = if i == 0 or j == 0: 1 else: lengths[i - 1][j - 1] + 1
        if lengths[i][j] > greatestLength:
          greatestLength = lengths[i][j]
          result = a[(i - greatestLength + 1)..i]
  return result

func find_common_sequence(x, y: string, toLower: bool = true): string {.exportpy.} =
  let a = maybeLower(x, toLower)
  let b = maybeLower(y, toLower)

  var ls = newSeq[seq[int]](a.len+1)
  for i in 0 .. a.len:
    ls[i].newSeq(b.len+1)

  for i, x in a:
    for j, y in b:
      if x == y:
        ls[i+1][j+1] = ls[i][j] + 1
      else:
        ls[i+1][j+1] = max(ls[i+1][j], ls[i][j+1])

  result = ""

  let j = b.len
  for i in 1 .. a.len:
    if ls[i][j] != ls[i - 1][j]:
      result = result & a[i - 1]

  return result
