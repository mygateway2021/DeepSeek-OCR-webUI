--- Page 26 ---

for speed is only realistic if the cost of breaking the system is near zero. Most development environments are optimized for release speed, enabling the software developer to make multiple changes in as short a time as possible. On the other hand, most production environments are optimized for safety, restricting the rate of change to those releases that carry the minimum risk of damage.  


## At Scale  


On top of everything else, today's software architect needs to be able to "think big" when building applications. As we heard earlier in this chapter, the microservices style is rooted in the idea of solving the problems that arise when software gets too big. To build at scale means to build software that can continue to work when demand grows beyond our initial expectations. Systems that can work at scale don't break when under pressure; instead they incorporate built- in mechanisms to increase capacity in a safe way. This added dimension requires a special perspective to building software and is essential to the microservices way.  


## In Harmony  


Your life is filled with decisions that impact speed and safety. Not just in the software domain, but in most of your everyday life; how fast are you willing to drive a car to get where you need to be on time? How does that maximum speed change when there is someone else in the car with you? Is that number different if one of your passengers is a child? The need to balance these ideals is something you were probably taught at a young age and you are probably familiar with the well- worn proverb, "haste makes waste."  


We've found that all of the characteristics that we associate with microservice architecture (i.e., replaceability, decentralization, context- bound, message- based communication, modularity, etc.) have been employed by practitioners in pursuit of providing speed and safety at scale. This is the reason a universal characteristic- driven definition of microservices is unimportant—the real lessons are found in the practices successful companies have employed in pursuit of this balancing act.  


We don't want to give you the wrong idea—microservice architecture is not limited to a simple series of decisions regarding speed and safety of change. The microservices domain is actually fairly complex and will require you to understand a wide breadth of concepts that have a great depth of impact. If it was any other way, this would be a very short book.  


Instead, we introduce the microservices way in order to help you understand the essence of the microservices style. All of the significant properties and patterns that are commonly adopted for this style of architecture reflect attempts to deal with the interplay between these forces. The companies that do this best are the ones that find ways to allow both safety and speed of change to coexist. Organizations that succeed


--- Page 27 ---

with microservice architecture are able to maintain their system stability while increasing their change velocity. In other words, they created a harmony of speed and safety that works for their own context.  


The pursuit of this harmony should shape the adoption decisions you make for your own system. Throughout this book we will introduce principles and patterns that have helped companies provide great value to their business. It will be tempting to simply replicate the patterns in your own organizations in exactly the same way. But do your best to first pay attention to the impact of these types of changes on your own organization's harmony. We will do our best to provide you with enough information to connect those dots.  


It also means that you may not find your balance in the same way as other companies. We don't expect your organization to work the same as the ones we've highlighted in this book and we don't expect your microservices implementation to be the same either. Instead, we hope that focusing on the way that microservices applications are built will help you identify the parts that could work for you.  


## Summary  


In this chapter we introduced the original intent of the microservice architecture concept—to replace complex monolithic applications with software systems made of replaceable components. We also introduced some of the concerns that first- time implementers often have, along with some of the practical realities. Finally, we introduced the microservices way, a goal- driven approach to building adaptable, reliable software. The balance of speed and safety at scale is key to understanding the essence of microservices and will come up again throughout this book. In the next chapter we'll take a closer look at the goals of speed and safety in the context of actual microservice implementations.


--- Page 28 ---

# 1


--- Page 29 ---

# The Microservices Value Proposition  


The microservice architectural style was defined based on common patterns observed across a number of pioneering organizations. These organizations did not consciously implement a microservice architecture. They evolved to it in pursuit of specific goals.  


In this chapter, we will explore the common benefits of microservice architecture and how they drive the higher- order goals from Chapter 1—speed, safety, and scale; illustrate how the goals of microservice architecture deliver business value; define a maturity model for microservice architecture benefits and goals; and finally, apply this information using a goal- oriented approach to microservice architecture.  


To start with, let's survey the motivations of some early microservice adopters.  


## Microservice Architecture Benefits  


Why are organizations adopting microservices? What are the motivations and challenges? How can the leaders of these organizations tell that taking on the challenges of managing a collection of small, loosely coupled, independently deployable services is actually paying off for the company? What is the measure of success? Surveying the early adopters of microservices, we find that the answers to these questions vary quite a bit. However, some common themes emerge and tie back to the mantra of "balancing speed and safety at scale."  


Werner Vogels of Amazon describes the advantages of their architecture as follows:  


We can scale our operation independently, maintain unparalleled system availability, and introduce new services quickly without the need for massive reconfiguration.  


—Werner Vogels, Chief Technology Officer, Amazon Web Services


--- Page 30 ---

By focusing on scalability and component independence, Amazon has been able to increase their speed of delivery while also improving the safety—in the form of scalability and availability—of their environment.  


UK e- retailer Gilt is another early adopter of microservice architecture. Their Senior Vice President of Engineering, Adrian Trenaman, listed these resulting benefits in an InfoQ article:  


- Lessens dependencies between teams, resulting in faster code to production- Allows lots of initiatives to run in parallel- Supports multiple technologies/languages/frameworks- Enables graceful degradation of service- Promotes ease of innovation through disposable code—it is easy to fail and move on  


The first three points help speed up software development, through organizational alignment and independent deployability, as well as polyglotism. The last two points speak to a safe environment that facilitates replaceability of services.  


Social media pioneer Hootsuite has observed efficiency benefits in their microservice adoption based on the tunability of the system:  


Some services require high availability, but are low volume, and it's the opposite for other services. A microservice approach allows us to tune for both of these situations, whereas in a monolith it's all or nothing.  


—Beier Cai, Director of Software Development, Hootsuite  


With a more granular set of components, Hootsuite is able to independently manage their services and achieve greater efficiency.  


Clay Garrard, Senior Manager of Cloud Services at Disney, found that although there was work done to modularize the code base of their monolithic applications, the domain boundaries were not clear. This meant that small changes often led to large deployments.  


With microservices, we have reduced the time it takes to deploy a useful piece of code and also reduced the frequency of deploying code that hasn't changed. Ultimately we strive to be flexible in our interpretation of microservice architecture, using its strengths where we can, but realizing that the business does not care about how we achieve results, only that we move quickly with good quality and flexible design.  


—Clay Garrard, Senior Manager of Cloud Services, Disney  


The primary driver here is speed, as requested directly from the business. However, there is also an emphasis on safety—through independent deployability and testability—as well as future- proofing through composability.


--- Page 31 ---

Lastly, SoundCloud sought to solve the following problem when they evolved to a microservice architecture:  


The monolithic code base we had was so massive and so broad no one knew all of it. People had developed their own areas of expertise and custodianship around submodules of the application.  


- Phil Calçado, former Director of Engineering, SoundCloud  


By embracing microservices, they were able to overcome this issue and improve the comprehensibility of their software system.  


There are common goals and benefits that emerge from these implementation stories. The goal of improving software delivery speed as functional scope grows is realized through greater agility, higher composability, improved comprehensibility, independent service deployability, organizational alignment, and polyglotism. The goal of maintaining software system safety as scale increases is achieved through higher availability and resiliency, better efficiency, independent manageability and replaceability of components, increased runtime scalability, and more simplified testability. Now let's explore how these goals and benefits derive business value for organizations that employ microservice architecture.  


## Deriving Business Value  


Successful companies do not focus on increasing software delivery speed for its own sake. They do it because they are compelled by the speed of their business. Similarly, the level of safety implemented in an organization's software system should be tied to specific business objectives. Conversely, the safety measures must not get in the way of the speed unnecessarily. Balance is required.  


For each organization, that balance will be a function of its delivery speed, the safety of its systems, and the growth of the organization's functional scope and scale. Each organization will have its own balance. A media company that aims to reach the widest possible audience for its content may place a much higher value on delivery speed than a retail bank whose compliance requirements mandate specific measures around safety. Nonetheless, in an increasingly digital economy, more companies are recognizing that software development needs to become one of their core competencies.  


In this new business environment, where disruptive competitors can cross industry boundaries or start up from scratch seemingly overnight, fast software delivery is essential to staying ahead of the competition and achieving sustainable growth. In fact, each of the microservice architecture benefits that drive delivery speed contribute real business value:


--- Page 32 ---

- Agility allows organizations to deliver new products, functions, and features more quickly and pivot more easily if needed.- Composability reduces development time and provides a compound benefit through reusability over time.- Comprehensibility of the software system simplifies development planning, increases accuracy, and allows new resources to come up to speed more quickly.- Independent deployability of components gets new features into production more quickly and provides more flexible options for piloting and prototyping.- Organizational alignment of services to teams reduces ramp-up time and encourages teams to build more complex products and features iteratively.- Polyglotism permits the use of the right tools for the right task, thus accelerating technology introduction and increasing solution options.  


Likewise, digital native consumers expect always- on services and are not shy about changing corporate allegiances. Outages or lost information can cause them to take their business elsewhere. A safe software system is indispensable. The safety- aligned benefits discussed earlier also provide particular business value:  


- Greater efficiency in the software system reduces infrastructure costs and reduces the risk of capacity-related service outages.- Independent manageability contributes to improved efficiency, and also reduces the need for scheduled downtime.- Replaceability of components reduces the technical debt that can lead to aging, unreliable environments.- Stronger resilience and higher availability ensure a good customer experience.- Better runtime scalability allows the software system to grow or shrink with the business.- Improved testability allows the business to mitigate implementation risks.  


Clearly, microservice architecture has the potential to provide numerous business benefits. However, not every organization needs every benefit, and not every microservice architecture is capable of delivering all of them. With that in mind, let's now look at how an organization can combine its business objectives with the potential benefits of microservice architecture to tailor a goal- oriented approach.


--- Page 33 ---

## Defining a Goal-Oriented, Layered Approach  


In spite of the fact that microservice architecture was originally a reaction to the limitations of monolithic applications, there is a fair amount of guidance in the industry that says new applications should still be built as monoliths first. The thinking is that only through the creation and ownership of a monolith can the right service boundaries be identified. This path is certainly well trodden, given that early microservice adopters generally went through the process of unbundling their own monolithic applications. The "monolith first" approach also appears to follow Gall's Law, which states that, "A complex system that works is invariably found to have evolved from a simple system that worked." However, is a monolithic application architecture the only simple system starting point? Is it possible to start simple with a microservice architecture?  


In fact, the complexity of a software system is driven by its scale. Scale comes in the form of functional scope, operational magnitude, and change frequency. The first companies to use microservice architecture made the switch from monolithic applications once they passed a certain scale threshold. With the benefit of hindsight, and with an analysis of the common goals and benefits of microservice architecture, we can map out a set of layered characteristics to consider when adopting microservice architecture.  


## Modularized Microservice Architecture  


Modularity ... is to a technological economy what the division of labor is to a manufacturing one.  


- W. Brian Arthur, author of The Nature of Technology  


At its most basic level, microservice architecture is about breaking up an application or system into smaller parts. A software system that is modularized arbitrarily will obviously have some limitations, but there is still a potential upside. Network- accessible modularization facilitates automation and provides a concrete means of abstraction. Beyond that, some of the microservice architecture benefits discussed earlier already apply at this base layer.  


To help software delivery speed, modularized services are independently deployable. It is also possible to take a polyglot approach to tool and platform selection for individual services, regardless of what the service boundaries are. With respect to safety, services can be managed individually at this layer. Also, the abstracted service interfaces allow for more granular testing.  


This is the most technologically focused microservice architecture layer. In order to address this layer and achieve its associated benefits, you must establish a foundation for your microservice architecture. This will be discussed in detail in Chapter 4.


--- Page 34 ---

## Cohesive Microservice Architecture  


The greater the cohesion of individual modules in the system, the lower the coupling between modules will be.  


Larry Constantine and Edward Yourdon, authors of Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design  


The next layer to consider in your microservice architecture is the cohesion of services. In order to have a cohesive microservice architecture, it must already be modularized. Achieving service cohesion comes from defining the right service boundaries and analyzing the semantics of the system. The concept of domains is useful at this layer, whether they are business- oriented or defined by some other axis.  


A cohesive microservice architecture can enable software speed by aligning the system's services with the supporting organization's structure. It can also yield composable services that are permitted to change at the pace the business dictates, rather than through unnecessary dependencies. Reducing the dependencies of a system featuring cohesive services also facilitates replaceability of services. Moreover, service cohesion lessens the need for highly orchestrated message exchanges between components, thereby creating a more efficient system.  


It takes a synthesized view of business, technology, and organizational considerations to build a cohesive system. This can be addressed through service design, which is the focus of Chapter 5.  


## Systematized Microservice Architecture  


The key in making great and growable systems is much more to design how its modules communicate rather than what their internal properties and behaviors should be.1  


Alan Kay, 1998 email to the Squeak- dev list  


The final and most advanced layer to consider in a microservice architecture is its system elements. After breaking the system into pieces through modularization, and addressing the services' contents through cohesion, it is time to examine the interrelationships between the services. This is where the greatest level of complexity in the system needs to be addressed, but also where the biggest and longest- lasting benefits can be realized.


--- Page 35 ---

There are two ways speed of delivery is impacted in a systematized microservice architecture. Although a single service may be understandable even in a modularized microservice architecture, the overall software system is only comprehensible when the connectivity between services is known. Also, agility is only possible when the impacts of changes on the whole system can be identified and assessed rapidly. This applies on the safety side as well, where runtime scalability is concerned. Lastly, although individual components may be isolated and made resilient in a modularized or cohesive microservice architecture, the system availability is not assured unless the interdependencies of the components are understood.  


Dealing with complex systems requires a careful approach based on influence versus control. The system aspects of microservice architecture are discussed in detail in Chapters 3 and 6.  


## Maturity Model for Microservice Architecture Goals and Benefits  


These layered characteristics—modularized, cohesive, and systematized—help to define a maturity model that serves a number of purposes. First, it classifies the benefits according to phase and goal (speed or safety) as discussed previously. Secondly, it illustrates the relative impact and priority of benefits as scale and complexity increase. Lastly, it shows the activities needed to address each architectural phase. This maturity model is depicted in Figure 2- 1.  


Note that an organization's microservice architecture can be at different phases for different goals. Many companies have become systematized in their approach to safety—through automation and other operational considerations—without seeking the speed- aligned system- level benefits. The point of this model is not for every organization to achieve systematized actualization with their microservice architecture. Rather, the model is meant to clarify goals and benefits in order to help organizations focus their microservice strategies and prepare for what could come next.


--- Page 36 ---


<center>Figure 2-1. A maturity model for microservice architecture goals and benefits </center>  


## Applying the Goal-Oriented, Layered Approach  


Now we have a good understanding of how a microservice architecture can bring value to an organization, and a model for understanding what characteristics can bring what goals and benefits at what stage of adoption. But what about your organization? What are your business goals? What problems do you need to solve? It is a common misstep to start down the microservices path for its own sake without thinking about the specific benefits you are targeting. In other cases, some organizations aim for a high- level goal and then only implement one aspect of microservices while ignoring its founding conditions. For example, an organization with a high- level divide between development and operations—an organizational red flag—might execute a containerization strategy on their existing applications and then wonder why they didn't speed up their software development sufficiently. A broad perspective is needed.  


To begin with, define the high- level business objectives you want to accomplish, and then weigh these against the dual goals of speed and safety. Within that context, con


--- Page 37 ---

sider the distinct benefits you are targeting. You can then use the maturity model to determine the complexity of the goal, and identify the best approach to achieve it.  


Holger Reinhardt, CTO of the German digital media group Haufe- Lexware, provides an example of a goal- oriented approach in action. One of Haufe's initial attempts at microservice architecture was on their monolithic service platform, which included functions such as user management and license management. The first attempt was explicitly focused on changing the architecture from monolith to service- enabled software system. The results were not positive. However, when they evaluated the main issues with the application—particularly the operational inefficiencies around it—they changed their approach from refactoring the existing architecture to automating the problematic deployment process. Through a small investment, they were able to take their service platform deployment downtime from 5 days to 30 minutes. Their next iteration will focus on reducing QA time through automation and a switch in methodology from white- box to black- box testing. Following these methodological changes, they will identify the domains in their monolithic application that require the greatest speed of innovation and unbundle those first. By taking an iterative approach tied to clear goals, they are able to measure success quickly and change course if needed.  


## Summary  


This chapter has covered a lot of ground that should help you define a strategy for applying a microservice architecture in your organization. We first analyzed the reasons the early adopters of microservice architecture chose this style. Next, we looked into the common goals and benefits of microservices, how they relate to each other, and what business objectives they can drive. Lastly, we defined a maturity model that can be used to target the right goals and benefits for applying a microservice architecture in your organization. You should now be ready to roll up your sleeves and learn a design- based approach to microservice architecture.


--- Page 38 ---

# 1


--- Page 39 ---

# Microservice Design Principles  


## The Flaw of Averages  


In the 1950s, the US Air Force launched a study into the causes of pilot errors and part of that study focused on the physical dimensions of the pilots and their cockpit control systems. The cockpits had been initially designed based on assumed physical averages of pilots and it was assumed that pilots had grown larger over time and that the design needed to be updated.  

  


This story comes from the book The End of Average by Todd Rose (Harper Collins, 2016). Rose has given a TEDx talk on the subject of averages and is a leading proponent of an interdisciplinary field called "The Science of the Individual".  


It fell to 23- year- old Lt. Gilbert Daniels to lead the painstaking process of carefully measuring over 4,000 pilots on 140 different physical dimensions and then analyze the results. Along the way, Daniels got the idea to go beyond the initial plan to compute the averages of all 140 dimensions in order to construct what the military deemed the "average pilot." Daniels wanted to know just how many of the 4,000 pilots he had measured actually were average—i.e., how many fit the computed values the military was aiming to use to redesign the airplane cockpits?  


By taking just ten of the many dimensions he was working with (height, chest size, sleeve length, etc.), Daniels constructed what he defined as the average pilot. Daniels also posited that anyone who fell within a \(30\%\) range of the target number for a dimension would be included in his list of average pilots. For example, the average


--- Page 40 ---

pilot height turned out to be \(5^{\prime}9^{\prime \prime}\) . So, for Daniels, anyone who measured \(5^{\prime}7^{\prime \prime}\) to \(5^{\prime}11^{\prime \prime}\) would be counted as average for height. Daniels then proceeded to check each of his 4,000 subjects to discover just how many of them would score within the average for every dimension. He was looking for all the pilots who could be considered completely average. To everyone's surprise, the total count was zero. There was not one single pilot that fell within \(30\%\) of the average for all ten dimensions. As Daniels wrote in his paper The "Average Man"?  


As an abstract representation of a mythical individual most representative of a given population, the average man is convenient to grasp in our minds. Unfortunately he doesn't exist.  


—Lt. Gilbert Daniels, The "Average Man"?  


It turns out there is no such thing as an average pilot. Designing a cockpit for the average pilot results in a cockpit configuration that fits no one. Intuitively, this makes sense to most of us. While averages are helpful when looking for trends in a group, the resulting "profile" from this group does not exist in real life. Averages help us focus on trends or broad strokes but do not describe any actual existing examples.  


The reason for this difference between real pilots and the average pilot can be summed up in what Rose calls the principle of jaggedness. When measuring individuals on a multidimensional set of criteria (height, arm length, girth, hand size, and so forth), there are so many varying combinations that no one individual is likely to exhibit the average value for all dimensions. And designing for an individual that exhibits all those averages will result in a poor fit for every actual person.  


This principle of jaggedness is important to keep in mind when designing software architecture, too. Designing for an ideal or average is likely to result in a model that fits no single purpose well. Guidance that calls out specific measurements of an ideal microservice or canonical model for microservices is likely to have traits that fit no existing microservice implementation. Ideals are just that—not realities.  


The solution that eventually worked for the US Air Force was to incorporate variability into the design of airplane cockpits. For example, creating an adjustable seat, the ability to modify the tilt and length of the steering column, and moving the foot pedals forward or back are all examples of designing in variability. This works because the exact dimensions of any single element in the design are not as important as the ability to identify the important dimensions that need to support variability.


--- Page 41 ---

# Designing Microservice Systems  


So far we've learned that companies building applications in the microservices way do more than just implement small components. We now know that there isn't a strict definition for what constitutes a microservice architecture. Instead, the focus is on building applications that balance speed and safety at scale, primarily through replaceability. Throughout the remaining chapters of this book we will dive deeper into the details of microservice adoption. But considering what you've learned about microservices systems so far, one thing should be clear—there are a lot of moving parts to consider. The hallmark of a microservice architecture might be smaller services, but following the microservices way will require you to think big. You'll need to tune your culture, organization, architecture, interfaces, and services in just the right way to gain the balance of speed and safety at scale.  


In this chapter we will lay the groundwork for thinking about your application in a way that helps you unlock the potential value of a microservices system. The concepts introduced are rooted in some pretty big domains: design, complexity, and systems thinking. But you don't need to be an expert in any of those fields to be a good microservice designer. Instead, we will highlight a model- driven way of thinking about your application that encapsulates the essential parts of complexity and systems thinking. Finally, at the end of this chapter we will introduce an example of a design process that can help promote a design- driven approach to microservices implementation.  


## The Systems Approach to Microservices  


We've found that many first- time adopters of microservices tend to focus on the services that need to be built. But in order to develop applications in the microservices way, you'll need to conceptualize the design as much more than isolated, individual service designs. That doesn't mean that the design of services can be ignored—just


--- Page 42 ---

like cars and pedestrians are essential to a traffic system, services are the key ingredient of a microservice system. But thinking in services terms alone isn't enough; instead you'll need to consider how all aspects of the system can work together to form an emergent behavior. Emergent behaviors are the ones that are greater than the sum of their parts and for a microservices application this includes the runtime behavior that emerges when we connect individual services together and the organizational behavior that gets us there.  

  


Emergence is an essential part of the science of complexity and is a key indicator of system complexity. Complexity scientist Melanie Mitchell (known for her work at the Santa Fe Institute) often uses ant colonies to illustrate emergence and complexity: predicting the behavior of a single ant is trivial, but predicting the behavior of an entire ant colony is much more difficult.  


A microservices system encompasses all of the things about your organization that are related to the application it produces. This means that the structure of your organization, the people who work there, the way they work, and the outputs they produce are all important system factors. Equally important are runtime architectural elements such as service coordination, error handling, and operational practices. In addition to the wide breadth of subject matter that you need to consider, there is the additional challenge that all of these elements are interconnected—a change to one part of the system can have an unforeseen impact on another part. For example, a change to the size of an implementation team can have a profound impact on the work that the implementation team produces.  


If you implement the right decisions at the right times you can influence the behavior of the system and produce the behaviors you want. But that is often easier said than done. Grappling with all of these system elements at the same time is difficult. In fact, you might find it especially challenging to conceptualize all of the moving parts of the microservice system in your head. What we are learning is that microservice systems are complex!  


Complexity scientists face a similar challenge when they work with complex systems. With all of the interconnected parts and the complex emergence that results, it is very difficult to understand how the parts work together. In particular, it is difficult to predict the results that can arise from a change to the system. So, they do what scientists have always done—they develop a model.  


The models mathematicians develop to study complex systems allow them to more accurately understand and predict the behavior of a system. But this is a field in its infancy and the models they produce tend to be very complicated. We don't expect you to understand the mathematics of complexity, nor do we think it will be particularly helpful in creating better microservice applications. But we do believe that a
