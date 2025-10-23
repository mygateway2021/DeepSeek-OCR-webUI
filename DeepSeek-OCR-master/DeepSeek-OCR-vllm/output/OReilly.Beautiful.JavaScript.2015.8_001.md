--- Page 1 ---

Beautiful JavaScript  


Leading Programmers Explain How They Think  


Anton Kovalyov  




--- Page 2 ---

# Beautiful JavaScript  


JavaScript is arguably the most polarizing and misunderstood programming language in the world. Many have attempted to replace it as the language of the Web, but JavaScript has survived, evolved, and thrived. Why did a language created in such a hurry succeed where others failed?  


This guide gives you a rare glimpse into JavaScript from people intimately familiar with it. Chapters contributed by domain experts such as Jacob Thornton, Ariya Hidayat, and Sara Chipps reveal what they love about their favorite language—whether it's turning the most feared features into useful tools, or how JavaScript can be used for self- expression.  


# Contributors include:  


Jonathan Barronville Daryl Koopersmith Jenn Schiffer Sara Chipps Anton Kovalyov Jacob Thornton Angus Croll Rebecca Murphey Ben Vinegar Marijn Haverbeke Daniel Pupius Rick Waldron Ariya Hidayat Graeme Roberts Nicholas Zakas  


## About the editor:  


About the editor: Anton Kovalyov is a software engineer at Medium, creator of JSHint, and coauthor of Third- Party JavaScript (Manning).  


"Reading this book is like sitting down with some of the masters of JavaScript for lunch and hearing them talk about what's on their mind at the moment. You'll leave with a new appreciation for the language, and with something you can use to make your next project better."  


- Dave Camp, Director of Engineering, Firefox  

  

  


Twitter: @oreillymedia facebook.com/oreilly oreilly.com


--- Page 3 ---

# Beautiful JavaScript 


Edited by Anton Kovalyov


--- Page 4 ---

## Beautiful JavaScript  


edited by Anton Kovalyov  


Copyright © 2015 Anton Kovalyov. All rights reserved.  


Printed in the United States of America.  


Published by O'Reilly Media, Inc., 1005 Gravenstein Highway North, Sebastopol, CA 95472.  


O'Reilly books may be purchased for educational, business, or sales promotional use. Online editions are also available for most titles (http://safaribooksonline.com). For more information, contact our corporate/institutional sales department: 800- 998- 9938 or corporate@oreilly.com.  


Acquisitions Editor: Simon St. Laurent  Editor: Allyson MacDonald  Production Editor: Matthew Hacker  Copyeditor: Rachel Head  Proofreader: Rachel Monaghan  


Indexer: WordCo Indexing Services, Inc.  Interior Designer: David Futato  Cover Designer: Susan Thompson  Illustrator: Rebecca Demarest  


August 2015: First Edition  


## Revision History for the First Edition  


2015- 08- 07: First Release  


See http://oreilly.com/catalog/errata.csp?isbn=9781449370756 for release details.  


The O'Reilly logo is a registered trademark of O'Reilly Media, Inc. Beautiful JavaScript, the cover image, and related trade dress are trademarks of O'Reilly Media, Inc.  


While the publisher and the authors have used good faith efforts to ensure that the information and instructions contained in this work are accurate, the publisher and the authors disclaim all responsibility for errors or omissions, including without limitation responsibility for damages resulting from the use of or reliance on this work. Use of the information and instructions contained in this work is at your own risk. If any code samples or other technology this work contains or describes is subject to open source licenses or the intellectual property rights of others, it is your responsibility to ensure that your use thereof complies with such licenses and/or rights.


--- Page 5 ---

# TABLE OF CONTENTS  


Preface. vii  


1 Beautiful Mixins. 1  


Classical Inheritance 1  


Prototypes 2  


Mixins 3  


The Basics 4  


The Use Case 4  


Classic Mixins 5  


The extend Function 6  


Functional Mixins 7  


Adding Options 8  


Adding Caching 9  


Advice 10  


Wrapup 11  


2 eval and Domain- Specific Languages. 13  


What About "eval Is Evil"? 13  


History and Interface 14  


Performance 15  


Common Uses 16  


A Template Compiler 16  


Speed 18  


Mixing Languages 19  


Dependencies and Scopes 20  


Debugging Generated Code 21  


Binary Pattern Matches 21  


Closing Thoughts 25  


3 How to Draw a Bunny. 27  


What Is a Rabbit? 27


--- Page 6 ---

What Is a Bunny? 28  What Does This Have to Do with JavaScript? 29  With So Much Variation, Which Way Is Correct? 32  How Does This Affect the Classroom? 33  Is This Art? And Why Does That Matter? 34  What Does This Look Like? 36  What Did I Just Read? 38  


# 4 Too Much Rope, or JavaScript for Teams. 39  


Know Your Audience 39  Stupid Good 40  Keep It Classy 41  Style Rules 43  Evolution of Code 44  Conclusion 44  


# 5 Hacking JavaScript Constructors for Model Harmony. 47  


Doppelgangers 48  Miniature Models of Factories 50  Constructor Identity Crisis 51  Making It Scale 52  Conclusion 54  


# 6 One World, One Language. 57  


An Imperative, Dynamic Proposal 58  The Paradox of Choice 60  Globalcommunicationscript 60  


# 7 Math Expression Parser and Evaluator. 61  


Lexical Analysis and Tokens 61  Syntax Parser and Syntax Tree 66  Tree Walker and Expression Evaluator 72  Final Words 76  


# 8 Evolution. 77  


Backbone 79


--- Page 7 ---

New Possibilities 79  


9 Error Handling. 83  


Assume Your Code Will Fail 83  


Throwing Errors 84  


When to Throw Errors 86  


Types of Errors 86  


Custom Errors 88  


Handling Errors 89  


Global Error Handling in Browsers 91  


Global Error Handling in Node.js 92  


Summary 93  


10 The Node.js Event Loop. 95  


Event- Driven Programming 95  


Asynchronous, Nonblocking I/O 97  


Concurrency 99  


Adding Tasks to the Event Loop 99  


11 JavaScript Is. 101  


JavaScript Is Dynamic 101  


JavaScript Can Be Static 102  


JavaScript Is Functional 102  


JavaScript Does Everything 103  


12 Coding Beyond Logic. 105  


0. The Basement 105  


1. Quine's Paradox 105  


2. The Conjecture 110  


3. Peer Review 112  


13 JavaScript Is Cutieful. 115  


All This Loose Beauty 115  


The Absurdity of Dalí 115  


Dalí's JavaScript 116  


Is This Beauty Just Ugly? 116  


An Unfortunate Necessity 116  


The Beauty Is in the Madness 116


--- Page 8 ---

Let's Have a Wee Look at map 116Hello, thisArg 117Okay! So That's a Bunch of Stuff I Already Knew About [] .map—Now What? 117calling All Cars 117Number 117Now I Know Everything 118Wild 118  


14 Functional JavaScript 119Functional Programming 119Functional JavaScript 121Objects 126Now What? 127  


15 Progress 129  


Index 147


--- Page 9 ---

## Preface  


FUNCTIONS ARE FIRST- CLASS CITIZENS, SYNTAX RESEMBLES JAVA, INHERITANCE is prototypal, and \((+^{\prime \prime \prime})\) equals zero. This is JavaScript, arguably the most polarizing and misunderstood programming language in the world. It was created in 10 days and had a lot of warts and rough edges. Since then, there have been many attempts to replace it as the language of the Web. And yet, the language and the ecosystem around it are thriving. JavaScript is the most popular language in the world—and the only true language of the web platform. What made JavaScript special? Why did a language that was created in such a hurry succeed where others failed?  


I believe the reasons why JavaScript (and the Web in general) survived lie in its omnipresence—it's practically impossible to find a personal computer that doesn't have some sort of JavaScript interpreter—and its ability to gain from disorder, to use its stressors for self- improvement.  


JavaScript, like no other language, brought all kinds of different people to the platform. Anyone with a text editor and a web browser could get started with JavaScript, and many did. Its expressiveness and limited standard library prompted those people to experiment with the language and push it to its limits. People were not only making websites and applications; they were writing libraries and creating programming languages that could be compiled back into JavaScript. Those libraries competed with each other, and their approaches to solving problems often contradicted one another. The JavaScript ecosystem was a mess, but it was bursting with life.


--- Page 10 ---

Many of those libraries and languages are now forgotten. Their best ideas, however—the ones that proved themselves and stood the test of time—were absorbed into the language. They made their way into JavaScript's standard library and its syntax. They made the language better.  


Then there were languages and technologies that were designed to replace JavaScript. But instead of succeeding, they unwillingly became its necessary stressors. Every time a new language or system to replace JavaScript emerged, browser vendors would find a way to make it faster, more powerful, and more robust. Once again, good ideas were absorbed into newer versions of the language, and the bad ones were discarded. These competing technologies didn't replace JavaScript; instead, they made it better.  


Today, JavaScript is unbelievably popular. Will it last? I don't know. I cannot predict whether it will still be popular 5 or 10 years from now, but it doesn't really matter. For me, JavaScript will always be a great example of a language that survived not despite its flaws but because of them, and a language that brought people of so many different backgrounds into this wonderful world of computer programming.  


## About This Book  


This book was written by people who are intimately familiar with the language. Each and every person who contributed a chapter is an expert in his or her domain. The authors highlight different sides of JavaScript, some of which you can discover only by writing lots of code, experimenting and making mistakes. As you make your way through this book, you'll get to see what JavaScript movers and shakers love about their favorite language.  


You'll also learn a lot. I did. But do not mistake this book for a JavaScript tutorial, because it is much bigger than that. There are chapters that challenge the conventional wisdom and show how even the most feared features can be used as helpful tools. Some authors show that JavaScript can be a tool for self- expression and a form of art, while others share the wisdom of using JavaScript in codebases with hundreds of contributors. Some authors share personal stories, while others look into the future.  


There's no common pattern that goes from one chapter to another—there's even a purely satirical chapter. This is intentional. I tried to give the authors as much freedom as possible to see what they would come up with, and they came up with something incredible. They came up with a book that resembles JavaScript itself, where each chapter is a reflection of its author.


--- Page 11 ---

## Conventions Used in This Book  


The following typographical conventions are used in this book:  


Italic  


Indicates new terms, URLs, email addresses, filenames, and file extensions.  


Constant width  


Used for program listings, as well as within paragraphs to refer to program elements such as variable or function names, databases, data types, environment variables, statements, and keywords.  


TIP This element signifies a tip or suggestion.  


NOTE  


This element signifies a general note.  


## Using Code Examples  


Supplemental material (code examples, exercises, etc.) is available for download at https://github.com/oreillymedia/beautiful_javascript.  


This book is here to help you get your job done. In general, if example code is offered with this book, you may use it in your programs and documentation. You do not need to contact us for permission unless you're reproducing a significant portion of the code. For example, writing a program that uses several chunks of code from this book does not require permission. Selling or distributing a CD- ROM of examples from O'Reilly books does require permission. Answering a question by citing this book and quoting example code does not require permission. Incorporating a significant amount of example code from this book into your product's documentation does require permission.  


We appreciate, but do not require, attribution. An attribution usually includes the title, author, publisher, and ISBN. For example: "Beautiful JavaScript, edited by Anton Kovalyov (O'Reilly). Copyright 2015 Anton Kovalyov, 978- 1- 449- 37075- 6."  


If you feel your use of code examples falls outside fair use or the permission given above, feel free to contact us at permissions@oreilly.com.


--- Page 12 ---

## Safari® Books Online  


Safari Books Online is an on- demand digital library that delivers expert content in both book and video form from the world's leading authors in technology and business.  


Technology professionals, software developers, web designers, and business and creative professionals use Safari Books Online as their primary resource for research, problem solving, learning, and certification training.  


Safari Books Online offers a range of plans and pricing for enterprise, government, education, and individuals.  


Members have access to thousands of books, training videos, and prepublication manuscripts in one fully searchable database from publishers like O'Reilly Media, Prentice Hall Professional, Addison- Wesley Professional, Microsoft Press, Sams, Que, Peachpit Press, Focal Press, Cisco Press, John Wiley & Sons, Syngress, Morgan Kaufmann, IBM Redbooks, Packt, Adobe Press, FT Press, Apress, Manning, New Riders, McGraw- Hill, Jones & Bartlett, Course Technology, and hundreds more. For more information about Safari Books Online, please visit us online.  


## How to Contact Us  


Please address comments and questions concerning this book to the publisher:  


O'Reilly Media, Inc.  1005 Gravenstein Highway North  Sebastopol, CA 95472  800- 998- 9938 (in the United States or Canada)  707- 829- 0515 (international or local)  707- 829- 0104 (fax)  


We have a web page for this book, where we list errata, examples, and any additional information. You can access this page at http://bit.ly/beautiful_javascript.  


To comment or ask technical questions about this book, send email to bookquestions@oreilly.com.  


For more information about our books, courses, conferences, and news, see our website at http://www.oreilly.com.  


Find us on Facebook: http://facebook.com/oreilly  


Follow us on Twitter: http://twitter.com/oreillymedia  


Watch us on YouTube: http://www.youtube.com/oreillymedia


--- Page 13 ---

# CHAPTER ONE  


# Beautiful Mixins  


Angus Croll  


Developers love to create overly complex solutions to things that aren't really problems.  


—Thomas Fuchs  


In the beginning there was code, and the code was verbose, so we invented functions that the code might be reused. But after a while there were also too many functions, so we looked for a way to reuse those too. Developers often go to great lengths to apply "proper" reuse techniques to JavaScript. But sometimes when we try too hard to do the right thing, we miss the beautiful thing right in front of our eyes.  


## Classical Inheritance  


Many developers schooled in Java, \(\mathrm{C + + }\) , Objective- C, and Smalltalk arrive at JavaScript with an almost religious belief in the necessity of the class hierarchy as an organizational tool. Yet humans are not good at classification. Working backward from an abstract superclass toward real types and behaviors is unnatural and restrictive—a superclass must be created before it can be extended, yet classes closer to the root are by nature more generic and abstract and are more easily defined after we have more knowledge of their concrete subclasses. Moreover, the need to tightly couple types \(a\) priori such that one type is always defined solely in terms of another tends to lead to an overly rigid, brittle, and often ludicrous model ("Is a button a rectangle or is it a control? Tell you what, let's make Button inherit from Rectangle, and Rectangle can inherit from Control...no, wait a minute..."). If we don't get it right early on, our system is forever burdened with a flawed set of relationships—and on those rare occasions that, by chance or genius, we do get it right, anything but a minimal tree structure usually represents too complex a mental model for us to readily visualize.


--- Page 14 ---

Classical inheritance is appropriate for modeling existing, well- understood hierarchies—it's okay to unequivocally declare that a FileStream is a type of Input Stream. But if the primary motivation is function reuse (and it usually is), classical hierarchies can quickly become gnarly labyrinths of meaningless subtypes, frustrating redundancies, and unmanageable logic.  


## Prototypes  


It's questionable whether the majority of behaviors can ever be mapped to objectively "right" classifications. And indeed, the classical inheritance lobby is countered by an equally fervent band of JavaScript loyalists who proclaim that JavaScript is a prototypal, not classical, language and is deeply unsuited to any approach that includes the word class. But what does "prototypal" mean, and how do prototypes differ from classes?  


In generic programming terms, a prototype is an object that supplies base behavior to a second object. The second object can then extend this base behavior to form its own specialization. This process, also known as differential inheritance, differs from classical inheritance in that it doesn't require explicit typing (static or dynamic) or attempt to formally define one type in terms of another. While classical inheritance is planned reuse, true prototypal inheritance is opportunistic.  


In general, when working with prototypes, one typically chooses not to categorize but to exploit alikeness.  


—Antero Taivalsaari, Nokia Research Center  


In JavaScript, every object references a prototype object from which it can inherit properties. JavaScript prototypes are great instruments for reuse: a single prototype instance can define properties for an infinite number of dependent instances. Prototypes may also inherit from other prototypes, thus forming prototype chains.  


So far, so good. But, with a view to emulating Java, JavaScript tied the prototype property to the constructor. As a consequence, more often than not, multilevel object inheritance is achieved by chaining constructor- prototype couples. The standard implementation of a JavaScript prototype chain is too grisly to appear in a book about beautiful JavaScript, but suffice it to say, creating a new instance of a base prototype in order to define the initial properties of its inheritor is neither graceful nor intuitive. The alternative—manually copying properties between prototypes and then meddling with the constructor property to fake real prototypal inheritance—is even less becoming.  


Syntactic awkwardness aside, constructor- prototype chaining requires upfront planning and results in structures that more closely resemble the traditional hierarchies of classical languages than a true prototypal relationship: constructors represent types


--- Page 15 ---

(classes), each type is defined as a subtype of one (and only one) supertype, and all properties are inherited via this type chain. The ES6 class keyword merely formalizes the existing semantics. Leaving aside the gnarly and distinctly unbeautiful syntax characteristic in constructor- prototype chains, traditional JavaScript is clearly less prototypal than some would claim.  


In an attempt to support less rigid, more opportunistic prototypes, the ES5 specification introduced Object.create. This method allows a prototype to be assigned to an object directly and therefore liberates JavaScript prototypes from constructors (and thus categorization) so that, in theory, an object can acquire behavior from any other arbitrary object and be free from the constraints of typecasting:  


var circle \(=\) Object.create{ area: function(){ return Math.PI \\* this.radius \\* this.radius; }, grow: function(){ this.radius++; }, shrink: function(){ this.radius- - ; } };  


Object.create accepts an optional second argument representing the object to be extended. Sadly, instead of accepting the object itself (in the form of a literal, variable, or argument), the method expects a full- blown meta property definition:  


var circle \(=\) Object.create{ /\*see above\*/ },{ radius: { writable:true, configurable:true, value: 7 } } };  


Assuming no one actually uses these unwieldy beasts in real code, all that remains is to manually assign properties to the instance after it has been created. Even then, the Object.create syntax still only enables an object to inherit the properties of a single prototype. In real scenarios, we often want to acquire behavior from multiple prototype objects: for example, a person can be an employee and a manager.  


## Mixins  


Fortunately, JavaScript offers viable alternatives to inheritance chaining. In contrast to objects in more rigidly structured languages, JavaScript objects can invoke any function property regardless of lineage. In other words, JavaScript functions don't need to


--- Page 16 ---

be inheritable to be visible—and with that simple observation, the entire justification for inheritance hierarchies collapses like a house of cards.  


The most basic approach to function reuse is manual delegation—any public function can be invoked directly via call or apply. It's a powerful and easily overlooked feature. However, aside from the verbosity of serial call or apply directives, such delegation is so convenient that, paradoxically, it sometimes actually works against structural discipline in your code—the invocation process is sufficiently ad hoc that in theory there is no need for developers to organize their code at all.  


Mixins are a good compromise: by encouraging the organization of functionality along thematic lines they offer something of the descriptive prowess of the class hierarchy, yet they are light and flexible enough to avoid the premature organization traps (and head- spinning dizziness) associated with deeply chained, single- ancestry models. Better still, mixins require minimal syntax and play very well with unchained JavaScript prototypes.  


## The Basics  


Traditionally, a mixin is a class that defines a set of functions that would otherwise be defined by a concrete entity (a person, a circle, an observer). However, mixin classes are considered abstract in that they will not themselves be instantiated—instead, their functions are copied (or borrowed) by concrete classes as a means of inheriting behavior without entering into a formal relationship with the behavior provider.  


Okay, but this is JavaScript, and we have no classes per se. This is actually a good thing because it means we can use objects (instances) instead, which offer clarity and flexibility: our mixin can be a regular object, a prototype, a function, whatever, and the mixin process becomes transparent and obvious.  


## The Use Case  


I'm going to discuss a number of mixin techniques, but all the coding examples are directed toward one use case: creating circular, oval, or rectangular buttons (something that would not be readily possible using conventional classical inheritance techniques). Here's a schematic representation: square boxes represent mixin objects, and rounded boxes represent the actual buttons.


--- Page 17 ---
  


## Classic Mixins  


Scanning the first two pages returned from a Google search for "javascript mixin," I noticed the majority of authors define the mixin object as a full- blown constructor type with its function set defined in the prototype. This could be seen as a natural progression—early mixins were classes, and this is the closest thing JavaScript has to a class. Here's a circle mixin modeled after that style:  


var Circle \(=\) function(){}; Circle.prototype \(=\) { area: function(){ return Math.PI \\* this.radius \\* this.radius; } grow: function(){ this.radius++; } shrink: function(){ this.radius- - ; } };  


In practice, however, such a heavyweight mixin is unnecessary. A simple object literal will suffice:  


var circleFns \(=\) { area: function(){ return Math.PI \\* this.radius \\* this.radius; } grow: function(){ this.radius++; } shrink: function(){ this.radius- - ; } };


--- Page 18 ---

Here's another mixin defining button behavior (for the sake of demonstration, I've substituted a simple log call for the working implementation of some function properties):  


var clickableFns = {  hover: function() {  console.log('hovering');  },  press: function() {  console.log('button pressed');  },  release: function() {  console.log('button released');  },  fire: function() {  this.action.fire();  }  


## The extend Function  


How does a mixin object get mixed into your object? By means of an extend function (sometimes known as augmentation). Usually extend simply copies (not clones) the mixin's functions into the receiving object. A quick survey reveals some minor variations in this implementation. For example, the Prototype.js framework omits a hasOwn Property check (suggesting the mixin is not expected to have enumerable properties in its prototype chain), while other versions assume you want to copy only the mixin's prototype object. Here's a version that is both safe and flexible:  


function extend(destination, source) {  for (var key in source) {  if (source.hasOwnProperty(key)) {  destination[key] = source[key];  }  }  return destination;  }  


Now let's extend a base prototype with the two mixins we created earlier to make a RoundButton.prototype:  


var RoundButton = function(radius, label) {  this.radius = radius;  this.label = label;  };  extend(RoundButton.prototype, circleFns);  extend(RoundButton.prototype, clickableFns);  var roundButton = new RoundButton(3, 'send');


--- Page 19 ---

roundButton.grow(); roundButton.fire();  


## Functional Mixins  


If the functions defined by mixins are intended solely for the use of other objects, why bother creating mixins as regular objects at all? Isn't it more intuitive to think of mixins as processes instead of objects? Here are the circle and button mixins rewritten as functions. We use the context (this) to represent the mixin's target object:  


var withCircle \(=\) function(){ this.area \(=\) function(){ return Math.PI \\* this.radius \\* this.radius; }; this.grow \(=\) function(){ this.radius++; }; this.shrink \(=\) function(){ this.radius- - ; };  


var withClickable \(=\) function(){ this.hover \(=\) function(){ console.log('hovering'); }; this.press \(=\) function(){ console.log('button pressed'); }; this.release \(=\) function(){ console.log('button released'); }; this.fire \(=\) function(){ this.action.fire(); };  


And here's our RoundButton constructor. We'll want to apply the mixins to RoundButton.prototype:  


var RoundButton \(=\) function(radius, label, action){ this.radius \(=\) radius; this.label \(=\) label; this.action \(=\) action; };  


Now the target object can simply inject itself into the functional mixin by means of Function.prototype.call, cutting out the middleman (the extend function) entirely:


--- Page 20 ---

withCircle.call(RoundButton.prototype); withClickable.call(RoundButton.prototype);  


var button1 = new RoundButton(4, 'yes!', function() {return 'you said yes!'}; button1. fire(); //'you said yes!'  


This approach feels right. Mixins as verbs instead of nouns; lightweight one- stop function shops. There are other things to like here too. The programming style is natural and concise: this always refers to the receiver of the function set instead of an abstract object we don't need and will never use; moreover, in contrast to the traditional approach, we don't have to protect against inadvertent copying of inherited properties, and (for what it's worth) functions are now cloned instead of copied.  


## Adding Options  


This functional strategy also allows mixed in behaviors to be parameterized by means of an options argument. The following example creates a withOval mixin with a custom grow and shrink factor:  


var withOval \(=\) function(options) { this.area \(=\) function() { return Math.PI \\* this. longRadius \\* this. shortRadius; }; this.ratio \(=\) function() { return this. longRadius/this. shortRadius; }; this. grow \(=\) function() { this. shortRadius \(^{+ =}\) (options.growBy/this.ratio()); this. longRadius \(^{+ =}\) options.growBy; }; this. shrink \(=\) function() { this. shortRadius \(^{- =}\) (options.shrinkBy/this.ratio()); this. longRadius \(^{- =}\) options.shrinkBy; };  


var OvalButton \(=\) function(longRadius, shortRadius, label, action) { this. longRadius \(=\) longRadius; this. shortRadius \(=\) shortRadius; this. label \(=\) label; this. action \(=\) action; };  


withButton.call(OvalButton.prototype); withOval.call(OvalButton.prototype, {growBy: 2, shrinkBy: 2});  


var button2 \(=\) new OvalButton(3, 2, 'send', function() {return 'message sent'}; button2. area(); //18.84955592153876 button2. grow(); button2. area(); //52.35987755982988 button2. fire(); //'message sent'


--- Page 21 ---

## Adding Caching  


You might be concerned that this approach creates additional performance overhead because we're redefining the same functions on every call. Bear in mind, however, that when we're applying functional mixins to prototypes, the work only needs to be done once: during the definition of the constructors. The work required for instance creation is unaffected by the mixin process, since all the behavior is preassigned to the shared prototype. This is how we support all function sharing on the twitter.com site, and it produces no noticeable latency. Moreover, it's worth noting that performing a classical mixin requires property getting as well as setting, and in fact functional mixins appear to benchmark quicker in the Chrome browser than traditional ones (although this is obviously subject to considerable variance).  


That said, it is possible to optimize functional mixins further. By forming a closure around the mixins we can cache the results of the initial definition run, and the performance improvement is impressive. Functional mixins now easily outperform classic mixins in every browser.  


Here's a version of the withRectangle mixin with added caching:  


var withRectangle \(=\) (function(){ function area(){ return this.length \\* this.width; } function grow(){ this.length++; this.width++; } function shrink(){ this.length- -, this.width- - ; } return function(){ this.area \(=\) area; this.grow \(=\) grow; this.shrink \(=\) shrink; return this; }); });  


var RectangularButton \(=\) function(length, width, label, action){ this.length \(=\) length; this.width \(=\) width; this.label \(=\) label; this.action \(=\) action; }  


withClickable.call(RectangularButton.prototype); withRectangle.call(RectangularButton.prototype);  


var button3 \(=\) new RectangularButton(4, 2, 'delete', function(){ return 'deleted'});


--- Page 22 ---

button3. area(); //8 button3. grow(); button3. area(); //15 button3. fire(); //'deleted'  


## Advice  


One danger with any kind of mixin technique is that a mixin function will accidentally overwrite a property of the target object that, coincidentally, has the same name. Twitter's Flight framework, which makes use of functional mixins, guards against clobbering by temporarily locking existing properties (using the writable meta property) during the mixin process.  


Sometimes, however, instead of generating a collision error we might want the mixin to augment the corresponding method on the target object. advice redefines a function by adding custom code before, after, or around the original implementation. The Underscore framework implements a basic function wrapper that enables advice:  


button.press \(=\) function(){ mylib.appendclass('pressed'); }; //after pressing button, reduce shadow (using underscore) button.pressWithShadow \(=\) _wrap(button.press, function(fn) { fn(); button.reduceShadow(); }  


The Flight framework takes this a stage further: now the advice object is itself a functional mixin that can be mixed into target objects to enable advice for subsequent mixins.  


Let's use this advice mixin to augment our rectangular button actions with shadow behavior. First we apply the advice mixin, followed by the two mixins we used earlier:  


withAdvice.call(RectangularButton.prototype); withClickable.call(RectangularButton.prototype); withRectangle.call(RectangularButton.prototype);  


And now the withShadow mixin that will take advantage of the advice mixin:  


var withShadow \(=\) function(){ this.after('press', function(){ console.log('shadow reduced'); }; this.after('release', function(){ console.log('shadow reset'); }; };  


withShadow.call(RectangularButton.prototype);


--- Page 23 ---

var button4 = new RectangularButton(5, 4); button4. press(); //'button pressed' 'shadow reduced' button4. release(); //'button released' 'shadow reset'  


The Flight framework sugarcoats this process. All flight components get withAdvice mixed in for free, and there's also a defineComponent method that accepts multiple mixins at a time. So, if we were using Flight we could further simplify the process (in Flight, constructor properties such as rectangle dimensions are defined as attr properties in the mixins):  


var RectangularButton = defineComponent(withClickable, withRectangle, withShadow); var button5 = new RectangularButton(3, 2); button5. press(); //'button pressed' 'shadow reduced' button5. release(); //'button released' 'shadow reset'  


With advice we can define functions on mixins without having to guess whether they're also implemented on the target object, so the mixin can be defined in isolation (perhaps by another vendor). Conversely, advice allows us to augment third- party library functions without resorting to monkey patching.  


## Wrapup  


When possible, cut with the grain. The grain tells you which direction the wood wants to be cut. If you cut against the grain, you're just making more work for yourself, and making it more likely you'll spoil the cut.  


- Charles Miller<sup>1</sup>  


As programmers, we're encouraged to believe that certain techniques are indispensable. Ever since the early 1990s, object- oriented programming has been hot, and classical inheritance has been its poster child. It's not hard to see how a developer eager to master a new language would feel under considerable pressure to fit classical inheritance under the hood.  


But peer pressure is not an agent of beautiful code, and neither is serpentine logic. When you find yourself writing Circle.prototype.constructor = Circle, ask yourself if the pattern is serving you, or you're serving the pattern. The best patterns tread lightly on your process and don't interfere with your ability to use the full power of the language.  


By repeatedly defining an object solely in terms of another, classical inheritance establishes a series of tight couplings that glue the hierarchy together in an orgy of mutual dependency. Mixins, in contrast, are extremely agile and make very few organizational


--- Page 24 ---

demands on your codebase—mixins can be created at will, whenever a cluster of common, shareable behavior is identified, and all objects can access a mixin's functionality regardless of their role within the overall model. Mixin relationships are entirely ad hoc: any combination of mixins can be applied to any object, and objects can have any number of mixins applied to them. Here, at last, is the opportunistic reuse that prototypal inheritance promised us.


--- Page 25 ---

# eval and Domain-Specific Languages  


Marijn Haverbeke  


eval is a language construct that takes a string and executes it as code.  


This means that in a language with an eval construct, the code that is being executed can come not just from input files, but also from the running code itself.  


There are several reasons why this is interesting and useful. In this chapter, I will explore the degree to which JavaScript's eval can be used to create simple language- based abstractions.  


## What About "eval Is Evil"?  


I know that some of my readers, at the mention of the word eval, are feeling the adrenaline shoot into their veins, and hearing the solemn voice of a certain bearded JavaScript evangelist boom in the back of their heads. "eval is evil!" this voice proclaims.  


I've never found absolute moral judgments very applicable in engineering. But if you do, and don't want to reevaluate your faith, feel free to skip this chapter.  


Practically speaking, there are a number of problematic issues that come up when eval is used. Its semantics are confusing and error- prone, and its impact on performance is not always obvious. I'm going to approach it as a tool, and try to clarify and study these issues, in order to help you use the tool effectively.
