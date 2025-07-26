class FirstFollowCalc:
  def __init__(self, grammar):
      self.grammar = {}
      self.first = {}
      self.follow = {}
      self.non_terminals = set()
      self.terminals = set()
      self.epsilon = 'ε'  # Use 'ε' for epsilon
      self.start_symbol = None
      self.add_grammar(grammar)
      self.calc_first()
      self.calc_follow()

  def add_grammar(self, grammar):
      for i, (lhs, rhs_list) in enumerate(grammar.items()):
          if i == 0: # Assume the first key is the start symbol
              self.start_symbol = lhs
          self.non_terminals.add(lhs)
          if lhs not in self.grammar:
              self.grammar[lhs] = []
          for rhs in rhs_list:
              self.grammar[lhs].append(rhs)
              for symbol in rhs:
                  if not symbol.isupper() and symbol != self.epsilon:
                      self.terminals.add(symbol)

  def calc_first(self):
      for nt in self.non_terminals:
          self._compute_first(nt)

  def _compute_first(self, symbol):
      if symbol in self.first:
          return self.first[symbol]

      self.first[symbol] = set()

      if symbol in self.grammar: # Non-terminal
          for production in self.grammar[symbol]:
              if production == self.epsilon:
                  self.first[symbol].add(self.epsilon)
              else:
                  for char in production:
                      if not char.isupper() and char != self.epsilon: # Terminal
                          self.first[symbol].add(char)
                          break
                      elif char.isupper(): # Non-terminal
                          first_of_char = self._compute_first(char)
                          self.first[symbol].update(first_of_char - {self.epsilon})
                          if self.epsilon not in first_of_char:
                              break
                  else: # If the loop completes without breaking (all symbols derived epsilon)
                      if production != '': # Handle cases like A -> ε
                           self.first[symbol].add(self.epsilon)


      else: # Terminal or Epsilon
           if symbol != self.epsilon:
              self.first[symbol].add(symbol)
           else:
               self.first[symbol].add(self.epsilon)


      return self.first[symbol]

  def _compute_first_sequence(self, sequence):
      first_seq = set()
      if not sequence:
          first_seq.add(self.epsilon)
          return first_seq

      for symbol in sequence:
          first_of_symbol = self._compute_first(symbol)
          first_seq.update(first_of_symbol - {self.epsilon})
          if self.epsilon not in first_of_symbol:
              break
      else:
          first_seq.add(self.epsilon)
      return first_seq


  def calc_follow(self):
      # Initialize FOLLOW sets
      for nt in self.non_terminals:
          self.follow[nt] = set()

      # Add end-of-input marker to the start symbol's FOLLOW set
      if self.start_symbol:
          self.follow[self.start_symbol].add('$')

      changed = True
      while changed:
          changed = False
          for lhs, productions in self.grammar.items():
              for production in productions:
                  for i, symbol in enumerate(production):
                      if symbol in self.non_terminals:
                          # Rule 1: A -> αBβ
                          beta = production[i+1:]
                          first_beta = self._compute_first_sequence(beta)
                          old_follow_b = len(self.follow[symbol])
                          self.follow[symbol].update(first_beta - {self.epsilon})
                          if len(self.follow[symbol]) != old_follow_b:
                              changed = True

                          # Rule 2: A -> αB or A -> αBβ where ε is in FIRST(β)
                          if not beta or self.epsilon in first_beta:
                              old_follow_b = len(self.follow[symbol])
                              self.follow[symbol].update(self.follow[lhs])
                              if len(self.follow[symbol]) != old_follow_b:
                                  changed = True

  def display_first_sets(self):
      print("FIRST sets:")
      for symbol, first_set in self.first.items():
          print(f"{symbol}: {first_set}")

  def display_follow_sets(self):
      print("FOLLOW sets:")
      for symbol, follow_set in self.follow.items():
          print(f"{symbol}: {follow_set}")

  def display_sets(self):
      """Displays the calculated FIRST and FOLLOW sets."""
      self.display_first_sets()
      print("\n") # Add a newline for separation
      self.display_follow_sets()



# Use the previously defined grammar
grammar = {
    'S': ['AB'],
    'A': ['a', 'ε'], # 'ε' represents epsilon (empty string)
    'B': ['b', 'c']
}

calc = FirstFollowCalc(grammar)
# calc.display_first_sets()
# calc.display_follow_sets()
calc.display_sets()