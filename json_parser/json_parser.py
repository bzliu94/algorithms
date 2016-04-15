# 2016-04-14

# note that we did something unusual that was fine for this grammar;
# we have a lookahead character instead of a lookahead token

# the grammar is a special case of LL(1) 
# where all types of tokens share disjoint sets of starting characters

# we dodged a bullet by not specifying FOLLOW sets 
# for non-terminals that don't have EPSILON as a production, 
# but if we had, we would have had to include 
# EOF for object, array, json

# 2016-01-07

# json parser; produces python value for a given json expression

# is fairly slow

import re
import string
import sys
"""
without actions
json -> object | array
object -> '{' object_p '}'
object_p -> pair object_p2 | EPSILON
object_p2 -> ',' object_p | EPSILON
pair -> STRING ':' value
array -> '[' array_p ']'
array_p -> value array_p2 | EPSILON
array_p2 -> ',' array_p | EPSILON
value -> STRING | NUMBER | object | array | 'true' | 'false' | 'null'
"""
"""
with actions
json -> object { json.value = object.value }
json -> array { json.value = array.value }
object -> '{' object_p '}' { object.value = object_p.value }
object_p -> pair object_p2 { object_p.value = object_p2.value; object_p.value.update(pair) }
object_p -> EPSILON { object_p.value = {} }
object_p2 -> ',' object_p { object_p2.value = object_p.value }
object_p2 -> EPSILON { object_p2.value = {} }
pair -> STRING ':' value { pair.value = {}; pair.value[STRING.value] = value.value }
array -> '[' array_p ']' { array.value = array_p.value }
array_p -> value array_p2 { array_p.value = array_p2.value; array_p.value.insert(0, value) }
array_p -> EPSILON { array_p.value = [] }
array_p2 -> ',' array_p { array_p2.value = array_p.value }
array_p2 -> EPSILON { array_p2.value = [] }
value -> STRING | NUMBER | object | array | 'true' | 'false' | 'null' { value.value = r0.value }
"""
class Token:
  def __init__(self, text):
    self.text = text
  def getText(self):
    return self.text
  def isStringToken(self):
    return False
  def isNumberToken(self):
    return False
  def isMiscToken(self):
    return False
class StringToken(Token):
  def __init__(self, text):
    Token.__init__(self, text)
  def isStringToken(self):
    return True
class NumberToken(Token):
  def __init__(self, text):
    Token.__init__(self, text)
  def isNumberToken(self):
    return True
class MiscToken(Token):
  def __init__(self, text):
    Token.__init__(self, text)
  def isMiscToken(self):
    return True
def getTokens(lexeme_seq_line, OVERALL_RE):
  curr_line = lexeme_seq_line
  regex = re.compile(OVERALL_RE)
  tokens = []
  while curr_line != "":
    m = regex.match(curr_line)
    lexeme_text = m.group(0)
    token = None
    if m.group("ws") != None:
      pass
    elif m.group("string") != None:
      token = StringToken(lexeme_text)
    elif m.group("number") != None:
      token = NumberToken(lexeme_text)
    elif m.group("misc") != None:
      token = MiscToken(lexeme_text)
    if token != None:
      tokens.append(token)
    curr_line = regex.sub("", curr_line, count = 1)
  return tokens
"""
STRING
   : '"' (ESC | ~ ["\\])* '"'
   ;
fragment ESC
   : '\\' (["\\/bfnrt] | UNICODE)
   ;
fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;
fragment HEX
   : [0-9a-fA-F]
   ;
NUMBER
   : '-'? INT '.' [0-9]+ EXP? | '-'? INT EXP | '-'? INT
   ;
fragment INT
   : '0' | [1-9] [0-9]*
   ;
// no leading zeros for exp. component
fragment EXP
   : [Ee] [+\-]? INT
   ;
// \- since - means "range" inside [...]
WS
   : [ \n\r\t\f\v]+ -> skip
   ;
"""
"""
FIRST(json) = {'{', '['}
FIRST(object) = {'{'}
FIRST(object_p) = {epsilon} | FIRST(STRING)
FIRST(object_p2) = {',', epsilon}
FIRST(pair) = FIRST(STRING)
FIRST(array) = {'['}
FIRST(array_p) = {epsilon, 't', 'f', 'n', '{', '['} | FIRST(STRING) | FIRST(NUMBER)
FIRST(array_p2) = {',', epsilon}
FIRST(value) = {'t', 'f', 'n', '{', '['} | FIRST(STRING) | FIRST(NUMBER)
FOLLOW(object_p) = {'}'}
FOLLOW(object_p2) {'}'}
FOLLOW(array_p) = {']'}
FOLLOW(array_p2) = {']'}
FIRST(STRING) = {'"'}
FIRST(NUMBER) = {'-', [0-9]}
FIRST(TRUE) = {'t'}
FIRST(FALSE) = {'f'}
FIRST(NULL) = {'n'}
"""
from collections import deque
class Parser:
  def __init__(self, tokens, FIRST_SETS, FOLLOW_SETS, regex_dsr, regex_float):
    self.token_deque = deque(tokens)
    self.first_sets = FIRST_SETS
    self.follow_sets = FOLLOW_SETS
    self.regex_dsr = regex_dsr
    self.regex_float = regex_float
  def getFirstSets(self):
    return self.first_sets
  def getFollowSets(self):
    return self.follow_sets
  def getRegexDSR(self):
    return self.regex_dsr
  def getRegexFloat(self):
    return self.regex_float
  def parse(self):
    root_node = self.json()
    tree = TokenTree()
    tree.setRoot(root_node)
    return tree
  def json(self):
    curr_char = self._getLookaheadChar()
    node = JSONNode(self._getNextToken())
    FIRST_SETS = self.getFirstSets()
    if curr_char in FIRST_SETS["object"]:
      object_node = self.object()
      node.addChildAtRight(object_node)
    elif curr_char in FIRST_SETS["array"]:
      array_node = self.array()
      node.addChildAtRight(array_node)
    else:
      self.error()
    return node
  def scan(self, char):
    # curr_str = char
    self.matchString(char)
  def object(self):
    node = ObjectNode(self._getNextToken())
    self.scan("{")
    object_p_node = self.object_p()
    node.addChildAtRight(object_p_node)
    self.scan("}")
    return node
  def object_p(self):
    curr_char = self._getLookaheadChar()
    node = ObjectPNode(self._getNextToken())
    FIRST_SETS = self.getFirstSets()
    FOLLOW_SETS = self.getFollowSets()
    if curr_char in FIRST_SETS["pair"]:
      pair_node = self.pair()
      node.addChildAtRight(pair_node)
      object_p2_node = self.object_p2()
      node.addChildAtRight(object_p2_node)
      return node
    elif curr_char in FOLLOW_SETS["object_p"]:
      return node
    else:
      self.error()
    # return node
  def object_p2(self):
    curr_char = self._getLookaheadChar()
    node = ObjectP2Node(self._getNextToken())
    FOLLOW_SETS = self.getFollowSets()
    if curr_char == ',':
      self.scan(',')
      object_p_node = self.object_p()
      node.addChildAtRight(object_p_node)
      return node
    elif curr_char in FOLLOW_SETS["object_p2"]:
      return node
    else:
      self.error()
    # return node
  def STRING(self):
    token = self._getNextToken()
    node = STRINGNode(token, self.getRegexDSR())
    if token.isStringToken() == True:
      self._removeNextToken()
    else:
      self.error()
    return node
  def NUMBER(self):
    token = self._getNextToken()
    node = NUMBERNode(token, self.getRegexFloat())
    if token.isNumberToken() == True:
      self._removeNextToken()
    else:
      self.error()
    return node
  def pair(self):
    node = PairNode(self._getNextToken())
    string_node = self.STRING()
    node.addChildAtRight(string_node)
    self.scan(':')
    value_node = self.value()
    node.addChildAtRight(value_node)
    return node
  def array(self):
    node = ArrayNode(self._getNextToken())
    self.scan('[')
    array_p_node = self.array_p()
    node.addChildAtRight(array_p_node)
    self.scan(']')
    return node
  def array_p(self):
    curr_char = self._getLookaheadChar()
    node = ArrayPNode(self._getNextToken())
    FIRST_SETS = self.getFirstSets()
    FOLLOW_SETS = self.getFollowSets()
    if curr_char in FIRST_SETS["value"]:
      value_node = self.value()
      node.addChildAtRight(value_node)
      array_p2_node = self.array_p2()
      node.addChildAtRight(array_p2_node)
    elif curr_char in FOLLOW_SETS["array_p"]:
      pass
    else:
      self.error()
    return node
  def array_p2(self):
    curr_char = self._getLookaheadChar()
    node = ArrayP2Node(self._getNextToken())
    FOLLOW_SETS = self.getFollowSets()
    if curr_char == ',':
      self.scan(',')
      array_p_node = self.array_p()
      node.addChildAtRight(array_p_node)
    elif curr_char in FOLLOW_SETS["array_p2"]:
      pass
    else:
      self.error()
    return node
  def value(self):
    token = self._getNextToken()
    curr_char = self._getLookaheadChar()
    node = ValueNode(token)
    FIRST_SETS = self.getFirstSets()
    if token.isStringToken() == True:
      string_node = self.STRING()
      node.addChildAtRight(string_node)
    elif token.isNumberToken() == True:
      number_node = self.NUMBER()
      node.addChildAtRight(number_node)
    elif curr_char in FIRST_SETS["object"]:
      object_node = self.object()
      node.addChildAtRight(object_node)
    elif curr_char in FIRST_SETS["array"]:
      array_node = self.array()
      node.addChildAtRight(array_node)
    elif curr_char in FIRST_SETS["TRUE"]:
      true_node = self.TRUE()
      node.addChildAtRight(true_node)
    elif curr_char in FIRST_SETS["FALSE"]:
      false_node = self.FALSE()
      node.addChildAtRight(false_node)
    elif curr_char in FIRST_SETS["NULL"]:
      null_node = self.NULL()
      node.addChildAtRight(null_node)
    else:
      self.error()
    return node
  def TRUE(self):
    node = TRUENode(self._getNextToken())
    self.matchString('true')
    return node
  def FALSE(self):
    node = FALSENode(self._getNextToken())
    self.matchString('false')
    return node
  def NULL(self):
    node = NULLNode(self._getNextToken())
    self.matchString('null')
    return node
  def error(self):
    raise Exception()
  def _getTokens(self):
    return self.token_deque
  def _getNextToken(self):
    return self.token_deque[0]
  def _removeNextToken(self):
    # self.tokens = self.tokens[1 : ]
    self.token_deque.popleft()
  def matchString(self, curr_str):
    next_token = self._getNextToken()
    text = next_token.getText()
    if curr_str == text:
      self._removeNextToken()
    else:
      self.error()
  def _getLookaheadChar(self):
    next_token = self._getNextToken()
    text = next_token.getText()
    return text[0]
class TokenTree:
  def __init__(self):
    self.root = None
  def setRoot(self, node):
    self.root = node
  def getRoot(self):
    return self.root
  def toString(self):
    root = self.getRoot()
    return root.toString()
  def getValue(self):
    return self.getRoot().getValue()
class TokenNode:
  def __init__(self, token, children):
    self.token = token
    self.children = children
  def getToken(self):
    return self.token
  def addChildAtRight(self, child):
    self.children.append(child)
  def getOrderedChildren(self):
    return self.children[ : ]
  def getIthChild(self, i):
    return self.children[i]
  def getName(self):
    return "N/A"
  def getStringComponents(self):
    children = self.getOrderedChildren()
    child_str_list = [x.toString() for x in children]
    components_list = [self.getName()] + child_str_list
    return components_list
  def toString(self):
    components_list = self.getStringComponents()
    if len(components_list) == 1:
      return components_list[0]
    joined_str = string.join(components_list, " ")
    overall_str = "(" + joined_str + ")"
    return overall_str
  def getValue(self):
    pass
  def error(self):
    raise Exception()
class JSONNode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getName(self):
    return "json"
  def getValue(self):
    child = self.getOrderedChildren()[0]
    return child.getValue()
class ObjectNode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getStringComponents(self):
    children = self.getOrderedChildren()
    child_str_list = [x.toString() for x in children]
    components_list = [self.getName(), '{'] + child_str_list + ['}']
    return components_list
  def getName(self):
    return "object"
  def getValue(self):
    child = self.getOrderedChildren()[0]
    return child.getValue()
class ObjectPNode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getName(self):
    return "object_p"
  def getValue(self):
    children = self.getOrderedChildren()
    if len(children) == 0:
      return {}
    elif len(children) == 2:
      pair_node = children[0]
      object_p2_node = children[1]
      pair_value = pair_node.getValue()
      object_p2_value = object_p2_node.getValue()
      object_p2_value.update(pair_value)
      return object_p2_value
    else:
      self.error()
class ObjectP2Node(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getStringComponents(self):
    children = self.getOrderedChildren()
    if len(children) == 0:
      return [self.getName()]
    child_str_list = [x.toString() for x in children]
    components_list = [self.getName(), ','] + child_str_list
    return components_list
  def getName(self):
    return "object_p2"
  def getValue(self):
    children = self.getOrderedChildren()
    if len(children) == 0:
      return {}
    elif len(children) == 1:
      object_p_node = children[0]
      object_p_value = object_p_node.getValue()
      return object_p_value
class STRINGNode(TokenNode):
  def __init__(self, token, regex_dsr):
    TokenNode.__init__(self, token, [])
    self.regex_dsr = regex_dsr
  def getRegexDSR(self):
    return self.regex_dsr
  def getName(self):
    return "STRING"
  def toString(self):
    token = self.getToken()
    lexeme = token.getText()
    return lexeme
  def getValue(self):
    token = self.getToken()
    lexeme_text = token.getText()
    regex_dsr = self.getRegexDSR()
    m_dsr = regex_dsr.match(lexeme_text)
    next_lexeme_text = m_dsr.group(1)
    return next_lexeme_text
class NUMBERNode(TokenNode):
  def __init__(self, token, regex_float):
    TokenNode.__init__(self, token, [])
    self.regex_float = regex_float
  def getRegexFloat(self):
    return self.regex_float
  def getName(self):
    return "NUMBER"
  def toString(self):
    token = self.getToken()
    lexeme = token.getText()
    return lexeme
  def getValue(self):
    token = self.getToken()
    lexeme_text = token.getText()
    regex_float = self.getRegexFloat()
    m_float = regex_float.match(lexeme_text)
    value = None
    if m_float != None:
      value = float(lexeme_text)
    else:
      value = int(lexeme_text)
    return value
class PairNode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getStringComponents(self):
    children = self.getOrderedChildren()
    child_str_list = [x.toString() for x in children]
    string_node = child_str_list[0]
    value_node = child_str_list[1]
    components_list = [self.getName(), string_node, ':', value_node]
    return components_list
  def getName(self):
    return "pair"
  def getValue(self):
    children = self.getOrderedChildren()
    string_node = children[0]
    value_node = children[1]
    string_value = string_node.getValue()
    value_value = value_node.getValue()
    value = {}
    value[string_value] = value_value
    return value
class ArrayNode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getStringComponents(self):
    children = self.getOrderedChildren()
    child_str_list = [x.toString() for x in children]
    components_list = [self.getName(), '['] + child_str_list + [']']
    return components_list
  def getName(self):
    return "array"
  def getValue(self):
    children = self.getOrderedChildren()
    array_p_node = children[0]
    array_p_value = array_p_node.getValue()
    return array_p_value
class ArrayPNode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getName(self):
    return "array_p"
  def getValue(self):
    children = self.getOrderedChildren()
    if len(children) == 0:
      return []
    elif len(children) == 2:
      value_node = children[0]
      array_p2_node = children[1]
      value_value = value_node.getValue()
      array_p2_value = array_p2_node.getValue()
      value = array_p2_value
      value.insert(0, value_value)
      return value
class ArrayP2Node(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getStringComponents(self):
    children = self.getOrderedChildren()
    if len(children) == 0:
      return [self.getName()]
    child_str_list = [x.toString() for x in children]
    components_list = [self.getName(), ','] + child_str_list
    return components_list
  def getName(self):
    return "array_p2"
  def getValue(self):
    children = self.getOrderedChildren()
    if len(children) == 0:
      return []
    elif len(children) == 1:
      array_p_node = children[0]
      array_p_value = array_p_node.getValue()
      return array_p_value
class ValueNode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getName(self):
    return "value"
  def getValue(self):
    children = self.getOrderedChildren()
    child = children[0]
    value = child.getValue()
    return value
class TRUENode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getName(self):
    return "TRUE"
  def toString(self):
    token = self.getToken()
    lexeme = token.getText()
    return lexeme
  def getValue(self):
    return True
class FALSENode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getName(self):
    return "FALSE"
  def toString(self):
    token = self.getToken()
    lexeme = token.getText()
    return lexeme
  def getValue(self):
    return False
class NULLNode(TokenNode):
  def __init__(self, token):
    TokenNode.__init__(self, token, [])
  def getName(self):
    return "NULL"
  def toString(self):
    token = self.getToken()
    lexeme = token.getText()
    return lexeme
  def getValue(self):
    return None
def parse(line, OVERALL_RE, FIRST_SETS, FOLLOW_SETS, regex_dsr, regex_float):
  tokens = getTokens(line, OVERALL_RE)
  parser = Parser(tokens, FIRST_SETS, FOLLOW_SETS, regex_dsr, regex_float)
  token_tree = parser.parse()
  return token_tree.getValue()

def main():
  # lexer regular expression values
  HEX_RE = r'(?:[0-9a-fA-F])'
  UNICODE_RE = r'(?:u' + HEX_RE + HEX_RE + HEX_RE + HEX_RE + r')'
  ESC_RE = r'(?:\\(?:["\\/bfnrt]|' + UNICODE_RE + r'))'
  STRING_RE = r'(?:"(?:' + ESC_RE + r'|[^"\\])*")'
  INT_RE = r'(?:0|(?:[1-9][0-9]*))'
  EXP_RE = r'(?:[Ee][+\-]?' + INT_RE + r')'
  FLOAT_RE = r'(?:(?:-?' + INT_RE + r'\.[0-9]+(?:' + EXP_RE + r')?)|(?:-?' + INT_RE + EXP_RE + r'))'
  NUMBER_RE = r'(?:' + FLOAT_RE + r'|(?:-?' + INT_RE + r'))'
  WS_RE = r'(?:[ \n\r\t\f\v]+)'
  COMMA_RE = r','
  OPEN_CURLY_BRACE_RE = r'\{'
  CLOSE_CURLY_BRACE_RE = r'\}'
  COLON_RE = r':'
  OPEN_SQUARE_BRACE_RE = r'\['
  CLOSE_SQUARE_BRACE_RE = r'\]'
  TRUE_RE = r'true'
  FALSE_RE = r'false'
  NULL_RE = r'null'
  MISC_RE = r'(?:' + COMMA_RE + r'|' + OPEN_CURLY_BRACE_RE + r'|' + CLOSE_CURLY_BRACE_RE + r'|' + COLON_RE + r'|' + OPEN_SQUARE_BRACE_RE + r'|' + CLOSE_SQUARE_BRACE_RE + r'|' + TRUE_RE + r'|' + FALSE_RE + r'|' + NULL_RE + r')'
  OVERALL_RE = r'(?P<string>' + STRING_RE + r')|(?P<number>' + NUMBER_RE + r')|(?P<misc>' + MISC_RE + r')|(?P<ws>' + WS_RE + r')'
  DEQUOTE_STR_RE = r'"(.*)"'
  # FIRST and FOLLOW
  FIRST = {}
  FOLLOW = {}
  EPSILON = -1
  DIGITS0TO9 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  FIRST["STRING"] = ['"']
  FIRST["NUMBER"] = ['-'] + DIGITS0TO9
  FIRST["TRUE"] = ['t']
  FIRST["FALSE"] = ['f']
  FIRST["NULL"] = ['n']
  FIRST["json"] = ['{', '[']
  FIRST["object"] = ['{']
  FIRST["object_p"] = [EPSILON] + FIRST["STRING"]
  FIRST["object_p2"] = [',', EPSILON]
  FIRST["pair"] = FIRST["STRING"]
  FIRST["array"] = ['[']
  FIRST["array_p"] = [EPSILON, 't', 'f', 'n', '{', '['] + FIRST["STRING"] + FIRST["NUMBER"]
  FIRST["array_p2"] = [',', EPSILON]
  FIRST["value"] = ['t', 'f', 'n', '{', '['] + FIRST["STRING"] + FIRST["NUMBER"]
  FOLLOW["object_p"] = ['}']
  FOLLOW["object_p2"] = ['}']
  FOLLOW["array_p"] = [']']
  FOLLOW["array_p2"] = [']']
  FIRST_SETS = {}
  FOLLOW_SETS = {}
  for key in FIRST.keys():
    value = FIRST[key]
    FIRST_SETS[key] = set(value)
  for key in FOLLOW.keys():
    value = FOLLOW[key]
    FOLLOW_SETS[key] = set(value)
  # prepare misc. regular expression matchers
  regex_dsr = re.compile(DEQUOTE_STR_RE)
  regex_float = re.compile(FLOAT_RE)
  # read from prompt
  stream = sys.stdin
  lexeme_seq_line = stream.readline()
  value = parse(lexeme_seq_line, OVERALL_RE, FIRST_SETS, FOLLOW_SETS, regex_dsr, regex_float)
  print value
  """
  # read from file
  stream = open("tests/official/input00.txt")
  line = stream.readline()
  n = int(line)
  for i in xrange(n):
    line = stream.readline()
    # print line
    value = parse(line, OVERALL_RE, FIRST_SETS, FOLLOW_SETS, regex_dsr, regex_float)
    # print value
  """
main()
