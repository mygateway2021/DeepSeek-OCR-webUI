--- Page 26 ---

## History and Interface  


An interpreter (in the broad sense of the word) for a language is a program that takes text and executes it as code. When you have an interpreter available, exposing it as an eval construct, which does pretty much the same thing, is easy and obvious.  


The first language to do this was an early dialect of Lisp. More recent dynamic languages—Perl, Python, PHP, Ruby, and of course JavaScript—followed suit. Most of these languages went through a similar process, where they initially introduced a straightforward, naive evaluation construct, and later tried to refine, extend, or disable it as a form of damage control.  


The subtlety in designing an interface for code execution lies in the environment in which the code is to be interpreted—the question of which variables it can see. In a primitive interpreter, which often represents variables in a way that makes it easy to inspect and manipulate them, it is no problem to give evaluated code full access to all the variables that are visible at the point where the eval construct is used. The initial design of a dynamic language is often intertwined with the first implementation of its interpreter, and this makes it tempting to go with the model where the evaluated code has access to the local environment.  


There are two reasons why this is problematic. Firstly, there's rarely a reason to want to access local scope. You'll occasionally see some confused JavaScript programmers do something like eval("obj." + propertyName) because they fail to realize that the language allows dynamic property access, or eval("var result = " + code) because they are ignorant of the fact that eval already returns the result of the evaluation, and the var result = part could be lifted out. When the code string comes from an external source, there's also the risk of a variable in the string accidentally using a variable name that is also defined locally, causing a conflict between the two uses. The one case where access to a local scope is not completely wrongheaded is when evaluated code needs to have access to utility functions defined in the module that evaluates it. We'll see a decent way to work around that later.  


The second reason that evaluating in the local scope is not a good idea is that it makes life quite a bit harder for the compiler. Knowing exactly what the code it's compiling looks like enables a compiler to make a lot of decisions at compile time (rather than runtime), which makes the code it produces faster. Most importantly, if it knows a variable \(\mathbf{x}\) refers to a specific \(\mathbf{x}\) variable defined either globally or in one of its enclosing scopes, it can generate very simple code to access this \(\mathbf{x}\) . An eval could introduce a new variable \(\mathbf{x}\) , forcing the compiler to represent its environment in a more complex way and to output more expensive code for each variable access.  


And this last point is the reason for the very odd way in which JavaScript eval behaves—the distinction between local and global evaluation.


--- Page 27 ---

eval is, historically, a regular global variable that holds a function. That means you can do everything with it that you can do with other values—store it in another variable or in a data structure, pass it to a function, and so on. But because the people trying to optimize JavaScript execution did not want to represent all environments and variable accesses in the expensive, dynamic way I described previously, they introduced a subtle rule, probably initially as a hack, that was later standardized into ECMAScript.  


This rule is: the eval is only done in the local scope if we can see, during compilation, that a call to eval takes place—there has to be a function call to the actual global variable named eval in the code (and this global must still have its original value). If you call eval in any other, more indirect way, it will not have access to the local scope, and thus will be a global evaluation.  


For example, eval("foo") is local, while (0 || eval)("foo") is global, and so is var lave = eval; lave("foo").  


Though this was conceived purely as an efficiency kludge, not as an attempt to provide a better interface, people have been intentionally making use of it, since global evaluation is often more useful and less error- prone than local evaluation.  


Another variant of global evaluation is the Function constructor. It takes strings for the argument names and function body as arguments, and returns a function in the context of the global scope (it does not close over variables in the scope where it was created). Note that the argument names can be passed either as separate arguments (new Function("a", "b", "return a + b")) or as a single comma- separated string (new Function("a, b", "return a + b")). For most purposes, this is the preferred way to evaluate code.  


## Performance  


Evaluating code is expensive. Not only does the JavaScript compiler have to be invoked to compile the code, but modern JavaScript engines also tend to perform analysis on the loaded program in order to perform certain optimizations. Introducing new code can invalidate the results of such analysis, and cause recompilation of other parts of the program.  


Evaluation in local scope is extra worrying, for the reasons discussed before. I ran a number of benchmarks on modern JavaScript engines, and found that variable access that goes through a scope that can be accessed by a local eval form is significantly slower. This means that if you're using the closure module pattern (an anonymous function as module scope), having a local evaluation anywhere in your module will incur a cost for all code in the module. The scope just needs to have such a call—it doesn't even have to execute it—to incur this cost.


--- Page 28 ---

On the other hand, the speed of a function created by new Function or a global eval is not adversely affected by the fact that it was created dynamically.  


So, a desirable pattern is one where the evaluation happens once (at program startup), or outside of hot loops (we're talking about few- millisecond delays here, not interface- freezing disasters). The functions generated by the evaluation can then be used as intensively as needed.  


## Common Uses  


The most obvious use of eval is dynamically running code from an external source: for example, in a module- manager library that fetches code from somewhere and then uses a global eval to inject it into the environment, or an interactive repl (read- eval- print loop) that executes code that the user types.  


In the past, eval was the easiest way to parse strings of JSON data, whose representation is a subset of JavaScript's own syntax. In modern implementations we have JSON.parse for that, which has the significant advantage of not enabling code injection attacks when parsing untrusted data.  


Most JavaScript- based text templating systems use some form of eval to precompile templates. They parse the template text once, produce a program that instantiates the template, and use eval to have the JavaScript compiler compile that. In some cases this is simply an optimization, but in others the templates may contain JavaScript code, so some form of eval has to be involved. We'll go over the compiler for a simple JavaScript- based templating language in the next section.  


A template is a kind of domain- specific language (DSL), a language designed to solve a specific problem (in this case, building up strings) by being specialized to express the elements of that problem more directly than plain JavaScript. Domain- specific languages are a more interesting application of eval. We'll cover another one, a compact and efficient notation for matching and extracting binary data, later on in this chapter.  


## A Template Compiler  


Before you look at the code that follows, I should warn you. You opened a book called Beautiful JavaScript, and I'm about to confront you with some rather ugly code. That may seem disingenuous.  


Code that builds up strings of code tends to look bad. If we had string interpolation, a code- oriented templating system, or even a data structure that represented code, things might be slightly better. But as it is, we'll be crudely concatenating lots of strings, many of them containing the same keywords and syntactic patterns as the code around them. This does not make for very elegant or readable code.


--- Page 29 ---

The function shown here accepts a template string as an argument and returns a function that represents a compiled version of this template. It recognizes templating directives written between hash signs. Here's an example of a trivial template that it parses:  


\\(in.title# Items on today's list: #for item in \\$in.items\\* #item.name##if item.note# (Note: #item.note#) #end# #end#  


A directive starting with for opens a loop (over an array). An if directive opens a conditional. Both are closed by an end directive. Anything else is interpreted as a value that should simply be inserted as text into the output. The variable \(\mathfrak{S}\mathfrak{n}\) is used to refer to the value passed into the template.  


For brevity, the code does no input checking whatsoever. Here's the implementation of that function:  


function compile(template) { var code \(=\) "var_out \(=\) ';", uniq \(= 0\) var parts \(=\) template.split("#"); for (var i \(= 0\) ; i \(<\) parts.length; \(^{+ + }\) { var part \(=\) parts[i], m; if (i % 2) { // Odd elements are templating directives if (m \(=\) part.match(/^for (\\\(+\) in (.\\*)/)) { var loopVar \(=\) m[1], arrayExpr \(=\) m[2]; var indexVar \(=\) "_i" \(^+\) (++uniq), arrayVar \(=\) "_a" \(^+\) uniq; code \(^+ =\) "for (var \(^+\) + indexVar \(^+ = 0\) , \(^+\) arrayVar \(^+ =\) " \(^+\) arrayExpr \(^+ =\) "; \(^+\) indexVar \(^+ =\) "<" \(^+\) arrayVar \(^+ =\) ".length; \(^{+ + }\) + indexVar \(^+ =\) ) {" \(^+\) "var \(^+\) + loopVar \(^+ =\) " \(^+\) arrayVar \(^+\) [" \(^+\) indexVar \(^+ =\) "]; } else if (m \(=\) part.match(/^if (.\\*)/)) { code \(^+ =\) "if (" \(^+\) m[1] \(^+\) ") {"; } else if (part \(= =\) "end") { code \(^+ =\) "]; } else { code \(^+ =\) "_out \(^+ =\) " \(^+\) part \(^+ =\) "; } } else if (part) { // Even elements are plain text code \(^+ =\) "_out \(^+ =\) " \(^+\) JSON.stringify(part) \(^+ =\) "; } } return new Function("\\$in", code \(^+\) "return _out;"); }  


To locate the directives, the function simply splits the template on hash characters, and considers the even- numbered parts to be plain text and the odd- numbered elements (the parts that appear between hash characters) as templating directives. Regular expressions are used to recognize the if and for directives.


--- Page 30 ---

The _out variable in the generated code is used to build up the output string. The underscore is an attempt to avoid name clashes, since we'll be mixing generated code with code found in the template.  


To build a loop for a for directive, we need to introduce two additional variables into the generated code—one for the index and one to hold the array. We need a variable that holds the array to ensure that whatever expression is used to produce it is not evaluated repeatedly, since it might be expensive to compute or have side effects. In order to make sure that these variable names do not clash, even for nested loops, a counter (uniq) is added to the variable name (_i1, _i2, etc.).  


Finally, the Function constructor is used to create a function with our generated code as the body and a single argument, \(S_{in}\) .  


If we feed the template compiler the example template, it will spit out a function like this (whitespace added):  


function(\$in) { var _out = '; _out += \$in.title; _out += "\n==========\n\nItems on today's list:\n"; for (var _i1 = 0, _a1 = \$in.items; _i1 < _a1.length; ++_i1) { var item = _a1[_i1]; _out += "\n *"; _out += item.name; if (item.note) { _out += " (Note: "; _out += item.note; _out += ") " } return _out; }  


We could make that code cleaner by adding some intelligence to the compiler (for example, it could combine subsequent \(+ =\) statements to simply use \(+\) ), but you can see how it expresses the steps needed to instantiate the template.  


With a few extensions, such as the option to escape the inserted strings for your output format of choice (HTML, for example), and some error checking, this code can be built into a practical templating engine.  


## Speed  


It is always possible to interpret a domain- specific language on demand. But just as compilers tend to run programs faster than interpreters, precompiling a template leads to faster instantiation than interpreting it from its source every time it is instantiated.


--- Page 31 ---

If we forget for a second that the templating language contains JavaScript code, it would be possible to do a form of compilation without new Function—we could parse the template, and build up a data structure that allows us to instantiate it quickly with little repeated work. But it'd take a lot of effort to come close to the speed of the preceding approach that way.  


The JavaScript compiler is much more powerful (and has more direct access to the machine) than our puny compiler, so by first translating to JavaScript and then handing off the rest of the work to its more advanced peer, we can get good results with very little work.  


This idea of building on top of a compiler for another language in order to run your own language or notation is widely applicable. The various compile- to- JavaScript languages make use of it. But it also works well on a smaller scale, such as for writing a tiny compiler for a simple language to solve a very specific problem.  


## Mixing Languages  


Let's look a bit more at the fact that the templates in the toy templating language contain JavaScript code. They are, in a way, JavaScript programs with a syntactic extension that optimizes them for text expansion.  


Whether this is a good idea is a question that can be answered in several ways. If you don't trust the source of your templates, or you want to expand the templates in an environment that doesn't run JavaScript, then it is definitely a bad idea. The authors of the templates can inject arbitrary code into your program, and expanding these templates in, for example, a Ruby program would be awkward.  


But we do get the full expressive power of a real programming language in our templates. The alternative would be to define a simple expression language as part of the templating language, parse that, and either interpret it during expansion or convert it to the output language (JavaScript, in our case). This approach has its own problems, though. It's more work, obviously. But it is also hard to find a balance between offering enough features to allow people to do what they need to do without the language becoming huge and complex.  


We already know JavaScript, so if we wanted, in the example template, to render only items whose category property contains the string important, we could simply type #if /bimportant\b/.test(item.category)#. If we had to express that in a sublanguage, we'd either be out of luck if the language didn't have string search, or need to first spend 10 minutes digging through documentation to figure out how to express string search in the language.  


(Tangentially related is the argument that templating languages should be weak because they should contain presentation logic only. My take on that is that, firstly,


--- Page 32 ---

presentation logic can get quite complicated, and secondly, taking away my hammer to ensure that I don't use it on screws is a lousy way of enforcing good style.)  


A tricky issue that comes up when you're mixing languages is "hygiene." The generated code and the code that appeared in the template both run in the same scope. Thus, there is a danger that the two sources of code will disagree on what a certain variable name refers to. The toy template compiler generates variables like _a3 to avoid accidentally clashing with variables from the included code. This mostly works, but is of course far from perfect (#for _a1 in [1, 2, 3]# causes a clash). You could use more obscure variable names (_\\$\\_o_0_a3) to further reduce the chance of clashes, but it'll never be elegant. Languages that use this kind of metaprogramming more intensively have mechanisms to cope with these kinds of problems. JavaScript doesn't, but because its metaprogramming support is so minimal, that's usually not a problem.  


## Dependencies and Scopes  


Since the toy template compiler used new Function to evaluate its code, that code will only be able to see the global scope.  


What if the code that sits in the template needs access to, for example, a date formatting function? Or what if the generated part of the code needs an HTML escaping function to escape the dynamic parts of the output? You could put them in the global scope, but if you're using modern, disciplined scoping in the style of CommonJS (Node.js) or RequireJS modules, that would be unfortunate.  


The key to a workable solution to this problem is that, though we can't control what the generated function itself closes over, we can wrap our result function in an additional function, and thus inject stuff for it to close over.  


Here's a crude utility that does this:  


function newFunctionWith(env, args, body) {  var code = "";  for (var prop in env)  code += "var " + prop + " = \$env." + prop + ";";  code += "return function(" + args + ") {" + body + "}";  return new Function("\$env", code)(env);  }  console.log(newFunctionWith({x: 10}, "y", "return x + y;")(20));  // → 30  


Given an object mapping variables to values, an argument list string, and a function body string, this helper acts like new Function(args, body), except that it makes sure that all the properties in the env object are visible as closed- over variables to the body of the function.


--- Page 33 ---

It does this by generating a wrapping function that unpacks its argument into local variables, and then, immediately after evaluating this function, calling it. For simple values like integers, it could also have inserted the string form of the value directly into the wrapping function (var \(\texttt{x} = 10\) ). However, that doesn't work for complex values, so we need to pass the environment object to the evaluated code, allowing it to extract the actual values from that object.  


Using this utility, the templating system could do something like allowing templates to declare their dependencies and require- ing those in, making the code close over them.  


## Debugging Generated Code  


Debugging generated code is rarely a pleasant experience. When you write a compiler like the one we just looked at, and try it out, you will most likely be greeted by some kind of syntax error. Details differ between JavaScript engines, but if this error has origin information at all, it'll often point to the line that did the evaluation, not to the generated code.  


So what now? Unfortunately, there's no good answer that I know of. One approach is to make your compiler function log the code before it evaluates it, autoformat it, put it in a file, and try to load it. Then, the error will at least point to the actual place where the code is broken.  


If it's not a syntax error but a logic error, this might not be necessary—you might just be able to insert console.log or debugger statements into your generated code.  


Where it gets really bad is when, as in the templating system I discussed, code from the input is mixed into the generated code. Debugging a compiler once is one thing. Getting strange, contextless exceptions whenever you make a typo in your template can ruin your whole day. For production- strength systems, you probably want serious syntax checking of your templates. There are a variety of good JavaScript parsers (written in JavaScript) available nowadays, and they can be used to properly parse the expressions or statements you expect in your template, at compile time. This also helps to determine their extent in a reliable way (a directive like #if \(\$ \mathrm{in}\) .type \(= =\) "#" # would not parse in the code shown earlier, because it doesn't understand that the second hash sign is quoted), and would make it possible to emit a meaningful error (including the template name and line offset) when nonsense is encountered.  


## Binary Pattern Matches  


The second example I want to show you largely follows the same pattern as the first: we compile a domain- specific language down to JavaScript, in order to gain both speed and expressivity.


--- Page 34 ---

There is a feature in the Erlang programming language that allows you to pattern- match against binary data by specifying a sequence of fields and, for each field, a variable name or constant. Variables will be bound to the content of the field, and constants will be compared to the content of the field in order to determine whether the pattern matches. This provides a very convenient way of checking and extracting data from binary blobs.  


Let's say we want something like this in JavaScript. Ideally, it'd look like this:  


function gifSize(bytes) {  binswitch (bytes) {  case \(< < "GIF89a"\) width:uint16 height:uint16>>:  return {width: width, height: height};  default:  throw new Error("not a GIF file");  }  


where binswitch is like switch, except that it matches a series of fields in the given chunk of binary data (a typed array, presumably). This pattern would mean "first the bytes corresponding to the string "GIF89a", then a two- byte unsigned integer, which is bound to width, and finally another unsigned integer bound to height." Patterns that bind variables like that are found in many modern programming languages, and are a very pleasant feature.  


If you're willing to do heavyweight full- file preprocessing, you could write your own JavaScript dialect in which this code is valid. But in this chapter, we're looking for lightweight tricks, not alternative languages. We need to find some kind of operator that gets us close enough to this goal, but can be expressed in the existing syntax of the language.  


Here's what I came up with:  


var pngHead \(=\) binMatch("\\x89PNG\\r\\n\x1a\\n':str8 _:uint4 'IHR':str4 " + "width:uint4 height:uint4 depth:uint1"); function pngSize(bytes) { var match; if (match \(=\) pngHead(bytes, 0)) return {width: match.width, height: match.height}; else throw new Error("Not a PNG file."); }  


Patterns are precompiled from strings to functions, much like in the template example. The pattern string contains any number of binding:type pairs, where type is a word like str or uint followed by a byte size, and binding can be _ (an underscore) to ignore a field, a literal (in which case the pattern matches only when the value is equal to the literal), or a field name in which to store the value.


--- Page 35 ---

The very ugly string at the start of the pattern contains the first eight bytes of the PNG header. The double backslashes are needed because the content of the string is interpreted as a string literal (again) in the generated code, so it may not contain raw newlines. After the file- identifying string, a four- byte field is found, which we ignore. Next, the string 'IHDR' announces the start of the image header, which starts with width, height, and color depth fields.  


A function produced by binMatch takes a Uint8Array and an offset integer, and returns null for failed matches and an object containing the matched values when the match succeeds. The return object will have an additional field, end, which indicates the byte offset of the end of the match.  


Here is the core of the match compiler. It is pleasantly small:  


function binMatch(spec) { var totalSize = 0, code = "", match; while (match = /^([^:]+):(\w+)(\d+)\s*/.exec(spec)) { spec = spec.slice(match[0].length); var pattern = match[1], type = match[2], size = Number(match[3]); totalSize += size; if (pattern == " ") { code += "pos += " + size + "; } else if (/\[w\$]+$/ .test(pattern)) { code += "out." + pattern + " = " + binMatch.read[type](size) + ";"; } else { code += "if (" + binMatch.read[type](size) + " != " + pattern + ") return null;"; } } code = "if (input.length - pos < " + totalSize + ") return null;" + "var out = {end: pos + " + totalSize + "};" + code + "return out"; return new Function("input, pos", code); }  


It does a (crude, non- error- checking) parse of the input string using a regular expression that matches a single pattern: type element. For wildcard (_) patterns, it simply generates code to move the offset (pos) forward. For other patterns, it uses a helper from binMatch.read (which we'll look at momentarily) to generate an expression that builds up a JavaScript value from the bytes at the current position. For literals, it generates an if that returns null when the value found doesn't match the literal.  


Finally, an extra conditional is generated at the start of the function, which verifies that there are enough bytes in the array to match the pattern, and code that initializes and returns the output object is added.  


These are the type- parsing functions needed for the example:


--- Page 36 ---

binMatch.read = { uint: function(size) { for (var exprS = [], i = 1; i <= size; ++i) exprS.push("input[pos++]" + " + Math.pow(256, size - i)); return exprS.join(" + "); }, str: function(size) { for (var exprS = [], i = 0; i < size; ++i) exprS.push("input[pos++]"); return "String.fromCharCode(" + exprS.join(", ") + "); } };  


Given a size, they return a string that contains the expression that will advance the pos variable and produce a value of the specified type. Note that uint is big- endian (network byte order). Obvious extensions would be to write a little- endian type (uintL), which we'd need when parsing our earlier GIF example, and of course signed types (int, intL).  


Further optimizations are possible. For example, we could pick literal strings and integers apart into bytes at compile time, and compare those bytes one by one instead of building up the composite value and comparing that. Or, we could first check all literals in a pattern and only then extract the output fields, so that the match does as little work as possible if it fails. This is a nice property of static metaprogramming—the static part of the input (in this case, the pattern string) gives us a rather high- level view of the desired dynamic behavior, and we can pick a compilation strategy based on that information. If you were to interpret such a pattern at runtime, there would be less room for such decisions.  


If you want to test this code out, here's a tiny HTML page that, using the code shown previously, allows you to pick a PNG file and will console.log its size:  


<!doctype html> <script src="binMatch.js"></script> <input type="file" id="file"> <script> var pngHead = binMatch("\\x89PNG\\r\\n\\x1a\\n':str8 _:uint4 " + " 'IHR':str4 width:uint4 height:uint4 depth:uint1"); document.getElementById("file").addEventListener("change", function(e) { var reader = new FileReader(); reader.addEventListener("loaded", function() { var match = pngHead(new Uint8Array(reader.result), 0); if (match) console.log("Your image is ", match.width, "x", match.height, "pixels."); else console.log("That is not a PNG image."); }); reader.readAsArrayBuffer(e.target.files[0]); }); </script>


--- Page 37 ---

The binary pattern compiler, by putting pieces of code (literals) from the input string directly in the generated code (without sanity- checking them), could, in slightly contrived situations such as building up the pattern string from user input, be used to inject code into a system. Always take a moment to consider this angle when you use eval- like constructs. For some tools, like the template compiler, giving the sublanguage the ability to run arbitrary code is part of the design. For others, like this one, it isn't, and it is a good idea to make sure they can't be used for that purpose. We could fix this by checking whether the syntax of the literals actually conforms to JavaScript literals, or by defining and parsing our own string and number syntax (which could also get rid of the double backslash problem) and not inserting any raw, unparsed code from the template at all.  


## Closing Thoughts  


There is a major convenience gap between my fantasy syntax for pattern matching and the reality of what I came up with. Instead of elegantly expressing our pattern inline, we have to build it up beforehand, in order to ensure that it is built only once—reparsing and recompiling it every time it gets run would, in a situation where the matching happens multiple times, be embarrassingly wasteful. Instead of simply binding the variables in the pattern to local variables, we have to store them in an object.  


In this case, I think that if you are doing actual binary parsing, the abstraction is helpful enough to live with the not- quite- ideal interface. But the case is representative of a wall that you hit when trying to push eval- based abstractions beyond a certain point.  


There's a pattern that works well—compiling a domain- specific language down to a piece of code. Some languages can be expressed as JSON- like composite data, rather than plain strings (for example, a decision tree modeled as nested objects).  


The awkward part lies in the interaction between the domain- specific language and the code around it. They can't be mixed, due to the requirement that the compilation happens only once, whereas the code that makes use of the domain- specific functionality will typically run many times.  


Small snippets of code with little external dependencies can be made part of the domain language. In some cases, you might even decide to include closures in your source data structure, in order to be able to access the local environment—yet even those won't be able to close over the incoming data for a specific invocation of the functionality, but only over data that has the same lifetime as the compiled artifact.  


For this reason, many domain- specific languages are better expressed using interpretation rather than compilation. jQuery is a good example of a successful interpreted domain language in JavaScript—it hacks method chaining in a way that allows for


--- Page 38 ---

succinct DOM operations. This abstraction would be completely unpractical (though probably faster) when executed as a compiled language.  


The pattern where you should consider reaching for a compiled domain- specific language is:  


- You're writing chunks of repetitive, low-density code.- Performance is important.- The code chunks can conveniently be isolated in functions.- You can think of a shorter, more elegant notation.


--- Page 39 ---

# How to Draw a Bunny  


Jacob Thornton  


This chapter is not about rendering rabbits with JavaScript.  


This chapter is about language and the difference between what it means to draw a "rabbit" and what it means to draw a "bunny."  


This chapter is not a tutorial. It's an exegesis. This chapter is at play.  


## What Is a Rabbit?  


So she was considering, in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy- chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.  


—Lewis Carroll, Down the Rabbit Hole  


A "rabbit" is an animal you might find in a field, forest, or pet shop. It is a gregarious plant- eater with a short tail and floppy ears. It is an actual rabbit existing in reality. A "rabbit" cannot talk to itself. A "rabbit" does not run late. From this point forward, when we speak of rabbits, we speak of these ordinary, everyday rabbits.  


For the purposes of this chapter, to "draw a rabbit" is to apply various drawing techniques in such a way as to render an image of a rabbit indistinguishable from the actual rabbit itself. It is to approach a level of realism on par with that of a photograph. A rabbit drawing is strictly referential. It strives to be a copy.  


Drawing a rabbit is mechanical and spec- based. There is a correct way to draw a rabbit and an incorrect way to draw a rabbit.


--- Page 40 ---

When you draw a rabbit, you are always drawing a very particular rabbit. Deviations from the rabbit model should be regarded as errors. The more your rabbit rendering stays on model, the better.  


## What Is a Bunny?  


After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming. It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other: he came trotting along in a great hurry, muttering to himself as he came, "Oh! the Duchess, the Duchess! Oh! won't she be savage if I've kept her waiting!"  


—Lewis Carroll, Down the Rabbit Hole  


A "bunny" is not just a young, cute rabbit.  


A bunny is a splendidly dressed abstraction. A playful resemblance that prioritizes an identity other than the rabbit. It is a symbol.  

  


There are several examples from pop culture of bunnies: Bugs Bunny, the Energizer Bunny, etc. These icons are always characters first and rabbits second (or third). Here, the rabbit identity is hijacked and subjugated to serve a new ruling identity.  


To "draw a bunny" is to play within the loose constraints of an already existing identity (the rabbit) to create something entirely new. The connotation of the word "bunny" itself invokes a lack of seriousness which serves to disarm and undermine the rigid structure of the rabbit, promoting both creative exploration and expression.


--- Page 41 ---

Consider the bunny heads of Ray Johnson (pictured above), a correspondence artist from New York.  


In January 1964, Ray Johnson signed a letter to his friend William (Bill) S. Wilson with a small picture of a bunny head next to his name. This image rapidly proliferated, primarily becoming Johnson's signature and "self portrait" as personifications of how he felt on a given day. Johnson also used the bunny head to represent other "characters" who populate his works, as well as the subject of one of his "How to draw" series.  


—Frances F.L. Beatty, Ph.D. The Ray Johnson Estate  


When you draw bunnies, their proximity to a real image of a rabbit isn't called into question. For Johnson, the bunnies ceased to be rabbits, instead becoming a vehicle for alternative expression; a means to creativity; and an exercise in play, imagination, inventiveness, and originality.  


## What Does This Have to Do with JavaScript?  


JavaScript is an expressive language.  


Expressions are what lie beyond the literal compiled logic of a program. They are what we as humans read and interpret. The expressiveness of JavaScript is a vehicle through which software developers speak. It is a way for developers to infuse their code with semantic value: different styles, dialects, and character. And this potential for linguistic play inherent in JavaScript is precisely where we begin to see "bunnies."  


To draw a rabbit in JavaScript is to copy patterns out of books and slides, to mimic specific styles from blogs, and more generally to reproduce already established forms and expressions. Alternatively, to draw a bunny here is to undertake an exercise in experimentation. It is to unearth alternative forms from within the language and then combine these forms in functional yet inventive ways.  


In drawing JavaScript bunnies, you're playing. It's fun. It challenges and evolves both your individual and the community's understanding of the language. It opens up new potential solutions to old problems, and exposes flaws in old assumptions. It establishes a personal relationship between you and the code you produce. It makes writing JavaScript a craft. An art. It makes reading software personal and purposeful. It establishes an audience for your program other than just the compiler. Intent becomes clearer. Code becomes more consistent. And you grow as a developer.  


With this in mind, consider the following conditional statement, which checks to see if a property exists; if the property doesn't exist, it calls a method to set it. Traditionally, this logic might have looked something like this:


--- Page 42 ---

if (!this.username) { this.setUsername(); }  


As an expression, this logic reads: if not a username, then set a username. However, using the logical OR operator you could express this same statement in a more minimalist way:  


this.username || this.setUsername()  


The expression: a username exists, or set a username.  


These two code blocks are functionally equivalent, yet their expressions are different. They read differently. Where the former has a sort of exactness and formality, the latter is pithy and short. Exploring these variations in expression is precisely what drawing bunnies is all about. And what's more, by using expressions in conjunction with other like expressions a developer can begin to architect an overarching voice or tone in a program.  


Let's consider a second reduced example. Imagine looking inside an array for a username. If the username is not present, you want to add the username to the array. The logic for this might be expressed as follows:  


if (users.indexOf(this.username) == - 1) { users.push(this.username) }  


This code reads: if the username has an index in the users array that is equal to - 1, then push the username into the users array.  


An alternative way to express this statement might be to make use of the bitwise NOT operator. The bitwise NOT operator inverts the bits of its operand, turning a - 1 into a 0 (or falsy). The preceding logic might then be rewritten simply as:  


\~users.indexOf(this.username) || users.push(this.username)  


The expression: the username is in the array, or add it.  


As you begin to build up these expressions into programs, a certain rhythm and time signature emerges. And as you improve as an engineer, you can begin to orchestrate different phrasings and melodies into your software as well. This establishes a consistent rhythm at the project level, which will make it much easier to flow from one piece of a program to another.  


The following is a simple function that, given x, y, w, h, and placement arguments, returns an offset object with a top and left value. It is written in a decidedly slow manner, with a very deliberate, heavy rhythm (switch > case... case... case... case... return):


--- Page 43 ---

function getOffset (x, y, w, h, placement) { var offset switch (placement) { case 'bottom': offset = { top: y + h, left: x + w/2 } break case 'top': offset = { top: y, left: x + w/2 } break case 'left': offset = { top: y + h/2, left: x } break case 'right': offset = { top: y + h/2, left: x + w } break } return offset }  


Notice the difference between this function and the following function, not in terms of computing performance (where the difference is inconsequential), but rather in pure cognitive pacing. The next function returns the same result, but with a quicker, more succinct rhythm (return > this/that, this/that, this/that):  


function getOffset (x, y, w, h, placement) { return placement == 'bottom' ? { top: y + h, left: x + w/2 } : placement == 'top' ? { top: y, left: x + w/2 } : placement == 'left' ? { top: y + h/2, left: x } : { top: y + h/2, left: x + w } }  


A third function might even exaggerate the pacing further, focusing in on the return object itself—clearly calling out expected properties “top” and “left”—but with a more complex rhythm, forking the conditions at the object's properties:  


function getOffset (x, y, w, h, placement) { return { top : placement == 'bottom' ? y + h : placement == 'top' ? y : y + h/2, left : placement == 'right' ? x + w :


--- Page 44 ---

placement == 'left' ? x : x + w/2 }  


As you've begun to see, expressions guide our reading of software. In JavaScript, the potential for this sort of variation both enables and is enabled by experimentation and play—which therefore should be championed and not discouraged.  


## With So Much Variation, Which Way Is Correct?  


Imagine sitting several adults down in a room and providing them with an actual image of a rabbit and adequate drawing supplies. Imagine asking them each to draw a rabbit.  


Depending on the group's exposure to various drawing techniques, you'd likely receive a variety of renderings, ranging from rather crude to rather capable.  


Variety here becomes a metric for the lack of experience in drawing amongst the group. Which is to say, if everyone were perfect at illustration they would each have rendered a photorealistic image, indistinguishable from the image of the rabbit; there wouldn't have been any variety at all.  


This is because to draw a rabbit is to exercise one's ability to duplicate. It is an exercise in experience and mimicry. There is a right answer, and thus, there isn't room for creativity.  


But what if you had asked the same group to draw a bunny?  


Arguably the request is at once less threatening, less rigid, and less scientific. To draw a bunny is to draw a rabbit- like thing. It is exceedingly difficult to be critical of a bunny drawing because at most it's only ever a resemblance.  


Following this, you could expect the variety in the group's images to be even more exaggerated. To draw a bunny is to celebrate and to lean on variety. Here, however, variety no longer takes a negative form. Instead, it is symptomatic of the potential for creative expression implicit in the act of drawing without bounds. It is a positive metric for inventiveness and imagination.  


To draw a bunny is to engage with variety. It serves to challenge the image of the rabbit by introducing new means of achieving likeness.  


Consider immediately invoked function expressions (IIFEs). By convention, an IIFE takes one of the two following forms:  


(function (){})( function (){)(})


--- Page 45 ---

But drawing bunnies is not about convention. Rather, it's an exercise in upsetting convention. And yet at the same time it's about positive variation—one manifestation of an expression not being absolutely superior to another. With this in mind, here are a few other ways you may write an IIFE:  


!function (){() - function (){() + function (){() - function (){() new function (){() 1,function (){() 1&function (){() var i=function (){()  


Each manifestation has its own unique qualities and advantages—some with fewer bytes, some safer for concatenation, each valid and each executable.  


## How Does This Affect the Classroom?  


Because school is limited by grades, it spends much of its time propagandizing the drawing of rabbits.  




--- Page 46 ---

If you've taken a drawing class, you've almost certainly drawn a block of wood. You've spent hours shading a piece of fruit. You've studied proportions. You've been lectured on perspective. You've been given tools to break things down to a grid. And, after a few months of intense studying, your apple does begin to look a bit more like the apple sitting in front of you.  


To be sure, this isn't a bad thing. In fact, quite the opposite. These practices give you foundational knowledge on top of which you can build more complex structures. Furthermore, you can turn the tools in on themselves and exploit them in very interesting ways. And perhaps best of all, they introduce conventions and a new language through which you can engage with your peers.  


The problem emerges when students think of these tools in absolute ways. This is the right way to do X; this is the only way to do Y. As you might imagine, this absolutism breeds arrogance, narcissism, and an environment rooted in peer opposition.  


## Is This Art? And Why Does That Matter?  


It's true to say that when you paint anything, you are also painting not only the subject, but you are painting yourself as well as the object that you are trying to record. Because painting is a dual performance. Because, for instance, if you look at a Rembrandt painting, I feel like I know very much more about Rembrandt than I do about the sitter.  


Francis Bacon, interview with David Sylvester  


Briefly consider two libraries I've contributed to this past year: Ratchet and Bootstrap.  


Functionally, the content of both libraries is as it should be. What's interesting are the undertones—or rather, the potential for the same sort of undertones you would expect to find in painting, music, or creative writing. Which is to say, the differences in style between these two projects aren't just arbitrary preferences. They're very definite, derived expressions, representative of a certain mood over time.


--- Page 47 ---

Bootstrap reads very fun, not serious—nearly every line is a joke. It's trying to provoke you. Taking shortcuts. Demanding that you reread it. Reread it again. It's very pop. Very optimistic. Forward. Playful.  


The code for Ratchet is very different. It's very conservative. It's not meant to draw attention to itself. It's very explicit. Assertive, necessary. It's easy to approach. It's a vanilla milkshake.  


Insofar as art has been characterized in terms of mimesis, expression, communication of emotion, and other such values, it follows that software, when written expressively, is also an artistic gesture. What's more, this realization reinforces our insistence on the importance of drawing bunnies inasmuch as the exercise stretches one's creative and expressive capacities, enabling the formation of opinions and development of style, while also helping to strengthen communication, exploration, and imaginative faculties in the programmer.  


Along these lines, my good friend Angus Croll has been exploring further creative manifestations of code with his great articles on literary figures writing JavaScript. In his articles, he writes several functions to return a Fibonacci series of a given length, each program in the style of a different literary figure: Hemingway, Breton, Shakespeare, Poe. The results are comedic, but the point is consistent:  


The joy of JavaScript is rooted in its lack of rigidity and the infinite possibilities that this allows for. Natural languages hold the same promise. The best authors and the best JavaScript developers are those who obsess about language, who explore and experiment with language every day and in doing so develop their own style, their own idioms, and their own expression.  


—Angus Croll, If Hemingway wrote JavaScript  


Beautiful JavaScript is an art. Reading through it should feel uniform; it should allow you to flow from expression to expression. It's not just about executing logic; it's about establishing pace and reflecting a little bit of yourself. It's about taking pride in what you create.


--- Page 48 ---

## What Does This Look Like?  

  


In 1945, Picasso released a suite of 11 lithographs entitled "Bull." In this series he deconstructs the image of the bull, from realist rendering to hyperreduced line drawing, progressively subtracting from and reimagining its form with each plate.  


What's of particular interest here is the progression. Beginning with the realistic brush drawing, Picasso bulks the form up, increasing its expression of power before dissecting it with lines of force, following the contours of its muscles and skeleton, ultimately reducing and simplifying the image into a line. This study is considered the ultimate master class in abstraction, and what's more, it's a classic example of Picasso drawing bunnies.  


This same exercise in abstraction can be applied to JavaScript.  


I had the privilege of working with Alex Maccaw during my time at Twitter. There, we had a number of conversations about interview philosophies and code challenges.  


During one of our discussions he mentioned that he had always asked the same introductory interview question during phone screens—and since then, I have adopted it as my first question as well.


--- Page 49 ---

The question goes, given the following condition, define explode:  


if ('alex'.explode() == 'a l e x') interview.nextQuestion() else interview.terminate()  


There are a number of ways to answer this question. Let's begin with the most verbose:  


String.prototype.explode = function () { var i var result = ' for (i = 0; i < this.length; i++) { result = result + this[i] if (i < result.length - 1) { result = result + ' } } return result }  


This block is swollen and distended, yet deliberate. There's nothing clever. It's by the book. And it's easily the most common response to the question.  


Simply put, we declare variables i and result, iterating over the string's value, pushing its characters to result and conditionally adding a space between each character until eventually we return.  


Fine. But now let's try something a bit cleverer:  


String.prototype.explode = function (f,a,t) { for (f = a = 't = this.length; a++ < t;) { f += this[a- 1] a < t && (f += ' ') } return f //allow @fat }  


If you write code like this, people will hate you. Without question. It's playful. It looks to trick you. To trick the language. It assaults the reader. It's concerned with everything, except its own logic. It's vain. But it's beautiful (to me).  


In this block, we're scoping the variables to the function by including them as pseudogramments (which spell my Twitter handle). The for loop saves some characters by setting both f and a to new string, and the a is then coerced in the next expression to 1 by the ++ increment operator, just in time to be used in the equality comparison. On the next line the program subtracts 1 from a before indexing the string to make up for starting the loop at 1 (rather than 0). It then conditionally adds a space to the end, before completing the loop and returning the result.


--- Page 50 ---

The next iteration of the solution is by far the simplest, leaning heavily on the language's tool belt. Perhaps surprisingly, this response is actually very uncommon to receive in real interviews:  


String.prototype.explode = function () { return this.split('').join('') }  


This solution is about getting to the next question. It's clever, but not overly so. It's blunt. It's mature. If the previous solution was crass, this one is urbane.  


And finally, the absolute simplest:  


String.prototype.explode = function (/*smart a$$*/){ return 'a l e x' }  


Which I've never gotten.  


## What Did I Just Read?  


If drawing rabbits in JavaScript means copying patterns out of books or mimicking specific styles from blogs, drawing bunnies is about experimentation and creative expression.  


To draw a bunny is to pervert the conventions of the language. To draw your breath or to get it all out as fast as possible. It's an exercise in discovering and pushing the bounds of your understanding of the language. It's about reinforcing and challenging JavaScript as a craft.  


In drawing JavaScript bunnies, you're always at play. And you're getting better.
