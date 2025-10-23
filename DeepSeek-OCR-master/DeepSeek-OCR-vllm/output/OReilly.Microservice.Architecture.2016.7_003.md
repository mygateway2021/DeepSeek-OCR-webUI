--- Page 51 ---

Vision Zero goal of zero traffic- related fatalities) provides the most clarity and has a higher likelihood of succeeding.  


For example, a financial information system might be optimized for reliability and security above all other factors. That doesn't mean that changeability, usability, and other system qualities are unimportant—it simply means that the designers will always make decisions that favor security and reliability above all other things.  


In Chapter 4 we will identify the goals that we have most commonly seen among companies that have embraced the microservices way and the principles that help support them.  

  


It is possible that you may need to change your optimization goals at some point in the lifetime of your application. That is OK; it just means that you need to follow the design process and implement small changes to guide your system toward the new goal. If the goal change is quite different from your original design goal this may take some time. If the optimization goal is radically different from your original goal, you may even create a new system design entirely.  


## Development Principles  


Underpinning a system optimization goal is a set of principles. Principles outline the general policies, constraints, and ideals that should be applied universally to the actors within the system to guide decision- making and behavior. The best designed principles are simply stated, easy to understand, and have a profound impact on the system they act upon.  


In Chapter 4 we will look at some of the principles that Netflix employs toward its optimization goals.  


## Sketch the System Design  


If you find yourself building the application in a greenfield environment with no existing organization or solution architecture in place, it is important that you establish a good starting point for your system design. You won't be able to create the perfect system on your first try and you aren't likely to have the time or information to do that anyway. Instead, a good approach is to sketch the important parts of your system design for the purposes of evaluation and iteration.  


How you do this is entirely up to you. There is a wealth of modeling and communication tools available to conceptualize organizational and solution architectures; choose the ones that work well for you. But the value of this step in the design process is to serialize some of the abstract concepts from your head into a tangible form that can


--- Page 52 ---

be evaluated. The goal of a sketching exercise is to continually improve the design until you are comfortable moving forward.  


The goal is to sketch out the core parts of your system, including organizational structure (how big are the teams? what is the direction of authority? who is on the team?), the solution architecture (how are services organized? what infrastructure must be in place?), the service design (what outputs? how big?), and the processes and tools (how do services get deployed? what tools are necessary?). You should evaluate these decisions against the goals and principles you've outlined earlier. Will your system foster those goals? Do the principles make sense? Do the principles need to change? Does the system design need to change?  


Sketching is powerful when the risk of starting over is small. Good sketches are easy to make and easy to destroy, so avoid modeling your system in a way that requires a heavy investment of time or effort. The more effort it takes to sketch your system the less likely you are to throw it away. At this early stage of system design, change should be cheap.  


Most importantly, remember that the purpose of the iterative sketching stage is to participate in the process of designing. The goal is to form new ideas, consider the impact of proposed designs, and experiment in a safe way. The goal is not to create a set of beautiful design documents or prescriptive plans.  


## Implement, Observe, and Adjust  


Bad designers make assumptions about how a system works, apply changes in the hope that it will produce desired behavior, and call it a day. Good designers make small system changes, assess the impact of those changes, and continually prod the system behavior toward a desired outcome. But a good design process is predicated on your ability to get feedback from the system you are designing. This is actually much more difficult than it sounds—the impact of a change to one small part of the system may result in a ripple of changes that impact other parts of your system with low visibility.  


The perfect microservice system provides perfect information about all aspects of the system across all the domains of culture, organization, solution architecture, services, and process. Of course, this is unrealistic. It is more realistic to gain essential visibility into our system by identifying a few key measurements that give us the most valuable information about system behavior. In organizational design, this type of metric is known as a key performance indicator (KPI). The challenge for the microservice designer is to identify the right ones.  


Gathering information about your system by identifying KPIs is useful, but being able to utilize those metrics to predict future behavior is incredibly valuable. One of the challenges that all system designers face is the uncertainty about the future. With per


--- Page 53 ---

fect information about how our system might need to change we could build boundaries in exactly the right places and make perfect decisions about the size of our services and teams.  


Without perfect information we are forced to make assumptions. Designers working on existing applications can observe the existing and past behavior of the system to identify patterns—components that change often, requirements that are always in flux, and services that can expect high usage. But designers who are working on new applications often have very little information to start with—the only way to identify the brittle points of the application is to ship the product and see what happens.  


The risk of making poor decisions is that we steer the system in a direction that increases our "technical debt" (i.e., the future cost of addressing a technical deficiency). If we go too far along the wrong path we risk producing a system that becomes too expensive to change, so we give up.  


The classic microservices example of this is the cautionary tale of the "monolith." A team creates an initial release of an application when the feature set is small and the componentry has low complexity. Over time, the feature set grows and the complexity of the deployed application grows, making change ever more difficult. At this point, the team agrees that the application needs to be redesigned and modularized to improve its changeability. But the redesign work is continually deferred because the cost of that work is too high and difficult to justify.  


At the other end of the scale is a system that is so overdesigned and overengineered for future flexibility that it becomes impractical. An incredibly complex, adaptable system that is built for massive amounts of change that never seems to happen.  


Rather than trying to predict the future, a good microservices designer examines the current state and makes small, measurable changes to the system. This is a bit like taking a wrong turn on a long road trip—if you don't know that you've made a mistake you might not find out you're going the wrong way until it is too late to turn back. But if you have a navigator with you, they may inform you right away and you can take corrective action.  


When you are driving a car, taking a corrective action to steer your car back in the right direction is fairly straightforward, but what should a corrective action look like in a microservices system? A system that is designed with a high degree of visibility might give us a lot of information about what is happening, but if the cost of changing the system is too high we won't be able to make any course corrections. This problem of costly change presents itself when you need special permission, additional funds, more people, or more time to make the changes you want to the system.


--- Page 54 ---

So, in order to design a microservice system that is dynamic you'll need to identify the right KPIs, be able to interpret the data, and make small, cheap changes to the system that can guide you back on the right course. This is only possible if the right organization, culture, processes, and system architecture are in place to make it cheap and easy to do so.  


## The Microservices System Designer  


Throughout this chapter we've referred to the work that the microservices system designer needs to undertake. But we haven't identified who this system designer is or where she might fit into your existing organization.  


To be most effective, the microservices system designer should be able to enact change to a wide array of system concerns. We've already identified that organization, culture, processes, solution architecture, and services are significant concerns for the system designer. But the boundaries of this system haven't been properly identified.  


You could decide that the system boundaries should mirror the boundaries of the company. This means that the changes you enact could have a broad- reaching impact. Alternatively, you could focus on a particular team or division within the company and build a system that aligns with the parent company's strategic goals. In fact, this type of nested set of systems is fairly common and we see it all around us in the physical world (e.g., consider the complex systems of the human brain, the human, and the human community).  


Ultimately, the microservices system designer or software system designer is responsible for all the elements of the bounded system. The implication is that there is a world within the system and world outside of these borders. The system designer's task is to introduce small changes within the system in order to produce behavior that will align with the desired goal. Not very different than the traditional executive, manager, or CIO's mission.  


But outside of these managerial positions there aren't many roles in the technology domain that allow for this systematic solution view. Instead, responsibilities are segregated among specialists who may not share the same objectives: The solution architect focuses on the coordination of services, the team manager focuses on the people, and the service developer focuses on the service design. We believe that someone or some team must be responsible for the holistic view of the entire system for a microservices system to succeed.  


## Summary  


In this chapter we introduced the microservices system model and a generic design process for influencing the system. Throughout the rest of the book we will be diving into each of the model's domains in much greater detail. Remember that each of the


--- Page 55 ---

decisions you make about organizational design, culture, solution architecture, process, and automation can result in unintended consequences to the system as a whole. Always maintain your holistic perspective and continue to observe and adjust as required.


--- Page 56 ---

# 1


--- Page 57 ---

# Establishing a Foundation  


Now that we have a general model for establishing complex systems, we also need to come up with goals, principles, and guidelines for actually designing the system. A common challenge in creating a microservice architecture for your company is finding the right set of principles to govern the work. One easy answer is to just copy someone else's successful model—to adopt the same goals, principles, and implementation patterns they used. This can work if the company you decide to mimic has the same general goals as your company. But that is not often the case. Each company has a unique set of priorities, culture, and customer challenges and simply taking on a fully formed model from some other organization is not likely to get you where you need to go.  


In this chapter, we'll review a capabilities model for microservices environments. We'll also introduce the platform that represents the tools and services you provide your developer and operations teams to allow them to meet their objectives. The quality and fit of these tools has an important impact on your teams' productivity. We will also review how company culture—including team size—can affect the resulting output of your teams.  


Following that, we'll focus on teams themselves; their size, communication modes, and the level of freedom they have to innovate within their own scope of work. There is quite a bit of research that shows that varying the size of the team has a direct impact on the quality of the code that team produces. And establishing support for creative thinking is another common trait for many of the companies we talked to in preparation for this book.  


By the time you complete this chapter, you should have a better understanding of the role goals and principles have in establishing a successful microservice environment and how you can use platforms and innovation culture to improve the general output or your teams.


--- Page 58 ---

## Goals and Principles  


Regardless of the software architecture style you employ, it is important to have some overall goals and principles to help inform your design choices and guide the implementation efforts. This is especially true in companies where a higher degree of autonomy is provided to developer teams. The more autonomy you allow, the more guidance and context you need to provide to those teams.  


In this section, we'll take a look at some general goals for a microservice architecture and some example principles. Along the way we'll list our own suggested principles for you to consider.  


## Goals for the Microservices Way  


It is a good idea to have a set of high- level goals to use as a guide when making decisions about what to do and how to go about doing it. We've already introduced our ultimate goal in building applications in the microservices way: finding the right harmony of speed and safety at scale. This overarching goal gives you a destination to aim for and given enough time, iterations, and persistence, will allow you to build a system that hits the right notes for your own organization.  


There is of course a glaring problem with this strategy—it might take a very long time for you to find that perfect harmony of speed and safety at scale if you are starting from scratch. But thanks to the efforts of generations of technologists we have access to proven methods for boosting both speed and safety. So, you don't need to reinvent established software development practices. Instead, you can experiment with the parameters of those practices.  


From our research, we've been able to distill four specific goals that lead to practices that aid both safety and speed of change. These goals aren't unique to microservice architecture, but they are useful in shaping your journey. Here are the four goals to consider:  


1. Reduce Cost: Will this reduce overall cost of designing, implementing, and maintaining IT services?  
2. Increase Release Speed: Will this increase the speed at which my team can get from idea to deployment of services?  
3. Improve Resilience: Will this improve the resilience of our service network?  
4. Enable Visibility: Does this help me better see what is going on in my service network?  


Let's look at these in a bit more depth.


--- Page 59 ---

## Reduce cost  


Reduce costThe ability to reduce the cost of designing, implementing, and deploying services allows you more flexibility when deciding whether to create a service at all. For example, if the work of creating a new service component includes three months of design and review, six months of coding and testing, and two more weeks to get into production, that's a very high cost—one that you would likely think very carefully about before starting. However, if creating a new service component takes only a matter of a few weeks, you might be more likely to build the component and see if it can help solve an important problem. Reducing costs can increase your agility because it makes it more likely that you'll experiment with new ideas.  


In the operations world, reducing costs was achieved by virtualizing hardware. By making the cost of a "server" almost trivial, it makes it more likely that you can spin up a bunch of servers in order to experiment with load testing, how a component will behave when interacting with others, and so on. For microservices, this means coming up with ways to reduce the cost of coding and connecting services together. Templated component stubs, standardized data- passing formats, and universal interfaces are all examples of reducing the costs of coding and connecting service components.  


## Increase release speed  


Increasing the speed of the "from design to deploy" cycle is another common goal. A more useful way to view this goal is that you want to shorten the time between idea and deployment. Sometimes, you don't need to "go faster," you just need to take a shortcut. When you can get from idea to running example quickly, you have the chance to get feedback early, to learn from mistakes, and iterate on the design more often before a final production release. Like the goal of reducing costs, the ability to increase speed can also lower the risk for attempting new product ideas or even things as simple as new, more efficient data- handling routines.  


One place where you can increase speed is in the deployment process. By automating important elements of the deployment cycle, you can speed up the whole process of getting services into production. Some of the companies we talked with for this book spend a great deal of time building a highly effective deployment pipeline for their organization. Many of them have such a well- designed deployment model that they release to production multiple times a day (sometimes over 100 times a day!). Automating release can go a long way toward increasing the speed of your microservice implementation.  


## Improve resilience  


Improve resilienceNo matter the speed or cost of solutions, it is also important to build systems that can "stand up" to unexpected failures. In other words, systems that don't crash, even when errors occur. When you have an overall system approach (not just focused on a single


--- Page 60 ---

component or solution) you can aim for creating resilient systems. This goal is often much more reasonable than trying to create a single component that is totally free of bugs or errors. In fact, creating a component that will have zero bugs is often impossible and sometimes simply not worth the time and money it takes to try.  


One of the ways DevOps practices has focused on improving resilience is through the use of automated testing. By making testing part of the build process, the tests are constantly run against checked- in code, which increases the chances of finding errors in the code. This covers the code, but not the errors that could occur at runtime. There are companies that run what they call end- to- end tests before releasing to production but many companies rely on a practice that Jez Humble calls blue- green deployment. In this case, a new release is placed in production with a small subset of users and, if all goes well during a monitoring phase, more users are routed to the new release until the full userbase is on the new release. If any problems are encountered during this phased rollout, the users can all be returned to the previous release until problems are resolved and the process starts again.  


## Enable visibility  


Another key goal should be to enable runtime visibility. In other words, improve the ability of stakeholders to see and understand what is going on in the system. There is a good set of tools for enabling visibility during the coding process. We often get reports on the coding backlog, how many builds were created, the number of bugs in the system versus bug completed, and so on. But we also need visibility into the runtime system.  


The DevOps practices of logging and monitoring are great examples of this level of runtime visibility. Etsy's John Allspaw has said, "If it moves graph it. If it matters, alert on it". Most effort to date has been to log and monitor operation- level metrics (memory, storage, throughput, etc.). However, there are some monitoring tools that can take action when things go badly (e.g., reroute traffic).  


## Trade-offs  


Each of these are important goals and sometimes they are competing goals. There are trade- offs to consider. You might be able to reduce your overall costs, but it might adversely affect runtime resilience. Or, you might be able to speed up deployment but that might mean you lose track of what services are running in production and reduce visibility into the larger service network. In the end, you'll need to balance various goals and find the right mix for your organization.  


Your organization may have some other high- level goals you want to consider and document. Whatever these turn out to be, one of the next things you need to do is convert those goals into a set of actionable principles.


--- Page 61 ---

## Operating Principles  


Operating PrinciplesAlong with a set of goals for a microservice approach, it is important to have a set of principles. Unlike goals, which are general, principles offer more concrete guidance on how to act in order to achieve those goals. Principles are not rules—they don't set out required elements. Instead, they offer examples on how to act in identifiable situations. Principles can also be used to inform best practices. Many of the organizations we looked at when doing research have their own set of principles within their company.  


## Netflix  


NetflixOne company that has been open about their own journey toward creating a successful microservice architecture is Netflix. In 2013, Adrian Cockcroft, Netflix's Cloud Architect, presented a day- long workshop on Netflix's cloud architecture and operating principles.1 We'll highlight a few of them here.  

  


We've called out just a few of Netflix's principles here. You can learn more about these and other key elements of the Netflix operating model by checking out the slides and video from Adrian Cockcroft's 2013 talk, "Cloud Native Architecture." From 2014 on, Adrian left Netflix and has continued presenting on microservices, DevOps, and related technology issues. You can find these presentations and videos in a different SlideShare account.  


## Antifragility  


AntifragilityNetflix works to strengthen their internal systems so that they can withstand unexpected problems. "The point of antifragility is that you always want a bit of stress in your system to make it stronger." There are several things Netflix does to promote this, including their "Simian Army" set of tools, which "enforce architectural principles, induce various kinds of failures, and test our ability to survive them". Software has bugs, operators make mistakes, and hardware fails. By creating failures in production under controlled conditions, developers are incentivized to learn to build more robust systems. Error reporting and recovery systems are regularly tested, and real failures are handled with minimal drama and customer impact.  


## Immutability  


ImmutabilityCockcroft says the principle of immutability is used at Netflix to assert that autoscaled groups of service instances are stateless and identical, which enables Net


--- Page 62 ---

flix's system to "scale horizontally." The Chaos Monkey, a member of the Simian Army, removes instances regularly to enforce the immutable stateless service principle. Another related technique is the use of "Red/Black pushes". Although each released component is immutable, a new version of the service is introduced alongside the old version, on new instances, then traffic is redirected from old to new. After waiting to be sure all is well, the old instances are terminated.  


## Separation of Concerns  


The Netflix microservice architecture arises because of separation of concerns (SoC) in the engineering team organization. Each team owns a group of services. They own building, operating, and evolving those services, and present a stable agreed interface and service level agreement to the consumers of those services. Invoking Conway's law, an organization structured with independent self- contained cells of engineers will naturally build what is now called a microservice architecture.  


So these are the three key principles: antifragility, immutability, and separation of concerns. Some of these same ideas were expressed in slightly different terms in 1978 by Douglas McIlroy when describing the Unix operating system.  


## Unix  


A succinct set of software architecture principles appears in the foreword for the 1978 edition of Bell Labs' "UNIX Timesharing System" documentation. The four points (listed next) were offered as a set of "maxims that have gained currency among the builders and users of the Unix system."  


Here is the list Douglas McIlroy and his colleagues called out:  


1. Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new features.  
2. Expect the output of every program to become the input to another, as yet unknown, program. Don't clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don't insist on interactive input.  
3. Design and build software, even operating systems, to be tried early, ideally within weeks. Don't hesitate to throw away the clumsy parts and rebuild them.  
4. Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you've finished using them.  


One of the interesting things about these four principles is that they offer general guidance on how to think about writing software. Phrases like "do one thing well" and "build software ... to be tried early" can lead developers to adopt what is known in the Unix world as "The Rule of Parsimony" when writing code ("only write a big pro


--- Page 63 ---

gram when nothing else will do"). This along with other Unix rules provides developers with a set of guidelines for which programming languages or libraries to use. These principles are also meant to shape developers' thinking.  


## Suggested principles  


Having a set of principles to guide software developers and architects makes a lot of sense. As we learned from the story at the top of this chapter, the jaggedness principle applies here as well. There is no one set of principles that matches every company. Each organization needs to create a set that works for their company.  


With this in mind, we offer a set of eight principles that reflects aspects of the other examples we've looked at so far. You can use these as starter material in putting together your own unique set for your company, or tune these until they fit.  


## Do one thing well  


Many microservice implementations adopt the essential message—"do one thing well," which leads to the challenge of deciding what constitutes "one thing" in your implementation. For some, "one thing" is managing user accounts. For others, "one thing" is finding a single user record. We'll get a chance to talk about how they decide where these types of boundaries are drawn for your organization in Chapter 5.  


## Build afresh  


The second part of McIlroy's first principle ("build afresh") is also important. Part of the Unix philosophy is to create a collection of powerful tools that are predictable and consistent over a long period of time. It is worth considering this as an additional principle when implementing microservices. It may be better to build a new microservice component rather than attempt to take an existing component already in production and change it to do additional work. This also maps to Netflix's immutability principle.  


## Expect output to become input  


Another important principle for Unix developers is the notion that one program's output is another program's input. For Unix systems, this leads to reliance on text strings as the primary data- passing medium. On the Web, the data- passing medium is the media type (HTML, HAL, Siren, Collection+JSON, etc.). In some cases, you can even use HTTP's content- negotiation feature to allow API providers and consumers to decide for themselves at runtime which format will be used to pass data.  


## Don't insist on interactive input  


In the Unix world, there is a desire to create scripts that tie a number of command- line tools together to create a "solution." This means humans don't need to be engaged every step of the way—the scripts handle both the input and


--- Page 64 ---

the output on their own. Reducing the need for human interaction increases the likelihood that the component can be used in unexpected ways.  


Human interaction isn't something that microservice components need to deal with at runtime. But when we expand our scope of focus to the microservice system, it's easy to find countless human interactions that could benefit from this principle. Reducing the dependency on human interaction in the software development process can go a long way toward increasing the speed at which change occurs.  


## Try early  


Adopting the point of view that your microservice components should be "tried early" fits well with the notion of continuous delivery and the desire to have speed as a goal for your implementations. Another advantage of this "try early" principle is you will learn your mistakes early. It turns out "try early" is also a way to encourage teams to get in the habit of releasing early and often. The earlier you release (even when that release is to a test environment), the earlier you get feedback and the quicker you can improve.  


## Don't hesitate to throw it away  


This is a difficult one for some developers. Being willing to throw something away can be hard when you've spent a great deal of time and effort building a component. However, when you adopt the "try early" principle, throwing away the early attempts is easier.  


It is also important to consider this "throw it away" principle for components that have been running in production for a long time. Over time, components that did an important job may no longer be needed. You may have applied the "build afresh" principle and replaced this component with one that does the job better. It may be the case that the "one thing" that component does is simply no longer needed. The important thing is to be willing to throw away a component when it no longer serves its intended purpose.  


## Toolmaking  


The "use tools" principle covers the notion that, when working to build a solution, you sometimes need to build the "right tool" for the job. One of the important elements in the developmental history of humans was the ability to create tools. These tools were created in order to reach a goal. In other words, tools are a means, not an end. This is also an important principle for microservice architecture.  


While doing research for this book, we found several examples of companies that created their own developer and deployment tool chains in order to improve their overall developer experience. Sometimes these tools are built from existing open source software projects. Sometimes the tools are, themselves, passed into


--- Page 65 ---

open source so that others can use them and contribute to improving and maintaining them. The important element here is to recognize that, in some cases, you may need to divert from building your solution and spend some time building tools to help you build that solution.  


## Platforms  


Along with a set of general goals and concrete principles, you'll need tangible tools to make them real—a platform with which to make your microservice environment a reality. From a microservice architecture perspective, good platforms increase the harmonic balance between speed and safety of change at scale. We typically think about speed and safety as opposing properties that require a trade- off to be made but the right tooling and automation give you an opportunity to cheat the trade- off.  


For example, the principle of immutability primarily improves the safety of changes that are made to the system. There is also an inherent release cost for immutability as each deployable unit needs its own associated release mechanisms, infrastructure, and management. On its own, the added cost can reduce the speed at which changes can be made. However, the introduction of containerization tools like Docker make independent deployability easy and greatly reduce the associated costs. When immutability is combined with containerization, both speed and safety of changes are optimized, which may explain the rapid adoption of Docker in large organizations.  


With a platform we pass from the conceptual world to the actual world. The good news is that there are many examples of companies establishing—and even sharing—their microservice platforms. The challenge is that it seems every company is doing this their own way, which presents some choices to anyone who wants to build their own microservice environment. Do you just select one of the existing OSS platforms? Do you try to purchase one? Build one from scratch?  


It would be a mistake to just select one of the popular company's platforms and adopt it without careful consideration. Does this company provide the same types of services that mine does? Does this company optimize for the same things that mine will? Do we have similar staffing and training environments? Are our target customers similar (priorities, skills, desired outcomes, etc.)?  


Instead of focusing on a single existing company's platform, we'll look at a general model for microservice platforms. One of the ones we like was described by Adrian Cockcroft in 2014. He outlined a set of capabilities that he said all microservice implementations need to deal with, which he called "microservice concerns." We will divide them into two groups: shared capabilities and local capabilities.


--- Page 66 ---

## Shared Capabilities  


Shared CapabilitiesIt's common in large enterprises to create a shared set of services for everyone to use. These are typically centered around the common infrastructure for the organization. For example, anything that deals with hardware (actual or virtual) falls into this category. Common database technologies (MySQL, Cassandra, etc.) and other software- implemented infrastructure is another example of shared services.  


Shared capabilities are platform services that all teams use. These are standardized things like container technology, policy enforcement, service orchestration/interop, and data storage services. Even in large organizations it makes sense to narrow the choices for these elements in order to limit complexity and gain cost efficiencies. Essentially, these are all services that are provided to every team in the organization.  

  


It is important to note that shared services does not mean shared instance or shared data. Just because all the teams use a single type of data storage technology (e.g., Datomic, Mongo, Cassandra, and MySQL) does not mean they all use the same running instance of the data storage and all read and write from the same tables.  


While shared capabilities offer potential cost savings they are ultimately rooted in the microservices goal of change safety. Organizations that highly value safety of changes are more likely to deploy centralized shared capabilities that can offer consistent, predictable results. On the other hand, organizations that desire speed at all costs are likely to avoid shared components as much as possible as it has the potential to inhibit the speed at which decentralized change can be introduced. In these speed- centric companies, capability reuse is less important than speed of delivery. As with all things in the microservices way you will need to experiment with different forms of shared capabilities to see what works best for your unique context.  


The following is a quick rundown of what shared services platforms usually provide:  


## Hardware services  


All organizations deal with the work of deploying OS- and protocol- level software infrastructure. In some companies there is a team of people who are charged with accepting shipments of hardware (e.g., 1- U servers), populating those machines with a baseline OS and common software for monitoring, health checks, etc., and then placing that completed unit into a rack in the "server room" ready for use by application teams.  


Another approach is to virtualize the OS and baseline software package as a virtual machine (VM). VMs like Amazon's EC2 and VMWare's hypervisors are examples of this technology. VMs make it possible to automate most of the work of populating a "new machine" and placing it into production.


--- Page 67 ---

A more recent trend is the use of containers to solve this problem. Docker is the most popular player in this field. We'll talk more about Docker in Chapter 6. But there are others. CoreOS Rocket is one. By the time you read this there may be many more container products in the space.  


## Code management, testing, and deployment  


Once you have running servers as targets, you can deploy application code to them. That's where code management (e.g., source control and review), testing, and (eventually) deployment come in. There are quite a few options for all these services and some of them are tied to the developer environment, especially testing.  


Most microservice shops go to considerable lengths to automate this part of the process. For example, the Amazon platform offers automation of testing and deployment that starts as soon a developer checks in her code. Since the process of automation can be involved and posting to production can be risky, it is a good idea to treat this as a shared service that all teams learn to use.  


## Data stores  


There are many data storage platforms available today, from classic SQL- based systems to JSON document stores on through graph- style databases such as Riak and Neo4J. It is usually not effective for large organizations to support all possible storage technologies. Even today, some organizations struggle with providing proper support for the many storage implementations they have onsite. It makes sense for your organization to focus on a select few storage platforms and make those available to all your developer teams.  


## Service orchestration  


The technology behind service orchestration or service interoperability is another one that is commonly shared across all teams. There is a wide range of options here. Many of the flagship microservice companies (e.g., Netflix and Amazon) wrote their own orchestration platforms. We'll cover more on this in Chapter 5.  


## Security and identity  


Platform- level security is another shared service. This often happens at the perimeter via gateways and proxies. Again, some companies have written their own frameworks for this; Netflix's Security Monkey is an example. There are also a number of security products available. Shared identity services are sometimes actually external to the company. We'll talk more about this in Chapter 6.  


## Architectural policy  


Finally, along with shared security, sometimes additional policy services are shared. These are services that are used to enforce company- specific patterns or models—often at runtime through a kind of inspection or even invasive testing.


--- Page 68 ---

One example of policy enforcement at runtime is Netflix's "Simian Army"—a set of services designed to purposely cause problems on the network (simulate missing packets, unresponsive services, and so on) to test the resiliency of the system.  


Another kind of policy tooling is one that standardizes the way outages or other mishaps are handled after the fact. These kinds of after- action reviews are sometimes called postmortems. For example, Etsy created (and open sourced) a tool for standardizing postmortems called Morgue. Whether in the form of runtime monitors or postmortem analysis, policy services ensure that varying teams adhere to the same guidance on how to handle both resiliency and security in their implementations.  


## Local Capabilities  


Local capabilities are the ones that are selected and maintained at the team or group level. One of the primary goals of the local capabilities set is to help teams become more self- sufficient. This allows them to work at their own pace and reduces the number of blocking factors a team will encounter while they work to accomplish their goals. Also, it is common to allow teams to make their own determination on which developer tools, frameworks, support libraries, config utilities, etc., are best for their assigned job. Sometimes these tools are selected from a curated set of "approved" products. Sometimes these tools are created in- house (even by the same team). Often they are open source, community projects.  


Finally, it is important that the team making the decision is also the one taking responsibility for the results. Amazon's Werner Vogels' describes it this way:  


You build it, you run it.  


Werner Vogels, Amazon CTO  

  


In small organizations, it is likely that the local capability elements will be the same for the entire company (e.g., the small startup is just a single team anyway). However, as the company grows, acquires new products, and expands into new technology and market spaces, forcing everyone to continue to use the same developer tools, routing implementations, etc., does not scale well. At that point, it makes sense to allow product groups to start making those decisions for themselves.  


Most local capabilities services are ones that access and/or manipulate the shared service. For example, Netflix created a tool to make it easy for teams to spin up Amazon machine images (or AMIs) called Aminator, and another tool to make deploying code to those cloud images (called Asgard). Both of these tools make dealing with AMIs and deployments a "self- service" experience. Dev teams don't need to rely on


--- Page 69 ---

someone else to spin up machines or install software on them—the team does that themselves.  


Here's a rundown of the common local capabilities for microservice environments:  


## General tooling  


A key local capability is the power to automate the process of rolling out, monitoring, and managing VMs and deployment packages. Netflix created Asgard and Aminator for this. A popular open source tool for this is Jenkins.  


## Runtime configuration  


A pattern found in many organizations using microservices is the ability roll out new features in a series of controlled stages. This allows teams to assess a new release's impact on the rest of the system (are we running slower?, is there an unexpected bug in the release?, etc.). Twitter's Decider configuration tool is used by a number of companies for this including Pinterest, Gilt, and Twitter. This tool lets teams use configuration files to route traffic from the "current" set of services to the "newly deployed" set of services in a controlled way. In 2014, Twitter's Raffi Kirkorian explained Decider and other infrastructure topics in an InfoQ interview. Facebook created their own tool called Gatekeeper that does the same thing. Again, placing this power in the hands of the team that wrote and released the code is an important local capability.  


## Service discovery  


There are a handful of popular service discovery tools including Apache Zoo- keeper, CoreOS' etcd, and HashiCorp's Consul. We'll cover the role of discovery tools in Chapter 6. These tools make it possible to build and release services that, upon install, register themselves with a central source, and then allow other services to "discover" the exact address/location of each other at runtime. This ability to abstract the exact location of services allows various teams to make changes to the location of their own service deployments without fear of breaking some other team's existing running code.  


## Request routing  


Once you have machines and deployments up and running and discovering services, the actual process of handling requests begins. All systems use some kind of request- routing technology to convert external calls (usually over HTTP, Web- Sockets, etc.) into internal code execution (e.g., a function somewhere in the codebase). The simplest form of request routing is just exposing HTTP endpoints from a web server like Apache, Microsoft IIS, NodeJS, and others. However, as service requests scale up, it is common to "front" the web servers with specialized routing proxies or gateways. Netflix created Zuul to handle their routing. There are popular open source services like Netty (created by JBoss) and Twitter's Finagle. We'll talk more about gateways in Chapter 6.


--- Page 70 ---

## System observability  


A big challenge in rapidly changing, distributed environments is getting a view of the running instances- seeing their failure/success rates, spotting bottlenecks in the system, etc. There are quite a few tools for this. Twitter created (and open sourced) Zipkin for this task, and there are other similar frameworks that provide visibility into the state of the running system.  


There is another class of observability tooling- those that do more than report on system state. These tools actually take action when things seem to be going badly by rerouting traffic, alerting key team members, etc. Netflix's Hystrix is one of those tools. It implements a pattern known as the Circuit Breaker to improve the resiliency of running systems.  


## Culture  


Along with establishing goals and principles and arming your organization with the right tools for managing platform, code, and runtime environments, there is another critical foundation element to consider- your company culture. Culture is important because it not only sets the tone for the way people behave inside an organization, but it also affects the output of the group. The code your team produces is the result of the culture.  


But what is culture? Quite a bit has been written about culture in general- from many perspectives including anthropological as well as organizational. We'll focus on the organizational point of view here. In her 1983 paper, "Concepts of Culture and Organizational Analysis", Linda Smircich describes culture as "shared key values and beliefs" that convey a sense of identity, generate commitment to something larger than the self, and enhances social stability. Damon Edwards of DTO Solutions and one of the organizers of the DevOpsDays series of events defines culture as "why we do it the way we do it".  


So, how does culture affect team output? And, if it does, what kinds of team culture improve team performance and work quality? We'll look at three aspects of culture that you should consider as a foundation for your microservice efforts:  


## Communication  


Research shows that the way your teams communicate (both to each other and to other teams) has a direct measurable effect on the quality of your software.  


## Team alignment  


The size of your teams also has an effect on output. More people on the team means essentially more overhead.


--- Page 71 ---

Fostering innovation  


Innovation can be disruptive to an organization but it is essential to growth and long- term success.  


## Focus on Communication  


One of the best- known papers on how culture affects team output is Mel Conway's 1968 article in Datamation magazine, "How Do Committees Invent?" The line most often quoted from this short and very readable paper is:  


Organizations which design systems ... are constrained to produce designs that are copies of the communication structures of these organizations.  - Mel Conway, author of "How Do Committees Invent?"  


Put simply, communication dictates output.  


This quote was identified in 1975 by Fred Brooks as "Conway's law" and it provides some important insights on the importance of organizational structure affecting the quality of the final product of the company. Conway's paper identifies a number of reasons for this assertion as well as directives on how to leverage this understanding to improve the group's output. A 2009 study for Microsoft Research showed that "organizational metrics are significantly better predictors of error- proneness" in code than other more typical measures including code complexity and dependencies.  


Another key point in Conway's article is that "the very act of organizing a team means certain design decisions have already been made." The process of deciding things like the size, membership, even the physical location of teams is going to affect the team choices and, ultimately, the team output. This gives a hint to the notion of applying Conway's law when setting up your team structure for a software project (sometimes referred to as a "reverse Conway"). By considering the communication needs and coordination requirements for a software project, you can set up your teams to make things easier, faster, and to improve overall communication.  


## Aligning Your Teams  


Team alignment is important—it affects the quality of code. What can we do to take advantage of this information? Using the information from the start of this chapter, what "tunable" elements can we use to improve the alignment of our team structures to meet our goals for increasing speed, resilience, and visibility for our microservice efforts?  


In his 1998 paper, "The Social Brain", British anthropologist Robin Dunbar found that social group sizes fall into predictable ranges. "[T]he various human groups that can be identified in any society seem to cluster rather tightly around a series of values (5, 12, 35, 150, 500, and 2,000)." These groups each operate differently. The first (5) relies very much on a high- trust, low- conversation mode: they seem to understand


--- Page 72 ---

each other without lots of discussion. Dunbar found that, as groups get larger, more time is spent on maintaining group cohesion. In his book Grooming, Gossip and the Evolution of Language, Dunbar suggests that in large primate groups up to \(40\%\) of time is spent in grooming just to maintain group stability. He points out that this grooming behavior in primates is replaced by gossip and other trivial conversations in humans.  


Dunbar's "grooming" in primates is analogous to meetings, emails, and other forms of communication in organizations that are often seen as time wasters. The possibility of increasing the number of internal meetings with large groups at Amazon in the early days of their AWS services implementation prompted Jeff Bezos to quip:  


No, communication is terrible!  


Jeff Bezos, Amazon founder and CEO  


This led to Bezos' now famous "two- pizza team" rule. Any team that cannot be fed by two pizzas is a team that is too big.  


Fred Brooks' 1975 book The Mythical Man Month contains the classic observation that "adding [more people] to a late software project makes it later." This maxim speaks directly to the notion that adding people increases communication overhead, similar to the findings of Dunbar.  


As the size of the group grows, the number of unique communication channels grows in a nonlinear way. This instance of combinatorial explosion is a common problem and needs to be kept in mind as you design your teams.  


When we talk to companies working in the microservices way, they commonly cite team sizes that match closely to Dunbar's first two groups (5 and 12). We refer to these as Dunbar levels 1 and 2, respectively. For example, Spotify, the Swedish music streaming company, relies on a team size of around seven (what they call a [squad). They also rely on an aggregate of several teams that they call a tribe and reference Dunbar's work directly when describing how they came to this arrangement.  


There are a number of other factors in establishing your teams including responsibilities, deliverables, and skillsets that need to be present within a team. We'll cover details on how to go about selecting and tuning these elements later in the book.  


## Fostering Innovation  


A third important element in managing company culture is fostering innovation within your organization. Many companies say they want to make innovative thinking common within the organization. And the ability to take advantage of creative and innovative ideas is sometimes cited as a reason to adopt a microservice approach to developing software. So it makes sense to spend a bit of time exploring what innovation looks like and how it can affect your organization.


--- Page 73 ---

A simple definition of innovate from Merriam- Webster's dictionary is "to do something in a new way; to have new ideas about how something can be done." It's worth noting that being innovative is most often focused on changing something that is already established. This is different than creating something new. Innovation is usually thought of as an opportunity to improve what a team or company already has or is currently doing.  


A common challenge is that the innovation process can be very disruptive to an organization. Sometimes "changing the way we do things" can be seen as a needless or even threatening exercise—especially if the change will disrupt some part of the organization (e.g., result in eliminating tasks, reducing workload, or even replacing whole teams). For this reason, the act of innovating can be difficult. Another problem with innovation is that the actual process often looks chaotic from the outside. Innovating can mean coming up with ideas that might not work, that take time to get operating properly, or even start out as more costly and time consuming than the current practice. Yet, many organizations really want to encourage innovative work within their teams.  


Companies we talked to enable innovation by adopting a few key principles. First, they provide a level of autonomy to their teams. They allow teams to determine the best way to handle details within the team. Netflix calls this the principle of "context, not control." Team leaders are taught to provide context for the team's work and guidance on meeting goals, but to not control what the team does. Netflix's Steve Urban explains it like this:  


I have neither the place, the time, nor the desire, to micromanage or make technical decisions for [my team].  


—Steve Urban, Netflix engineer  


Second, companies that foster innovation build in a tolerance for some level of chaos. They operate with the understanding that it's OK if some things look a bit disorganized or messy. Of course, there are limits to this. Harvard Business Review's "Managing Innovation: Controlled Chaos" points out that "Effective managers of innovation ... administer primarily by setting goals, selecting key people, and establishing a few critical limits and decision points for intervention." Fostering innovation means setting boundaries that prevent teams from taking actions that threaten the health and welfare of the company and allowing teams to act on their own within these safe boundaries.  


Managing communication channels, aligning teams, and establishing a safe place to innovate are all essential to enabling a successful culture that can take advantage of a microservice- style approach to designing, implementing, and maintaining software.


--- Page 74 ---

## Summary  


In this chapter we've reviewed the common set of platform capabilities called Cockcroft's "microservices concerns" and cited examples of how a number of organizations provide these platform capabilities to their teams. We also focused on the teams themselves. The way your teams communicate, their size, and the level of innovation you support within those teams have a significant effect on the quality of their output.  


So, with these ideals in mind, what does it take to actually implement microservice solutions? In the next two chapters we'll show you working examples of the platform capabilities we discussed here as well as offer guidance on component design and implementation that follows the recommended principles from this chapter.


--- Page 75 ---

# Microservices in Practice  


## The Microservices Way at Hootsuite  


Vancouver- based Hootsuite is a pioneer in social media for business. The company was formed by members of Invoke Media who built a platform to manage their own social network interactions and then realized that other companies had the same need. As the company grew, so did their monolithic, PHP- based platform. In order to meet the demands of their market through a \(100+\) team of developers, they are evolving their application to a collection of product- oriented microservices.  


Hootsuite took a design- based approach to their microservice migration from the outset. They recognized that defining the right logic boundaries can be a harder problem than introducing new technology. They use what they call "distributed domain- driven design" as a means of breaking services out of their monolith. API definitions and associated contracts provide a means of describing service scope and function, and API consumers are involved in the creation of both. The Hootsuite team found that API design guidelines helped to create a common language for this process. Over time, Hootsuite has classified their microservices into three categories: data services that encapsulate key business entities and ensure scalability, functional services that combine data services with business logic to execute core business logic, and facade services that decouple consumer contracts from core functional logic. Hootsuite's design approach continues to evolve as their microservice implementation matures.  


Hootsuite's organization includes product- aligned teams made up of five to seven people. They also have a cross- functional platform team that is responsible for frameworks and tooling, and has visibility across the organization. To address common
