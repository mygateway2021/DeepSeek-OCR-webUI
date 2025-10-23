--- Page 76 ---

interest areas like APIs and JavaScript, they have a collection of "guilds" that anyone can join. In the spirit of empowerment and delivery speed, Hootsuite does not have any governance checkpoints that intrude on a team's development process. Instead, they have a set of community- defined principles and tools that guide microservice development. Recently, they formed a technology architecture group made up of senior technical leaders to address technological issues that have a broad effect on the organization, but this group was formed organically—not as the result of an executive edict. Beier Cai, Director of Software Development, likens Hootsuite's governance approach to "eventual consistency." This empowered, iterative style is a match for the microservices way.  


Fittingly given the company's origin, Hootsuite has created a goal- oriented toolset for microservices. To address deployment, they use Docker and Mesos. For service discovery, they use Consul and NGINX. These four open source components are used together in a solution called "Skyline" that enables secure, dynamic, performant routing in their growing fabric of microservices. They have also found Scala, Akka, and the Play framework useful in building their individual services, and leverage both HTTP and Kafka for interservice communication. The tooling extends to the design process as well. To make sure developers know what services and components are available for use in service development, the Hootsuite team created a tool to dynamically generate system visualizations that link to code repositories and operational documentation. As needs arise, more tools are discovered or created.  


Hootsuite's evolution to a microservice architecture continues. They have over a dozen microservices in production with many more on the way. As a result of embracing an approach to microservices adoption that cuts across their architecture, organization, culture, processes, and tools, they have been able to improve their delivery speed, flexibility, autonomy, and developer morale.


--- Page 77 ---

# Service Design  


As discussed in Chapter 3, one of the key elements—the one most everyone thinks of when we talk about microservice architecture—is the design of the actual microservice components themselves. It is these autonomous services that make up the fabric of our microservice system and do the actual work of implementing your solution strategy. Implementing systems that contain a large number of small service components is a challenge so we'll devote an entire chapter to a set of tools and processes that can help you and your team take on the task.  


In our experience working with various organizations and interviewing others, some of the more challenging questions that teams adopting microservice architecture face are how to properly size microservices ("how micro is micro?") and how to properly deal with data persistence in order to avoid sharing of data across services. These two concerns are actually closely related. A mistake in optimal sizing often begets the extraneous data- sharing problem, but the latter is especially problematic, operationally, since it can create tight cross- service coupling and impede independent deployability, a core value of the architectural style. Other topics that come up frequently when we talk with people who are designing and implementing microservices are things like support for asynchronous messaging, transaction modeling, and dealing with dependencies in a microservice environment. Getting a handle on these elements will help you curb the amount of additional (nonessential) complexity that creeps into your overall system. And doing that can help you in your constant struggle to balance the two key factors in any IT system: speed and safety.  


In this chapter, we will cover microservice boundaries, looking at just how "micro" a service should be and why. We will explore microservice interfaces (APIs), discussing the importance of evolvable, message- oriented APIs for microservices and how they can reduce intercomponent coupling. We will investigate effective data storage approaches for microservices, exploring the power of shifting from data- centric and


--- Page 78 ---

state- capturing models toward capability- driven and event- sourcing- oriented ones. We'll also show how the command query responsibility segregation (CQRS) pattern can improve the granularity of data services, while maintaining sufficient speed and safety.  


This chapter will also cover key topics such as supporting transactions across microservice boundaries, asynchronous messaging, and dealing with dependencies with eyes on the prize of independent deployability.  


By the time we get through this material you should have a good understanding of the challenges as well as the available patterns and practices you can use when it comes to designing and building microservice components.  


Let's get started with the big one: "What is the optimal size of a microservice?"  


## Microservice Boundaries  


So just how micro should a microservice be?  


In reality, there is no simple answer for this question. The things that first come to mind, such as lines of code in a microservice or the size of a team working on one are compelling, since they offer the chance to focus on a quantifiable value (e.g., "The answer is 42!").<sup>1</sup> However, the problem with these measures is that they ignore the business context of what we are implementing. They don't address the organizational context of who is implementing the service and, more importantly, how the service is being used within your system.  


Instead of trying to find some quantity to measure, we find most companies focus on a quality of each microservice—the use case or context in which the component will be used. Many microservice adopters have turned to Eric Evans' "domain- driven design" (DDD) approach for a well- established set of processes and practices that facilitate effective, business- context- friendly modularization of large complex systems.  


## Microservice Boundaries and Domain-Driven Design  


Essentially, what we see people doing when they introduce the microservices way into their companies is that they begin to decompose existing components into smaller parts in order to increase their ability to improve the quality of the service faster without sacrificing reliability.  


There are many ways to decompose a large system into smaller subsystems. In one case we may be tempted to decompose a system based on implementation technology.


--- Page 79 ---

For instance, we can say that all computationally heavy services need to be written in C or Rust or Go (choose your own poison) and therefore they are a separate subsystem, while I/O- heavy features could certainly benefit from the nonblocking I/O of a technology such as Node.js and therefore they are a subsystem of their own. Alternatively, we can divide a large system based on team geography: one subsystem may be written in the US, while others may be developed and maintained by software teams in Africa, Asia, Australia, Europe, or South America. Intuitively, giving a self- contained subsystem for development to a team that is located in one place is well- optimized. Another reason you may decide to divide a system based on geography is that specific legal, commercial, and cultural requirements of operating in a particular market may be better understood by a local team. Can a software development team from New York accurately capture all the necessary details of an accounting software that will be used in Cairo?  


In his seminal book Domain- Driven Design, Eric Evans outlines a fresh approach to determining boundaries of subsystems in the context of a larger system. In the process, he offers a model- centric view of software system design. As we've pointed out in this book, models are a great way to view a system. They provide an abstract way to look at something—a way that highlights the things we are interested in. Models are a point of view.  

  


## It's Only a Model  


To understand the DDD approach, it is important to remember that any software system is a model of a reality—it is not the reality itself. For instance, when we log in to online banking and are looking at our checking account, we are not looking at the actual checking account. We're just looking at a representation—a model—that gives us information about the checking account such as balance and past transactions. It's likely that the screen our bank teller sees when looking at our account has different information because it's another model of our account.  


In his book, Evans notes that most large systems don't actually have a single model. The overall model of a large system is actually comprised of many smaller models that are intermingled with each other. These smaller models are organic representations of relevant business contexts—they make sense in their context and when used within the context they are intuitive for a person who is the subject matter expert of the context.


--- Page 80 ---

## Bounded Context  


In DDD, Evans points out that teams need to be very careful when combining contextual models to form a larger software system. He puts it this way:  


Multiple models are in play on any large project. Yet when code based on distinct models is combined, software becomes buggy, unreliable, and difficult to understand. Communication among team members becomes confused. It is often unclear in what context a model should not be applied.  


—Eric Evans, author of Domain- Driven Design: Tackling Complexity in the Heart of Software  


It is worth noting that Evans' DDD was introduced more than a decade before the word "microservice" had come into vogue. Yet, the preceding quotation is an important observation about the nature of modeling—if you try to rely on a single model (e.g., a canonical model) things become difficult to understand. The microservices way attempts to break large components (models) into smaller ones in order to reduce the confusion and bring more clarity to each element of the system. As such, microservice architecture is an architectural style that is highly compatible with the DDD way of modeling. To aid in this process of creating smaller, more coherent components, Evans introduced the bounded contexts concept. Each component in the system lives within its own bounded context, which means the model for each component and these context models are only used within their bounded scope and are not shared across the bounded contexts.  


It is generally acknowledged that properly identifying bounded contexts in a system, using DDD techniques, and breaking up a large system along the seams of those bounded contexts is an effective way of designing microservice boundaries. In his book Building Microservices, Sam Newman states:  


If our service boundaries align to the bounded contexts in our domain, and our microservices represent those bounded contexts, we are off to an excellent start in ensuring that our microservices are loosely coupled and strongly cohesive.  


Newman makes an important point here: bounded contexts represent autonomous business domains (i.e., distinct business capabilities), and therefore are the appropriate starting point for identifying the dividing lines for microservices. If we use the DDD and bounded contexts approaches, the chances of two microservices needing to share a model and the corresponding data space, or ending up having tight coupling, are much lower. Avoiding data sharing improves our ability to treat each microservice as an independently deployable unit. And independent deployability is how we can increase our speed while still maintaining safety within the overall system.  


Using DDD and bounded contexts is an excellent process for designing components. However, there is more to the story. We could actually use DDD and still end up creating fairly large components. But large is not what we're going for in a microservice


--- Page 81 ---

architecture. Instead, we're aiming at small—micro, even. And that leads to an important aspect of designing microservice components—smaller is better.  


## Smaller Is Better  


The notion of work- unit granularity is a crucial one in many contexts of modern software development. Whether defined explicitly or implicitly, we can clearly see the trend showing up in such foundational methodologies as Agile Development, Lean Startup, and Continuous Delivery, among others. These methodologies have revolutionized project management, product development, and DevOps, respectively.  


It is interesting to note that each one of them has the principle of size reduction at its core: reducing the size or scope of the problem, reducing the time it takes to complete a task, reducing the time it takes to get feedback, and reducing the size of the deployment unit. These all fall into a notion we call "batch- size reduction."  


For example, here's an excerpt from the Agile Manifesto:  


Deliver working software frequently, from a couple of weeks to a couple of months, with a preference to the shorter timescale.  


—The Agile Manifesto, Kent Beck et al.  


Basically, moving to Agile from Waterfall can be viewed as a reduction of the "batch size" of a development cycle—if the cycle was taking many months in Waterfall, now we strive to complete a similar batch of tasks: define, architect, design, develop, and deploy, in much shorter cycles (weeks versus months). Granted, the Agile Manifesto lists other important principles as well, but they only reinforce and complement the core principle of "shorter cycles" (i.e., reduced batch size).  


In the case of Lean Startup, Eric Ries directly points to the crucial importance of small batch size, right in the definition of the methodology:  


The Lean Startup takes its name from the lean manufacturing revolution that Taiichi Ohno and Shigeo Shingo are credited with developing at Toyota. Lean thinking is radically altering the way supply chains and production systems are run. Among its tenets are drawing on the knowledge and creativity of individual workers, the shrinking of batch sizes, just- in- time production and inventory control, and an acceleration of cycle times. It taught the world the difference between value- creating activities and waste and showed how to build quality into products from the inside out.  


—Eric Ries, author of The Lean Startup  


Similarly, when discussing the principal benefits of Continuous Delivery, Martin Fowler is unambiguous about the role of small batch sizes, calling it the precondition for a core benefit of the methodology.  


Once you adopt the notion of limited batch size from Agile, Lean, and Continuous Delivery at the code, project, and deployment level, it makes sense to think about


--- Page 82 ---

applying it at the architecture level as well. And many of the companies we interviewed have done this. After all, architecture is the direct counterpart to the other three disciplines. So, in the simplest terms, this "limited batch size" is the "micro" in microservice.  

  


Just as in Agile, etc., there's no simple, universal measure for determining just "how small" a microservice should be (e.g., a quantity). What people tell us is that they use the word "small" as a quality like "reliable" and "coherent," etc.  


## Ubiquitous Language  


Just by stating a simple preference of "smaller is better," we immediately run into a problem if bounded contexts are our only tool for sizing microservices, because bounded contexts cannot actually be arbitrarily small. Here's what one of the prominent authorities in the space of DDD, Vaughn Vernon, had to say about the optimal size of a bounded context:  


Bounded context should be as big as it needs to be in order to fully express its complete ubiquitous language.  


—Vaughn Vernon, author of Implementing Domain- Driven Design  


In DDD, we need a shared understanding and way of expressing the domain specifics. This shared understanding should provide business and tech teams with a common language that they can use to collaborate on the definition and implementation of a model. Just as DDD tells us to use one model within a component (the bounded context), the language used within that bounded context should be coherent and pervasive—what we in DDD call ubiquitous language.  


From a purely technical perspective, the smaller the microservice the easier it can be developed quicker (Agile), iterated on quicker (Lean), and deployed more frequently (Continuous Delivery). But on the modeling side, it is important to avoid creating services that are "too small." According to Vernon, we cannot arbitrarily reduce the size of a bounded context because its optimal size is determined by the business context (model). Our technical need for the size of a service can sometimes be different (smaller) from what DDD modeling can facilitate. This is probably why Sam Newman, very carefully, called bounded context analysis an "excellent start," but not the sole prescription for how to size microservices. And we completely agree. Bounded contexts are a great start, but we need more tools in our toolbelt if we are to size microservices efficiently. We will discuss some of those tools later in this chapter, in particular when we look into data storage for microservices.


--- Page 83 ---

## API Design for Microservices  


When considering microservice component boundaries, the source code itself is only part of our concern. Microservice components only become valuable when they can communicate with other components in the system. They each have an interface or API. Just as we need to achieve a high level of separation, independence, and modularity of our code we need to make sure that our APIs, the component interfaces, are also loosely coupled. Otherwise, we won't be able to deploy two microservices independently, which is one of our primary goals in order to balance speed and safety.  


We see two practices in crafting APIs for microservices worth mentioning here:  


- Message-oriented- Hypermedia-driven  


## Message-Oriented  


Just as we work to write component code that can be safely refactored over time, we need to apply the same efforts to the shared interfaces between components. The most effective way to do this is to adopt a message- oriented implementation for microservice APIs. The notion of messaging as a way to share information between components dates back to the initial ideas about how object- oriented programming would work. Alan Kay reminded everyone of the power of messages on an email list in 1998:  


I'm sorry that I long ago coined the term "objects" for this topic because it gets many people to focus on the lesser idea. The big idea is "messaging."  


—Alan Kay  


All of the companies we talked with about microservice component design mentioned the notion of messaging as a key design practice. For example, Netflix relies on message formats like Avro, Protobuf, and Thrift over TCP/IP for communicating internally and JSON over HTTP for communicating to external consumers (e.g., mobile phones, browsers, etc.). By adopting a message- oriented approach, developers can expose general entry points into a component (e.g., an IP address and port number) and receive task- specific messages at the same time. This allows for changes in message content as a way of refactoring components safely over time. The key lesson learned here is that for far too long, developers have viewed APIs and web services as tools to transmit serialized "objects" over the wire. However, a more efficient approach is to look at a complex system as a collection of services exchanging messages over a wire.


--- Page 84 ---

## Hypermedia-Driven  


Some companies we spoke to are taking the notion of message- oriented to the next level. They are relying on hypermedia- driven implementations. In these instances, the messages passed between components contain more than just data. The messages also contain descriptions of possible actions (e.g., links and forms). Now, not just the data is loosely coupled—so are the actions. For example, Amazon's API Gateway and AppStream APIs both support responses in the Hypertext Application Language (HAL) format.  


Hypermedia- style APIs embrace evolvability and loose coupling as the core values of the design style. You may also know this style as APIs with Hypermedia As The Engine Of Application State (HATEOAS APIs). Regardless of the name used, if we are to design proper APIs in microservice architecture, it helps to get familiar with the hypermedia style.  


Hypermedia style is essentially how HTML works for the browser. HTTP messages are sent to an IP address (your server or client location on the Internet) and a port number (usually "80" or "443"). The messages contain the data and actions encoded in HTML format. For example, a message that contains information on an outstanding shipment due to arrive at your office might look like this:  


<html> <head> <title>Shipment #123</title> </head> <body> <h1>Shipment #123</h1> <div id="data"> <span>ID: 123</span><br /> <span>Description: Widget Covers</span><br /> <span>Quantity: 1 Gross</span><br /> <span>Estimated Arrival: 2017-01-09</span><br /> </div> <div id="actions"> <a href="...">Refresh</a> <a href="...">Exit</a> <form method="get" action="..."> <input name="id" value=""/> <input type="submit" value="Search" /> </form> </div> </html>  


James Gregory of ThoughtWorks, a company experienced in helping customers adopt and implement microservice- style systems, puts it this way:


--- Page 85 ---

When we work on projects with more and more services involved the big revelation was the people who build HTTP and use Hypermedia know what they're talking about —and we should listen to them.  


—James Gregory, Lead Consultant at ThoughtWorks  


The hypermedia API style is as transformative to the API space as object- oriented design was for code design. A long time ago, we used to just write endless lines of code (maybe lightly organizing them in functions), but then object- oriented design came by with a revolutionary idea: "what if we grouped the state and the methods that operate on that state in an autonomous unit called an object, thus encapsulating data and behavior?" In essence, hypermedia style has very similar approach but for API design. This is an API style in which API messages contain both data and controls (e.g., metadata, links, forms), thus dynamically guiding API clients by responding with not just static data but also control metadata describing API affordances (i.e., "what can I do with this API?").  

  


To learn more about hypermedia APIs and how to design them, check out the book RESTful Web APIs by Mike Amundsen, Leonard Richardson, and Sam Ruby. By the way, don't let the book title fool you—even though it says "RESTful," it is about hypermedia APIs and among other things explains why the book says REST while it talks about hypermedia APIs.  


Exposing affordances makes sense for services that communicate over the Web. If we look at the Web as both the human- centric Web (websites consumed by humans) and machine Web (APIs), we can see stark differences in how far behind the machine Web is. When you load a web page on the human- centric Web, it doesn't just give you content (text, photos, videos, etc.)—most web pages also contain links to related content or search menus: something you can interact with. Basically, web pages tell you, in the response itself, what else you can do. Conventional web APIs don't do this. Most contemporary RESTful (CRUD) APIs respond with just data and then you have to go and read some documentation to find out what else can be done. Imagine if websites were like that: you would go to a specific URL, read content, then you'd have to look in some documentation (a book? a PDF?) to find other interesting URLs, many of which may be outdated, to navigate to the next thing. Most people would agree that it would be quite a ridiculous experience. The human Web wouldn't be very functional if the responses didn't contain behavioral affordances. But that's exactly the case for most modern RESTful APIs. And, as a matter of fact, the data- only approach is quite as brittle and dysfunctional for the machine Web as the picture we painted for the human- centric Web, except we have gotten used to the unfortunate state of affairs.


--- Page 86 ---

Hypermedia APIs are more like the human Web: evolvable, adaptable, versioning- free—when was the last time you cared about what “version” of a website you are looking at? As such, hypermedia- style APIs are less brittle, more discoverable, and fit right at home in a highly distributed, collaborative architectural style such as microservices.  


## Data and Microservices  


As software engineers, we have been trained to think in terms of data, first and foremost. To give the simplest example, it has pretty much been ingrained in our “muscle memory,” or whatever the mental equivalent of one is, to start system design by first designing the pertinent data models. When asked to build an application, the very first task most software engineers will complete is identifying entities and designing database tables for data storage. This is an efficient way of designing centralized systems and whole generations of programmers have been trained to think this way. But data- centric design is not a good way to implement distributed systems—especially systems that rely on independently deployable microservices. The biggest reason for this is the absence of strong, centralized, uniform control over the entire system in the case of distributed systems, which makes a formerly efficient process inefficient.  


The first step in breaking the data- centric habit is to rethink our system designs. We need to stop designing systems as a collection of data services and instead use business capabilities as the design element, or as Sam Newman notes in his book:  


You should be thinking not in terms of data that is shared, but about the capabilities those contexts provide [...]. I have seen too often that thinking about data leads to anemic, CRUD- based (create, read, update, delete) services. So ask first “What does this context do?” and then “So what data does it need to do that?”  


—Sam Newman, author of Building Microservices  


It turns out that capabilities- centric design is more suitable for microservices than a more traditional, data- centric design.  


## Shipping, Inc.  


To demonstrate some of the practical aspects of microservice architecture, throughout Chapters 5 and 6 we will be using an imaginary startup. Let’s assume that we are designing a microservice architecture for a fledgling shipment company, aptly named Shipping, Inc. As a parcel- delivery company, they need to accept packages, route them through various sorting warehouses (hops on the route), and eventually deliver to the destination. Because it is 2016 and the company is very tech- savvy, Shipping, Inc. is building native mobile applications for a variety of platforms to let customers track their packages all the way from pickup to final delivery. These mobile applications will get the data and functionality they need from a set of microservices.


--- Page 87 ---

Let's imagine that Shipping, Inc.'s accounting and sales subsystems (microservices) need access to daily currency exchange rates to perform their operations. A datacentric design would create a table or set of tables in a database that contain exchange rates. Then we would let various subsystems query our database to retrieve the data. This solution has significant issues—two microservices depend on the design of the shared table and data in it, leading to tight coupling and impeding independent deployability.  


If instead, we had viewed "currency exchange rates" as a capability and had built an independent microservice (currency rates) serving the sales and accounting microservices, we would have had three independent services, all loosely coupled and independently deployable. Furthermore, since, by their nature, APIs in services hide implementation details, we can completely change the data persistence supporting the currency rates service (e.g., from MySQL to Cassandra, if scalability became an issue) without any of the service's consumers noticing the change or needing to adjust. Last but not least, since services (APIs) are able to put forward alternative interfaces to its various consumers, we can easily alter the interface that the currency rates microservice provides to the sales microservice, without affecting the accounting microservice, thus fulfilling the promise of independent evolution, a necessity for independent deployability. Mission accomplished!  


Thinking in terms of capabilities rather than data is a very powerful technique for API design, in general. It usually results in a more use- case- oriented interface (instead of an SQL- like data- object interface). A capabilities- centric API design is usually a good approach, but in the case of microservices it is not just a smart design technique, it's a powerful way of avoiding tight coupling. We just saw evidence of this.  


Much like bounded context analysis, capabilities- oriented design is a crucial technique but not sufficient to ensure independent deployability for all use cases. Not every example is as simple as our currency rates one. We cannot always encapsulate shared data inside a microservice and call it a day. For example, a common use case that cannot be solved with encapsulated capabilities is that of reporting. Any business application requires a certain level of reporting. And reporting often spans across multiple models, bounded contexts, and capabilities. Should reporting- oriented microservices be allowed to share tables with other microservices? The obvious answer is no, because that would immediately create severe tight coupling of services all around the system, and at the very least undermine (if not completely kill) independent deployability.  


Let's see what techniques we can use to avoid data- sharing in complex use cases. The first one we will look at is event sourcing, a powerful data- modeling methodology that can help us avoid data- sharing in microservices, even in very complicated cases. The second, related methodology is CQRS—command query responsibility segregation.


--- Page 88 ---

## Event Sourcing  


We've mentioned that there are some deeply ingrained software engineering habits that greatly affect the way we typically approach systems engineering. One of the most widespread of those habits is structural data modeling. It has become very natural for us to describe models as collections of interacting logical entities and then to map those logical entities to physical tables where the data is stored. More recently, we have started using NoSQL and object stores that take us slightly away from the relational world, but in essence the approach is still the same: we design structural entities that model objects around us and then we "save" the object's state in a database store of some kind. Whether storage happens in table rows and columns, serialized as JSON strings, or as object graphs, we are still performing CRUD- based modeling. But this is not the only way to model the world. Instead of storing structures that model the state of our world, we can store events that lead to the current state of our world. This modeling approach is called event sourcing.  


Event sourcing is all about storing facts and any time you have "state" (structural models)—they are first- level derivative off of your facts. And they are transient.  


Greg Young, Code on the Beach, 2014  


In this context, by "facts" Young means the representative value of an event occurrence. An example could be "a package was transported from the last sorting facility, out for final delivery." Later in this chapter, we will see more examples of what facts can be.  


It is fair to note that for the majority of software developers used to structural data modeling, event sourcing will initially sound alien and, maybe, even somewhat weird. But it really isn't. For one thing, event sourcing is not some bleeding- edge, untested theory dreamed up to solve problems in microservices. Event sourcing has been used in the financial industry with great success, independent of any microservice architecture association.  


In addition, the roots and inspiration for event sourcing go way beyond microservices, the Internet itself, or even computers—all the way back to financial accounting and the paper- and- pen ledgers that contain a list of transactions, and never just the end value ("state") of a balance. Think of your bank account: there's a balance amount for your checking and savings accounts, but those are not first- class values that banks store in their databases. The account balance is always a derivative value; it's a function. More specifically, the balance is the sum of all transactions from the day you opened your account.


--- Page 89 ---

If you decide to dispute your current balance and call up your bank, they are not going to retort by saying, "But sir/ma'am, that's the value in our database, it has to be true!" Instead, they will print out all relevant transactions for you (or point you to online banking where you can do it yourself) and let you verify that the result of the transactions should indeed be equal to the balance value displayed. If you do find any errors with any of the transactions, the bank will issue a "compensating transaction" to fix the error. This is another crucial property of event sourcing: much like in life, we can never "go back" in time and "change" the past, we can only do something in the present to compensate for the mistakes of the past. In event sourcing, data is immutable—we always issue a new command/event to compensate rather than update a state of an entity, as we would do in a CRUD style.  


When event sourcing is introduced to developers, the immediate concern is usually performance. If any state value is a function of events, we may assume that every access to the value would require recalculation of the current state from the source events. Obviously that would be extremely slow and generally unacceptable. Fortunately, in event sourcing, we can avoid such expensive operations by using a so- called rolling snapshot—a projection of the entity state at a given point in time. Depending on the event source implementation, it is common to snapshot intermediary values at various time points. For instance, you may precalculate your bank account balance on the last day of every month, so that if you need the balance on January 15, 2016 you will already have it on December 31, 2015 and will just need to calculate the projection for two weeks, instead of the entire life of the bank account. The specifics of how you implement rolling snapshots and projections may depend on the context of your application. Later in this chapter we will see that with a related pattern called CQRS, we can do much more than just cache states in rolling snapshots.  


Despite its accounting roots, event sourcing is not only relevant to just financial use cases. For the rest of this chapter we will use a business scenario as far from banking and accounting as we could imagine: shipment and delivery of goods.  


Remember the imaginary package- shipment startup Shipping, Inc. that we introduced in this chapter? As a parcel- delivery company, they need to accept packages, route them through various sorting warehouses (hops on the route), and eventually deliver to their destinations.  


A representative data model for this system executed in structural style is shown in Figure 5- 1.


--- Page 90 ---


<center>Figure 5-1. Data model for Shipping, Inc. using "current state" approach </center>  


The corresponding events- based model is shown in Figure 5- 2.  



<center>Figure 5-2. Data model for Shipping, Inc. using event sourcing </center>


--- Page 91 ---

As you can see, the structural model strives to only save the current state of the system, while the event sourcing approach saves individual "facts." State, in event sourcing, is a function of all the pertinent facts that occurred. Not only does this give us full auditability (as demonstrated in the case when we called our bank to dispute the balance), we can also build state projections toward any time in the past, not just the "now." Would you like to know where all the packages were on Wednesday? No problem with event sourcing! Answering this question would be more difficult with the structural model, since it would require special coding.  


If you enjoy noticing patterns in seemingly unrelated things the way we do, we urge you to take another look at the two diagrams. You may notice how every entity in the structural model is a "snowflake" (i.e., it has a unique "shape," in terms of properties and relationships, and was attentively crafted to represent differing real- life concepts). In contrast, events in an event store all look the same from the outside. This is a very similar view to another technology closely related to microservices: containers. Indeed, for the container host (e.g., a Docker host), all containers look alike—the host doesn't "care" what is inside a container, it knows how to manage the lifecycle of a container independent of the contents of the container. In contrast, custom- installed enterprise applications have all kinds of peculiar "shapes" and environmental dependencies that the host must ensure exist (e.g., shared libraries the application expects). The "indifference to shape and contents" approach seems to be a trend in modern technologies, as we can see the same pattern in SQL versus NoSQL storage. It is very reminiscent, in its tendency to show up under multiple contexts, of the "batch- size reduction" trend we noticed earlier while looking at different modern methodologies across multiple disciplines (e.g., project management, product development, operations, and architecture). We love this—when the same pattern emerges in multiple places, we can use our understanding of the pattern to identify or predict "next big thing."  


But let's get back to microservices. We dipped our toes in a data- modeling technology called event sourcing and noted some of its benefits compared to conventional, structural modeling, but how exactly does it help us solve the data isolation and encapsulation challenges of microservice architecture? As it turns out, we need one more design pattern, CQRS, to complement event sourcing and we will be well on our way toward being able to design effective data storage for microservices with data persistence models that can avoid data sharing at even very small microservice sizes.  


## System Model for Shipping, Inc.  


As we noted earlier, a good start for a microservice system design is to identify bounded contexts in the system. Figure 5- 3 shows a context map for key bounded contexts in our problem space. We will use this context map in discussing the solution throughout the chapter.


--- Page 92 ---


<center>Figure 5-3. High-level context map for Shipping, Inc.'s microservice architecture </center>  


What are the capabilities of the three contexts and some of the data flows between the contexts, depicted by the arrows and numbers on the graph? They are as follows:  


1. Customer Management creates, edits, enables/disables customer accounts, and can provide a representation of a customer to any interested context.  
2. Shipment Management is responsible for the entire lifecycle of a package from drop-off to final delivery. It emits events as the package moves through sorting and forwarding facilities, along the delivery route.  
3. Shipment Tracking is a reporting application that allows end users to track their shipments on their mobile device.  


If we were to implement a data model of this application using a traditional, structural, CRUD- oriented model we would immediately run into data sharing and tight- coupling problems. Indeed, notice that the Shipment Management and Shipment Tracking contexts will have to query the same tables, at the very least the ones containing the transitions along the route. However, with event sourcing, the Shipment Management bounded context (and its corresponding microservice) can instead record events/commands and issue event notifications for other contexts and those other contexts will build their own data indexes (projections), never needing direct access to any data owned and managed by the Shipment Management microservice. The formal approach to this process is described in a pattern called CQRS.  


## CQRS  


Command query responsibility segregation is a design pattern that states that we can (and sometimes should) separate data- update versus data- querying capabilities into separate models. It tracks its ancestry back to a principle called command- query separation (CQS), which was introduced by Bertrand Meyer in his book Object- Oriented


--- Page 93 ---

Software Construction (Prentice- Hall, 1997). Meyer argued that data- altering operations should be in different methods, separated from methods performing read- only operations. CQRS takes this concept a large step further, instructing us to use entirely different models for updates versus queries. This seemingly simple statement often turns out to be powerful enough to save the day, especially in the complicated case of the reports- centric microservices we mentioned earlier in this chapter.  


Since reports usually need to aggregate and contrast data generated in different parts of a large system, they often need to span multiple subsystems and bounded contexts and almost always require access to data from multiple contexts. But it is only so if we assume we have a single model for any entity, where we both query and update the entity. If we instead use CQRS, the need to access data across multiple contexts (and related problems) can be eliminated. With CQRS, the Shipment Management microservice can "own" and encapsulate any updates related to package delivery, just notifying other contexts about events occurring. By subscribing to notifications of these events, a reporting service such as Shipment Tracking can build completely independent, query- optimized model(s) that don't need to be shared with any other service.  


Figure 5- 4 shows a conceptual diagram that depicts CQRS for our Shipping, Inc. application.  


As you can see, thanks to CQRS, we were able to completely separate the data models of the Shipment Management and Tracking microservices. In fact, Shipping Management doesn't even need to know about the existence of the Tracking microservice, and the only thing the Tracking microservice relies on is a stream of events to build its query index. During runtime the Tracking microservice only queries its own index. Furthermore, the Tracking microservice can include event and command data from other microservices using the same flow, keeping its independence and loose coupling.  


The big win with using event sourcing and CQRS is that they allow us to design very granular, loosely coupled components. With bounded contexts our boundaries have to align with business capabilities and subdomain boundaries. With event sourcing, we can literally create microservices so tiny that they just manage one type of event or run a single report. Targeted use of event sourcing and CQRS can take us to the next level of autonomous granularity in microservice architecture. As such, they play a crucial role in the architectural style.


--- Page 94 ---


<center>Figure 5-4. Data flow in command-query responsibility segregation (CQRS)-based model for Shipping, Inc. </center>  

  


Be careful not to abuse/overuse event sourcing and CQRS. You should only use event sourcing and CQRS when necessary, since they will complicate your implementation. Event sourcing and CQRS are not an "architecture" for your entire system, rather they are a powerful toolset to be used sparingly. There are still many use cases in which the conventional, CRUD- based model is much simpler and should be preferred.  


## Distributed Transactions and Sagas  


The shared data model is not the only use case that can introduce tight coupling between microservices. Another important threat is workflows. A lot of real- life processes cannot be represented with a single, atomic operation, since they are a sequence of steps. When we are dealing with such workflows, the result only makes sense if all of the steps can be executed. In other words, if any step in the sequence fails, the resulting state of the relevant system becomes invalid. You probably recognize this problem from RDBMS systems where we call such processes "transactions." However, database transactions are local, contained within the confines of a single


--- Page 95 ---

database where their implementations predominantly rely on the use of a shared state (i.e., we put locks on the rows and tables that participate in a transaction, guaranteeing data consistency). Once the transaction is fully executed we can remove the locks, or if any step of the transaction steps fails, we can roll back the steps already attempted.  


For distributed workflows and share- nothing environments (and microservice architecture is both of those), we cannot use traditional transaction implementations with data locks and ACID compliance, since such transactions require shared data and local execution. Instead, an effective approach many teams use is known as "Sagas". Sagas were designed for long- lived, distributed transactions by Hector Garcia- Molina and Kenneth Salem, and introduced in 1987 (yes, way before microservices or even the Web) during their work at Princeton University.  


Sagas are very powerful because they allow running transaction- like, reversible workflows in distributed, loosely coupled environments without making any assumptions on the reliability of each component of the complex system or the overall system itself. The compromise here is that Sagas cannot always be rolled back to the exact initial state of the system before the transaction attempt. But we can make a best effort to bring the system to a state that is consistent with the initial state through compensation.  


In Sagas, every step in the workflow executes its portion of the work, registers a callback to a "compensating transaction" in a message called a "routing slip," and passes the updated message down the activity chain. If any step downstream fails, that step looks at the routing slip and invokes the most recent step's compensating transaction, passing back the routing slip. The previous step does the same thing, calling its predecessor compensating transaction and so on until all already executed transactions are compensated.  


Consider this example: let's say a customer mailed a prepaid cashier's check for \(\) 100\(via Shipping, Inc.'s insured delivery. When the courier showed up at the destination, they found out that the address was wrong and the resident wouldn't accept the package. Thus, Shipping, Inc. wasn't able to complete the transaction. Since the package was insured, it is Shipping, Inc.'s responsibility to "roll back" the transaction and return the money to the sender. With ACID - compliant transactions, Shipping, Inc. is supposed to bring the exact\) \ \(100\) check back to the original sender, restoring the system state to its exact initial value. Unfortunately, on the way back the package was lost. Since Shipping, Inc. could no longer "roll back" the transaction, they decided to reimburse the insured value of \(\) 100\(by depositing that amount into the customer's account. Since this was an active, long - time Shipping, Inc. customer and a rational human being, they didn't care which\) \ \(100\) was returned to them. The system didn't return to its exact initial state, but the compensating transaction brought the environment back to a consistent state. This is basically how Sagas work.


--- Page 96 ---

Due to its highly fault- tolerant, distributed nature, Sagas are very well- suited to replace traditional transactions when transactions across microservice boundaries are required in a microservice architecture. If you want to learn more about Sagas and see working code implementing a very expressive example related to travel booking, check out the Saga example by Clemens Vasters.  


## Asynchronous Message-Passing and Microservices  


Asynchronous message- passing plays a significant role in keeping things loosely coupled in a microservice architecture. You probably noticed that in one of the examples earlier in this chapter, we used a message broker to deliver event notifications from our Shipment Management microservice to the Shipment Tracking microservice in an asynchronous manner. That said, letting microservices directly interact with message brokers (such as RabbitMQ, etc.) is rarely a good idea. If two microservices are directly communicating via a message- queue channel, they are sharing a data space (the channel) and we have already talked, at length, about the evils of two microservices sharing a data space. Instead, what we can do is encapsulate message- passing behind an independent microservice that can provide message- passing capability, in a loosely coupled way, to all interested microservices.  


The message- passing workflow we are most interested in, in the context of microservice architecture, is a simple publish/subscribe workflow. How do we express it as an HTTP API/microservice in a standard way? We recommend basing such a workflow on an existing standard, such as PubSubHubbub. Now to be fair, PubSubHubbub wasn't created for APIs or hypermedia APIs, it was created for RSS and Atom feeds in the blogging context. That said, we can adapt it relatively well to serve a hypermedia API- enabled workflow. To do so, we need to implement a flow similar to the one shown in Figure 5- 5.  



<center>Figure 5-5. Asynchronous message-passing implemented with a PubSubHubbub-inspired flow </center>


--- Page 97 ---

We also need to standardize some hypermedia affordances:  


rel="hub"  


Refers to a hub that enables registration for notification of updates to the context.  


rel="pingback"  


Gives the address of the pingback resource for the link context.  


rel="sub"  


When included in a resource representation of an event, the "sub" (subscription) link relation may identify a target resource that represents the ability to subscribe to the pub/sub event- type resource in the link context.  


rel="unsub"  


When included in a resource representation of an event, the "unsub" (subscription cancellation) link relation may identify a target resource that represents the ability to unsubscribe from the pub/sub event- type resource in the link context.  


rel="event"  


Resource representation of a subscribeable events.  


rel="events"  


Link to a collection resource representing a list of subscribeable events.  


## Dealing with Dependencies  


Another important topic related to independent deployability is embedding of dependencies. Let's imagine that Shipping, Inc's currency rates microservice is being hammered by user queries and requests from other microservices. It would cost us much less if we hosted that microservice in a public cloud rather than on expensive servers of our corporate data center. But it doesn't seem possible to move the microservice to another host, if it stores data in the same SQL or NoSQL database system as all other microservices.  


Please note that data tables are not shared, just the installation of the database- management system. It seems like the logical conclusion is that we cannot have any microservice share even the installation of a data storage system. Some may argue that a microservice needs to "embed" every single dependency it may require, so that the microservice can be deployed wherever and whenever, without any coordination with the rest of the system.  


A strict requirement of full dependency embedding can be a significant problem, since for decades we have designed our architectures with centralized data storage, as shown in Figure 5- 6.


--- Page 98 ---


<center>Figure 5-6. Components using a centralized pool of dependencies </center>  


Centralized data storage is operationally convenient: it allows dedicated, specialized teams (DBAs, sysadmins) to maintain and fine- tune these complex systems, obscuring the complexity from the developers.  


In contrast, microservices favor embedding of all their dependencies, in order to achieve independent deployability. In such a scenario, every microservice manages and embeds its database, key- value store, search index, queue, etc. Then moving this microservice anywhere becomes trivial. This deployment would look like Figure 5- 7.


--- Page 99 ---


<center>Figure 5-7. Components using fully embedded, isolated dependencies </center>  


The postulate of wholesale embedding of (data storage) dependencies looks beautiful on the surface, but in practice it is extremely wasteful for all but the simplest use cases. It is obvious that you will have a very hard time embedding entire Cassandra, Oracle, or ElasticSearch clusters in each and every microservice you develop. Especially if you are far down the microservices journey and possibly have hundreds of microservices. This is just not doable. Neither is it necessary.


--- Page 100 ---

In reality, a microservice doesn't have to carry along every single dependency (such as a data storage system) in order to be mobile and freely move across the data centers. Let us explain.  


In his previous job, one of us (Irakli) traveled a lot for work. He'd acquired important tips for doing it efficiently—tips that he was completely indifferent to during his previous life as a casual traveler. As any frequent traveler will tell you, the most important rule for mobility is to keep your luggage light. You don't have to pack literally everything you may possibly need. For example, nobody packs shower- heads and towels on a business trip: you know you will find those at the hotel. If you know that the destination hotel has a convenience shop and your employer pays for incidentals, you don't even have to pack most toiletries. Irakli learned what he could count on being available "onsite" and what he needed to always bring with him. And, to pack light, he learned to limit his "dependencies" on a lot of things that were not needed as part of his packing routine.  


Likewise, the trick to microservice mobility is not packing everything but instead ensuring that the deployment destination provides heavy assets, such as database clusters, in a usable and auto- discoverable form at every destination where a microservice may be deployed. Microservices should be written so that they can quickly discover those assets upon deployment and start using them.  

  


Let's be clear: data sharing between microservices is still the ultimate no- no. Sharing data creates tight coupling between microservices, which kills their mobility. However, sharing a database cluster installation is absolutely OK, given that each microservice only accesses isolated, namespaced portions of it.  


## Pragmatic Mobility  


Figure 5- 8 shows what a proper, sophisticated microservices deployment should look like in practice.
