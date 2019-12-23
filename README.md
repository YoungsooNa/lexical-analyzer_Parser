# lexical-analyzer_Parser
My lexical analyzer and Parser
<br><br><br>


## Usage
 1. move to directory of parser
 2. type >> main.py code_path
 3. token table and parsing_table.json are generated.
 4. You can see the printed result which code is correct or not.
 
 <br><br><br>
## The process of parser

1. creating a LL(1) parsing table
2. top down parsing with LL(1) parsing table
3. If correct then print code is correct! else print error with details.

1.The process of creating a parsing table
1.0. define suitable CFG and terminals and non-terminal and start non-terminal for LL(1)
1.1.  get first set of nonterminals in CFG
1.2.  get follow set of nonterminals in CFG
1.3. let’s make LL(1) parsing table

1.1 The process of get first set of nonterminals in CFG

1.1.1  for all nonterminal add the nonterminal to unsolved_nt list
1.1.2  if terminal derivated by some nonterminal then add terminal to first set of the nonterminal
1.1.3  if nonterminal derivated by some nonterminal then add nonterminal to unsolved_nt list
1.1.4  repeat until unsolved_nt is empty

1.2  The process of get follow set of nonterminals in CFG

1.2.1 if A is a nonterminal and start sign then FOLLOW(A) include $
1.2.2  if B -> aAb, b != epsilon then FOLLOW(A) include FIRST(b) without epsilon
1.2.3  if B -> aA or B -> aAb b=>epsilon then add FOLLOW(B) to FOLLOW(A)

1.2.1.1 add $ to follow set of start nonterminal

1.2.2.1 If word is non terminal and next word exist
1.2.2.2 If next word is terminal then add to word in follow set
1.2.2.3 If next word is non terminal then check next word equal epsilon. If not add first set of next word to follow set of word

1.2.3.1 If the word is nonterminal and word is the last word then follow set of word include follow set of nonterminal
1.2.3.2 If the word is nonterminal and word is not the last word and all of word’s next sentence can be derivate to epsilon then follow set of the word include nonterminal.
1.2.3.3 Rule 3 for getting the follow set has a difficult problem that all follow set will be changed.
1.2.3.4 solve this problem by saving relation of follow set so try adding a terminal to set of follow until no change.

1.2.3.2.1 The way of know expression can be derivated to epsilon.
1.2.3.2.2 All word in expression must derivate to epsilon.

1.3. let’s make LL(1) parsing table

1.3.1 A -> exp , for a in First(exp) -> M[A, a] = A ->　exp
1.3.1.1 get the first set of expression
1.3.1.2 if length of first set is bigger then 0 it means LL(1)[nonterminal][element of first set] = nonterminal -> exp

1.3.2.0 If exp(expression) is in CFG ＝＞A -> a exp b then 
1.3.2.1 if b => epsilon then for b in Follow(A) M[A, b] = A -> exp
1.3.2.2 calculate A -> exp b then b 


2. The process of getting top down parsing with LL(1) parsing table

2.1 make stack for parser
2.2 make input code string queue and type queue
2.3 getting expression from parser.pop() and type queue.popleft() from parsing table
2.4 if two terminals from parser.pop() and queue.popleft() same remove both.
2.5 if not add word in expression by reverse order to stack
2.6 loop until stack has only end sign.
2.7 If error occur then print error message and stack , remain string 
2.7.1 error occurred by two state.
2.7.2 If parsing table is empty with M[stack_pop, string_type] = Null
2.7.3 If stack_pop not include parsing table’s keys.

3. If correct then print code is correct! else print error with details.
3.1 define parser function return True and False, and before returning print message
