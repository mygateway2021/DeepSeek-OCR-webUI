--- Page 51 ---

# Too Much Rope, or JavaScript for Teams  


Daniel Pupius  


Beauty is power and elegance, right action, form fitting function, intelligence, and reasonability.  


—Kim Stanley Robinson, Red Mars  


JavaScript is a flexible language. In fact, this entire book is a testament to its expressiveness and dynamism. Within these pages you'll hear stories of how to bend the language to your will, descriptions of how to use it to experiment and play, and suggestions for seemingly contradictory ways to write it.  


My job is to tell a more cautionary tale.  


I'm here to ask the question: what does it mean to write JavaScript in a team? How do you maintain sanity with 5, 10, 100 people committing to the same codebase? How do you make sure new team members can orient themselves quickly? How do you keep things DRY without forcing broken abstractions?  


## Know Your Audience  


In 2005 I joined the Gmail team in sunny Mountain View, California. The team was building what many considered at the time to be the pinnacle of web applications. They were awesomely smart and talented, but across Google, JavaScript wasn't considered a "real programming language"—you engineered backends, you didn't engineer web UIs—and this mentality affected how they thought about the code.  


Furthermore, even though the language was 10 years old, JavaScript engines were still limited: they were designed for basic form validation, not building applications. Gmail was starting to hit performance bottlenecks. To get around these limitations much of


--- Page 52 ---

the application was implemented as global functions, anything requiring a dot lookup was avoided, sparse arrays were used in place of templates, and string concatenation was a no- no.  


The team was writing first and foremost for the JavaScript engine, not for themselves or others. This led to a codebase that was hard to follow, inconsistent, and sprawling.  


Instead of optimizing by hand, we transitioned to a world where code was written for humans and the machine did the optimizations. This wasn't a new language, mind you—it was important that the raw code be valid JavaScript, for ease of understanding, testing, and interoperability. Using the precursor to the Closure Compiler, we developed optimization passes that would collapse namespaces, optimize strings, inline functions, and remove dead code. This is work much better suited to a machine, and it allowed the raw code to be more readable and more maintainable.  


TIP Lesson 1: Code for one another, and use tools to perform mechanical optimizations.  


## Stupid Good  


As the old adage goes, debugging is harder than writing code, so if you write the cleverest code you can, you'll never be clever enough to debug it.  


It can be fun to come up with obscure and arcane ways of solving problems, especially since JavaScript gives you so much flexibility. But save it for personal projects and JavaScript puzzlers.  


When working in a team you need to write code that everyone is going to understand. Some parts of the codebase may go unseen for months, until a day comes when you need to debug a production issue. Or perhaps you have a new hire with little JavaScript experience. In these types of situation, keeping code simple and easy to understand will be better for everyone. You don't want to spend time decoding some bizarro, magical incantation at two in the morning while debugging production issues.  


Consider the following:  


var el = document.querySelector('.profile'); el.classListList['add','remove'][+el.classListList.contains('on')]]('on');  


And an alternative way of expressing the same behavior:  


var el = document.querySelector('.profile'); if (el.classListList.contains('on')) el.classListList.remove('on'); else el.classListList.add('on');


--- Page 53 ---

Saying that the second snippet is better than the first may seem in conflict with the concept that “succinctness = power.” But I believe there is a disconnect that stems from the common synonyms for succinct: compact, brief.  


I prefer terse as a synonym:  


using few words, devoid of superfluity, smoothly elegant  


The first snippet is more compact than the second snippet, but it is denser and actually includes more symbols. When reading the first snippet you have to know how coercion rules apply when using a numeric operator on a Boolean, you have to know that methods can be invoked using subscript notation, and you have to notice that square brackets are used for both defining an array literal and method lookup.  


The second snippet, while longer, actually has less syntax for the reader to process. Furthermore, it reads like English: “If the element’s class list contains ‘on’, then remove ‘on’ from the class list; otherwise, add ‘on’ to the class list.”  


All that said, an even better solution would be to abstract this functionality and have the very simple, readable, and succinct:  


toggleCssClass(document.querySelector('.profile'), 'on');  


TIP Lesson 2: Keep it simple; compactness \(! =\) succinctness.  


## Keep It Classy  


When I’m talking with “proper programmers,” they often complain about how terrible JavaScript is. I usually respond that JavaScript is misunderstood, and that one of the main issues is that it gives you too much rope—so inevitably you end up hanging yourself.  


There were certainly questionable design decisions in the language, and it is true that the early engines were quite terrible, but many of the problems that occur as JavaScript codebases scale can be solved with pretty standard computer science best practices. A lot of it comes down to code organization and encapsulation.  


Unfortunately, until we finally get ES6 we have no standard module system, no standard packaging mechanisms, and a prototypal inheritance model that confuses a lot of people and begets a million different class libraries.  


While JavaScript’s prototypal inheritance allows instance- based inheritance, I generally suggest when working in a team that you simulate classical inheritance as much as possible, while still utilizing the prototype chain. Let’s consider an example:


--- Page 54 ---

var log = console.log.bind(console); var bob = { money: 100, toString: function() { return ' \(\) + this.money \} ; var billy = Object.create(bob);  


log('bob:' + bob, 'billy:' + billy); // bob: \(\) 100\(billy:\) \ \(100\) bob.money \(= 150\) log('bob:' + bob, 'billy:' + billy); // bob: \(\) 150\(billy:\) \ \(150\) billy.money \(= 50\) log('bob:' + bob, 'billy:' + billy); // bob: \(\) 150\(billy:\) \$50\(delete billy.money; log('bob:' + bob, 'billy:' + billy); // bob:\) \ \(150\) billy: \(\) 150\$  


In this example, billy inherits from bob. What that means in practice is that billy. pro totype \(=\) bob, and nonmatching property lookups on billy will delegate to bob. In other words, to begin with billy's \(\) 100\(is bob's\) \ \(100\) ; billy isn't a copy of bob. Then, when billy gets his own money, it essentially overrides the property that was being inherited from bob. Deleting billy's money doesn't set it to undefined; instead, bob's money becomes billy's again.  


This can be rather confusing to newcomers. In fact, developers can go a long time without ever knowing precisely how prototypes work. So, if you use a model that simulates classical inheritance, it increases the chances that people on your team will get on board quickly and allows them to be productive without necessarily needing to understand the details of the language.  


Both the Closure library's goog.inherits and Node.js's util.inherits make it easy to write class- like structures while still relying on the prototype for wiring:  


function Bank(initialMoney) { EventEmitter.call(this); this.money \(=\) money; } util.inherits(Bank, EventEmitter); Bank.prototype.widthraw \(=\) function (amount) { if (amount \(< =\) this.money) { this.money \(= =\) amount; this.emit('balance_changed', this.money); // inherited return true; } else { return false; } }  


This looks very similar to inheritance in other languages. Bank inherits from EventEmit ter; the superclass's constructor is called in the context of the new instance; util.inher


--- Page 55 ---

its wires up the prototype chain just like we saw with bob and billy earlier; and then the property lookup for emit falls to the EventEmitter "class."  


A suggested exercise for the reader is to create instances of a class without using the new keyword.  


TIP Lesson 3: Just because you can doesn't mean you should.  


TIP Lesson 4: Utilize familiar paradigms and patterns.  


## Style Rules  


The need for consistent style as codebases and teams grow is nothing unique to JavaScript. However, where many languages are opinionated about coding style, JavaScript is lenient and forgiving. This means it's all the more important to define a set of rules the team should stick to.  


Good style is subjective and can be difficult to define, but there are many cases where certain style choices are quantifiably better than others. In the cases where there isn't a quantifiable difference, there is still value in making an arbitrary choice one way or the other.  


TIP Style guides provide a common vocabulary so people can concentrate on what you're saying instead of how you're saying it.  


A good style guide should set out rules for code layout, indentation, whitespace, capitalization, naming, and comments. It is also good to create usage guides that explain best practices and provide guidance on how to use common APIs. Importantly, these guides should explain why a rule exists; over time you will want to reevaluate the rules and should avoid them becoming cargo cults.  


Style guides should be enforced by a linter and if possible coupled with a formatter to remove the mechanical steps of adhering to the guide. You don't want to waste cycles correcting style nits in code reviews.  


The ultimate goal is to have all code look like it was written by the same person.  


TIP Lesson 5: Consistency is king.


--- Page 56 ---

## Evolution of Code  


When I was first working on Google Closure there was no simple utility for making XMLHttpRequests; everything was rolled up in large, application- specific request utilities.  


So, in my naivete XhrLite was born.  


XhrLite became popular- - no one wants to use a "heavy" implementation- - but its users kept finding features that were missing. Over time small patches were submitted, and XhrLite accumulated support for form encoded data, JSON decoding, XSSI handling, headers, and more- - even fixes for obscure bugs in FF3.5 web workers.  


Needless to say, the irony of "XhrLite" becoming a distinctly heavy behemoth was not lost, and eventually it was renamed "Xhrlo." The API, however, remained bloated and cumbersome.  


TIP Small changes- - reasonable in isolation- - evolve into a system that no one would ever design if given a blank canvas.  


Evolutionary complexity is almost a force of nature in software development, but it has always seemed more pronounced with JavaScript. One of the strengths that helped spur JavaScript's popularity is that you can get up and running quickly. Whether you're creating a simple web app or a Node.js server, a minimal dev environment and a few lines of code yields something functional. This is great when you're learning, or prototyping, but can lead to fragile foundations for a growing team.  


You start out with some simple HTML and CSS. Perhaps you add some event handlers using jQuery. You add some XHRs, maybe you even start to use pushState. Before long you have an actual single- page application, something you never intended at first. Performance starts to suffer, there are weird race conditions, your code is littered with setTimeouts, there are hard- to- track- down memory leaks...you start wondering if a traditional web page would be better. You have the duck- billed platypus of applications.  


TIP Lesson 6: Lay good foundations. Be mindful of evolutionary complexity.  


## Conclusion  


JavaScript's beauty is in its pervasiveness, its flexibility, and its accessibility. But beauty is also contextual. What started as a "scripting language" is now used by hundred- plus- person teams and forms the building blocks of billion- dollar products. In such sit


--- Page 57 ---

uations you can't write code in the same way you would hacking up a one- person website. So...  


1. Code for one another, and use tools to perform mechanical optimizations.  


2. Keep it simple; compactness \(! =\) succinctness.  


3. Just because you can doesn't mean you should.  


4. Utilize familiar paradigms and patterns.  


5. Consistency is king.  


6. Lay good foundations. Be mindful of evolutionary complexity.


--- Page 58 ---

# 1


--- Page 59 ---

# Hacking JavaScript Constructors for Model Harmony  


Ben Vinegar  


JavaScript MVC—or MVW (Model, View, "Whatever")—frameworks come in many flavors, shapes, and sizes. But by virtue of their namesake, they all provide developers with a fundamental component: models, which "model" the data associated with the application. In client- side web apps, they typically represent a database- backed object.  


Last year at Disqus, we rewrote our embedded client- side application in Backbone, a minimal MVC framework. Backbone is often criticized for having an unsophisticated "view" layer, but one thing it does particularly well is managing models.  


Defining a new model in Backbone looks like this:  


var User \(=\) Backbone.Model.extend({ defaults: { username: ' firstname: ' , lastName: ' } , idAttribute: ' username' , fullName: function () { return this.get(' firstName') + this.get(' lastName') ; } });  


Here's some sample code that initializes a new model, and demonstrates how that model instance might be used in an application:


--- Page 60 ---

var user \(=\) new User({ username: 'john_doe', firstName: 'John', lastName: 'Doe' }); user.fullName(); // John Doe user.set('firstName', 'Bill'); user.save(); // PUTs changes to server endpoint  


These are simple examples, but client- side models can be very powerful, and they are typically—ahem—the backbone of any nontrivial MVC app.  


Additionally, Backbone provides what are called “collection” classes, which help developers easily manipulate common sets of model instances. You can think of them as superpowered arrays, loaded with helpful utility functions:  


var UserCollection \(=\) Backbone.Collection.extend({ model: User, url: '/users' });  


var users \(=\) new UserCollection();  


users.fetch(); // Fetches user records via HTTP  


var johndoe \(=\) users.get('john_doe'); // Find by primary idAttribute  


Not all MVC frameworks implement a Collection class exactly like Backbone does. For example, Ember.js defines a CollectionView class, which similarly maintains a set of common models, but tied to a DOM representation. API differences aside, it's clear that developers commonly manipulate and render sets of objects, and frameworks provide different facilities for doing so.  


## Doppelgangers  


When you're working with large or even medium- sized client applications, it's common to have multiple model instances representing the same database- backed object. This usually happens when you have multiple views of some data, such that a model appears in two or more views.  


Consider this example, which introduces two new collections of users: Followers, for users that are following a given user (say, on a social network), and Following, for users whom a given user happens to be following. A user who is both a follower and being followed will appear in both collections, in which case we will have duplicate instances of the same database- backed model:


--- Page 61 ---

var FollowingCollection \(=\) UserCollection.extend({ url: '/following' }); var FollowersCollection \(=\) UserCollection.extend({ url: '/followers' }); var following \(=\) new FollowingCollection(); var followers \(=\) new FollowersCollection(); following.fetch(); followers.fetch(); var user1 \(=\) following.get('johndoe'); var user2 \(=\) followers.get('johndoe'); user1 \(= = =\) user2; // false  


Having multiple instances of the same model has two major downsides.  


First, you are using additional memory to represent the same object. Depending on the complexity of the model and the sizes of the attributes it holds, it's not unreasonable for a single instance to consume kilobytes of memory. If instances are duplicated dozens or hundreds of times—a very possible scenario for long- lived single- page applications—they can quickly become a memory sink.  


Secondly, if you or the user modifies the state of one of these models on the client, other instances of that model will fall out of sync. This can happen through a number of means, like if the user changes the state of the object via the UI, or an update created by another user is sent to the client via a real- time service:  


user1.set('firstName', 'Johnny'); user2.get('firstName'); // still John  


In this simple example, where the same user appears in only two different collections, it might seem trivial to update both instances manually with the new property. But it's easy to imagine how in a complex application the same user object might exist across dozens of different collections—not just follower/following lists, but also notifications, feed items, logs, and so on.  


It would be terrific if, instead of having to track down every instance of a given model, we could have each instance update itself intelligently. Or better yet, if we never had duplicated instances to begin with.


--- Page 62 ---

## Miniature Models of Factories  


A common solution for handling duplicate instances is to use a factory function when you create a new model instance. If the factory detects that a model instance already exists, it will just return the existing instance instead:  


var userCache = {}; function UserFactory(attrs, options) { var username \(=\) attrs.username; return userCache[username] : userCache[username] : new User(attrs, options); } var user1 \(=\) UserFactory({ username: 'johndoe' }); var user2 \(=\) UserFactory({ username: 'johndoe' }); user1 \(= = =\) user2; // true  


In order to use this pattern effectively, you must always use this factory function when creating new instances. This is a simple enough chore when managing your own code. But difficulty arises when you try to enforce this pattern in codebases you aren't responsible for, like third- party libraries and plugins.  


Consider, for example, the Collection.prototype._prepareModel function from Backbone's source code. Backbone uses this function to "prepare" and ultimately create a new model instance to add to a collection. It is invoked by a variety of means, such as when you're populating a collection with models returned from an HTTP resource:  


// Prepare a hash of attributes (or other model) to be added to this // collection. Backbone.Collection.prototype._prepareModel \(=\) function(attrs, options) { if (attrs instanceof Model) { if (!attrs.collection) attrs.collection \(=\) this; return attrs; } options || (options \(=\) {}); options.collection \(=\) this; var model \(=\) new this.model(attrs, options); if (!model._validate(attrs, options)) { this.trigger('invalid', this, attrs, options); return false; } return model; };  


Of particular importance is this line:  


var model \(=\) new this.model(attrs, options);


--- Page 63 ---

This is what actually creates a new instance of the model associated with this collection.  


this.model is a reference to the constructor of the model class the collection wraps. It's specified when you define a new collection class, like we did earlier:  


var UserCollection \(=\) Backbone.Collection.extend({ model: User, url: '/users' });  


What's pretty cool is that instead of passing the User class to the collection definition, we can pass the UserFactory class (our factory function that returns unique model instances):  


var UserCollection \(=\) Backbone.Collection.extend({ model: UserFactory, url: '/users' });  


UserFactory will then be assigned to this.model, and will be invoked by the new operator when the collection creates a new instance:  


var model \(=\) new this.model(attrs, options); // this.model is UserFactory  


But wait a minute. Now we're invoking UserFactory via the new operator. We weren't doing that earlier; we were calling the function directly. Does this even work?  


It turns out it does.  


## Constructor Identity Crisis  


What exactly happens when you use the new operator on a function? A few things:  


1. It creates a new object.  
2. It sets that object's prototype property to be the prototype property of the constructor function.  
3. It invokes the constructor function, with this assigned to the newly created object.  
4. It returns the object, unless the constructor function returns a nonprimitive value. In that case, the nonprimitive value is returned instead.  


That last one is the neat part. If your constructor function returns a nonprimitive value, that becomes the result of the new operation.  


Since UserFactory returns a nonprimitive, that means that these two operations return the same value:


--- Page 64 ---

var user1 \(=\) UserFactory({ username: 'johndoe' }); var user2 \(=\) new UserFactory({ username: 'johndoe' });  


user1 === user2; // true  


This property of the new operator is pretty handy. It means that you can essentially discard the object created by new, and return what you want—in our case, a unique user model instance.  


## Making It Scale  


In the examples so far, UserFactory has been a single- purpose factory function; it only guarantees uniqueness of User instances. While that's super handy, there are probably other models for which we'll want to guarantee uniqueness. So, it would be nice to have a general- purpose wrapper that can work for any model class.  


In a moment we'll look at a function called UniqueFactory. It's actually a constructor function that is invoked with the new operator, and takes as input a normal Backbone model class. It returns a wrapped constructor function that generates unique instances of that class.  


For example, it can actually generate a UserFactory class:  


var UserFactory \(=\) new UniqueFactory(User); var user1 \(=\) UserFactory({ username: 'johndoe' }); var user2 \(=\) new UserFactory({ username: 'johndoe' }); user1 === user2; // true  


The UniqueFactory implementation is shown here:  


/\\* \\* \\* UniqueFactory takes a class as input, and returns a wrapped version of \\* that class that guarantees uniqueness of any generated model instances. \\* \\* \\* Example: \\* var UniqueUser \(=\) new UniqueFactory(User); \\*/ function UniqueFactory (Model) { var self \(=\) this; // The underlying Backbone Model class this.Model \(=\) Model; // Tracked instances of this model class this.instances \(=\) {}; // Constructor to return that will be used for creating new instances var WrappedConstructor \(=\) function (attrs, options) {


--- Page 65 ---

return self.getInstance(attrs, options); }; // For compatibility with Backbone collections, our wrapped // model prototype should point to the \\*actual\\* Model prototype WrappedConstructor.prototype = this.Model.prototype; return WrappedConstructor; } UniqueFactory.prototype.getInstance = function (attrs, options) { options = options || {}; var id = attrs && attrs[this.Model.prototype.idAttribute]; // If there's no ID, this model isn't being tracked, and // cannot be tracked; return a new instance if (!id) return new this.Model(attrs, options); // Attempt to restore a cached instance var instance = this.instances[id]; if (!instance) { // If we haven't seen this instance before, start caching it instance = this.createInstance(id, attrs, options); } else { // Otherwise update the attributes of the cached instance instance.set(attrs); } return instance; }; UniqueFactory.prototype.createInstance = function (id, attrs, options) { var instance = new this.Model(attrs, options); this.instances[id] = instance; return instance; };  


Let's take a closer look at the UniqueFactory constructor, because it's doing some tricky stuff.  


First recall that UniqueFactory is intended to be invoked with the new operator, which creates a new object and assigns it to this (which is immediately aliased to self). The constructor creates a new function, WrappedConstructor, whose signature matches that of a Backbone.Model constructor function. But instead of invoking the actual constructor, it calls the getInstance prototype method of the UniqueFactory instance we just created:  


var WrappedConstructor = function (attrs, options) { return self.getInstance(attrs, options); };


--- Page 66 ---

Then, on the last line of this function, UniqueFactory returns WrappedConstructor. Once again, we've decided to ignore the object created by the new operator, and instead return an entirely different object—a function, even.  


This means that when we invoke UniqueFactory, the return value is actually our wrapped constructor:  


var UserFactory = new UniqueFactory(User); // WrappedConstructor  


However, this time we actually used the object created by the new operator. We just didn't return it. And it still exists: in the closure created by the WrappedConstructor function (self).  


Phew. Did you catch all that?  


This is kind of a funny implementation. It's not necessarily ideal, but I presented it to you to demonstrate how the new operator can be abused in an interesting—if somewhat confusing—way. Namely, a constructor function can both make use of the object created by new and return an entirely new value, at the same time.  


## Beware of Memory Leaks  


In the example factory implementations here, I've glossed over an important detail: they maintain an ever- growing global cache of model instances. Since instances are never removed from the cache even when they're no longer needed, they continue occupying memory forever (or at least, until the page refreshes).  


For example, suppose a unique model instance is destroyed via Model.proto type.destroy:  


(function () { var user \(=\) UserFactory({ username: 'johndoe' });  


user.destroy(); // sends HTTP DELETE to API server )();  


Despite the user variable not existing outside the functional scope in which it is declared, and despite the johndoe record being destroyed on the server, the instance lives on inside our UserFactory instance cache.  


This is particularly bad in long- lived single- page applications. A proper implementation would "track" instance creation and dismissal, and remove the instance from the cache when it is no longer required to be there.  


## Conclusion  


In this chapter, we've identified the "uniqueness" problem that affects applications where the same database- backed object appears in multiple collections. We explored a


--- Page 67 ---

powerful solution for this problem: functions that wrap a class constructor, and guarantee the uniqueness of any returned objects. Lastly, we introduced a utility, UniqueFactory, that generates model classes that similarly guarantee uniqueness.  


What we've covered isn't necessarily unique to JavaScript. Factory methods that return unique instances are tried- and- true patterns that can be—and certainly have been—implemented in any number of languages.  


But one clever trick that JavaScript has up its sleeve is the new operator. Specifically, the function on which new is called can ignore the newly created object (this) and return what it pleases. This little quirk is deceptively powerful, because it allows you to emulate object creation when object creation is expected—for instance, when you're working with external libraries like Backbone.  


In my experience, JavaScript has never been accused of being a particularly flexible language. It still bears the marks of being designed in 10 days. But for all its warts, occasionally I discover new things about it that particularly please me. This small property of the new operator is one of them. Hopefully, having read this chapter, you'll feel similarly.


--- Page 68 ---

# 1


--- Page 69 ---

# One World, One Language  


Jenn Schiffer  


There sure are a lot of languages.  


—Jenn Schiffer  


It was September 2003 when I began my undergraduate studies in computer science. Having chosen a liberal arts school, I was required to select a number of general education course requirements that lived outside the realm of my major. One of those requirements was two foreign language courses. When I inquired about using Java to fulfill that sequence, my request was immediately shut down. "You have to pick a real foreign language, like Spanish or French," my undergraduate advisor told me.  


Perhaps I should have asked about JavaScript.  


To be multilingual, or a polyglot, has always been presented as superior to being able to speak one's native language only. I have never understood why people believe this. Living under one roof, having one job for an extended amount of time, and being in a long- term monogamous relationship: these are seen as qualities of a stable life. Being an expert in a single subject, as opposed to knowing a little bit about a lot, is championed. So should be the case with programming.  


JavaScript is a single, stable language that is powerful enough to build the World Wide Web, make robots move, and convince publishers to print entire books about it. If we were required to pick a single "best" programming language, JavaScript seems like a no- brainer.  


It is understandably controversial to say that a specific language is better than the rest and that it should, therefore, become the official language of programming. Who am I to decide which language every other programmer should learn and build with? In my favor, one of the greatest aspects of web development in the 21st century is the expression of opinions so strong they are worthy of becoming web standards.


--- Page 70 ---

## An Imperative, Dynamic Proposal  


Imagine you are an academic advisor at a liberal arts college and are tasked with defining the choices given to students for their foreign language requirements. A language called "JavaScript" comes up in a proposal, and you need to study it and determine if it is a viable option. Naturally, you just so happen to be a fluent JavaScript expert, yet you are not sure it would be more useful than, say, Java.  


Java is notoriously simple to learn at the college freshman level, regardless of the student's experience:  


/\\*\\*\\* Hello World in Java \\*/ class Example { public static void main(String[] args) { System.out.println("Hello World."); } }  


To run Java, though, the client must also be running the Java virtual machine (J.V.M.). It would be silly to ask students to carry multiple machines around to all of their classes, so a language that does not require a JVM would be a better option. You might be thinking, "Maybe this is a weird joke I just don't get?" Perhaps the author, yours truly, is trying to make a joke, and you feel like there are much better ones she could make. But this is no joke: JavaScript does not require a Java virtual machine.  


Neither does Haskell:  


- Hello World in Haskell main = putStrLn "Hello World."  


The problem with Haskell is that, unlike JavaScript, it requires installation of a compiler. It is also a functional programming language that, like Latin, is considered "dead" and referenced only in historical texts. Yes, it is useful to learn Haskell in order to understand the context of programming today, but not for making useful products. It would be irresponsible to require students to learn something that would not help them build client- side web applications.  


Ruby happens to be quite useful in building web applications:  


# Hello World in Ruby puts "Hello World."  


One of the features of Ruby is flexibility in the form of having dozens of different versions, the most popular of which is called Rails. Rails itself has many versions—dialects, if you will—which causes communication breakdowns between apps. Multiple versions works for operating system releases, but not for web development. JavaScript


--- Page 71 ---

versions do not matter to the user or developer because it is not server- side, and removing that headache makes it a better option for teaching.  


Cascading Style Sheets (C.S.S.) is also not server- side and does not require a compiler or virtual machine:  


/\* Hello World in C.S.S. \*/ #example { content: 'Hello World.'}  


But much like hardware does not work without software, C.S.S. does not work without other languages. In the previous example, the browser looks for an element on the page with the ID "example." If the developer did not use another language to create that element, the C.S.S. cannot do anything. The professor teaching the foreign language course would have to teach another language in addition to C.S.S., and that is asking a lot of the staff. JavaScript does not need other languages to work. It just works.  


How about HyperText Markup Language (H.T.M.L.)? It works on its own and does not need a compiler installed:  


<!- - Hello World in H.T.M.L. - - > <!DOCTYPE html> <html ng- app> <head> <script src="angular.js"></script> </head> <body ng- controller="ExampleController"> <script type="text/javascript"> function ExampleController($scope) { \(\) scope.printText \(=\) "Hello World"; } </script> <h1></h1> </body> </html>  


Actually, H.T.M.L. does need another language to work, and it is JavaScript. Sure, in the past, H.T.M.L. used to be all you needed to create a web page. In the current state of the Semantic Web, though, the use of frontend JavaScript frameworks like Ember.js is required to bind text to a document.  


JavaScript does not need a JavaScript framework to run, because it is JavaScript already:  


// Hello World in JavaScript alert('Hello World');


--- Page 72 ---

And there you have it. Simple, pure, vanilla, untouched, beautiful JavaScript. Short, effective, and simple to teach. You can rightfully count JavaScript among the options for teaching foreign languages to your college's student body.  


## The Paradox of Choice  


As hard as it is to choose the options of foreign language courses a student can take, it is even harder for the student to decide among those options. One of the hardest problems in computer science is choosing the right tool to use, and the same certainly goes for communication. It is an impossible question to ask: "German or JavaScript?" Why can a student not learn both?  


This may seem like an NP- complete problem. You cannot teach JavaScript in German, because JavaScript syntax is in American English:  


Benachrichtigung('Hello World');  


Although semantically, factually, and tactfully correct, the preceding code is syntactically incorrect:  


>> ReferenceError: Benachrichtigung is not defined  


It turns out, though, that you can teach German in JavaScript:  


alert('Hallo Welt');  


If one can learn a language within JavaScript, then it is clear that JavaScript can be the only foreign language course offered that will not prevent students from learning how to communicate in foreign countries.  


## Globalcommunicationscript  


College is the basis of learning for all web developers, as is evident with the current education revolution within the software industry. As more programming jobs are created, educators grow more responsible for fostering the growth of new developers. To make this job easy, it only makes perfect sense to choose a language that everyone can communicate and learn with. As we discovered in our foreign language course narrative, that language is JavaScript.  


Simple, pure, vanilla, untouched, beautiful JavaScript.


--- Page 73 ---

# CHAPTER SEVEN  


# Math Expression Parser and Evaluator  


Ariya Hidayat  


Domain- specific languages (DSLs) are encountered in many aspects of a software engineer's life: configuration file formats, data transfer protocols, model schemas, application extensions, interface definition languages, and many others. Because of the nature of such languages, the language expression needs to be straightforward and easy to understand.  


In this chapter, we will explore the use of JavaScript to implement a simple language that can be used to evaluate a mathematical expression. In a way, it is very similar to a classic handheld programming calculator. Besides the typical math syntax, our JavaScript code should handle operator precedence and understand predefined functions.  


Given a math expression as a string, this is the series of processing applied to that string:  


The string is split into a stream of tokens. The tokens are used to construct the syntax tree. The syntax tree is traversed to evaluate the expression.  


Each step will be described in the following sections.  


## Lexical Analysis and Tokens  


The first important thing to do to a string representing a math expression is lexical analysis—that is, splitting the string into a stream of tokens. Quite expectedly, a


--- Page 74 ---

function that does this is often called a tokenizer. Alternatively, it is also known as a lexer or a scanner.  


We first need to define the types of the tokens. Since we'll be dealing with simple math expressions, all we really need are number, identifier, and operator. Before we can identify a portion of a string as one of these tokens, we need some helper functions (they are self- explained):  


function isWhiteSpace(ch) { return (ch == 'u0009') || (ch == ' ') || (ch == 'u00A0'); }  


function isLetter(ch) { return (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'); }  


function isDecimalDigit(ch) { return (ch >= '0') && (ch <= '9'); }  


Another very useful auxiliary function is the following createToken, used mostly to avoid repetitive code in the later stages. It basically creates an object for the given token type and value:  


function createToken(type, value) { return { type: type, value: value }; }  


As we iterate through the characters in the math expression, we will need a way to advance to the next character and another method to have a peek at the next character without advancing our position:  


function getNextChar() { var ch = 'x00', idx = index; if (idx < length) { ch = expression.charAt(idx); index += 1; } return ch; }  


function peekNextChar() { var idx = index; return ((idx < length) ? expression.charAt(idx) : 'x00'); }


--- Page 75 ---

In our expression language, spaces do not matter: \(40 + 2\) is treated the same as \(40 + 2\) . Thus, we need a function that ignores whitespace and continues to move forward until there is no whitespace anymore:  


function skipSpaces() { var ch; while (index < length) { ch = peekNextChar(); if (!isWhiteSpace(ch)) { break; } getNextChar(); }  


Suppose we want to support standard arithmetic operations, brackets, and simple assignment. The operators we need to support are \(+, - , *, /, = , (\) , and ). A method to scan such an operator can be constructed as follows. Note that rather than checking the character against all possible choices, we just use a simple trick utilizing the String.indexOf method. By convention, if this scanOperator function is called but no operator is detected, it returns undefined:  


function scanOperator() { var ch = peekNextChar(); if ('+\\*/()='.indexOf(ch) \(> = 0\) { return createToken('Operator', getNextChar()); } return undefined; }  


Deciding whether a series of characters is an identifier or not is slightly more complex. Let us assume we allow the first character to be a letter or an underscore. The second, third, and subsequent characters can each be another letter or a decimal digit. We disallow a decimal digit to start an identifier to avoid confusion with a number. Let's begin with two simple helper functions that do these checks:  


function isIdentifierStart(ch) { return (ch \(= =\) '') || isLetter(ch); }  


function isIdentifierPart(ch) { return isIdentifierStart(ch) || isDecimalDigit(ch); }  


The identifier check can now be written as a simple loop like this:  


function scanIdentifier() { var ch, id; ch = peekNextChar();
