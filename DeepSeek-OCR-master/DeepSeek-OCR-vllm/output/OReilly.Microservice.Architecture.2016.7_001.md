--- Page 1 ---
  


# Microservice Architecture  


ALIGNING PRINCIPLES, PRACTICES, AND CULTURE  


Irakl Nadareishvili, Ronnie Mitra, Matt McLarty & Mike Amundsen


--- Page 2 ---

## Microservice Architecture  


Microservices can have a positive impact on your enterprise- just ask Amazon and Netflix- but you can fall into many traps if you don't approach them in the right way. This practical guide covers the entire microservices landscape, including the principles, technologies, and methodologies of this unique, modular style of system building. You'll learn about the experiences of organizations around the globe that have successfully adopted microservices.  


In three parts, this book explains how these services work and what it means to build an application the microservices way. You'll explore a design- based approach to microservice architecture with guidance for implementing various elements. And you'll get a set of recipes and practices for meeting practical, organizational, and cultural challenges to microservice adoption.  


Learn how microservices can help you drive business objectives Examine the principles, practices, and culture that define microservice architectures Explore a model for creating complex systems and a design process for building a microservice architecture Learn the fundamental design concepts for individual microservices Delve into the operational elements of a microservice architecture, including containers and service discovery Discover how to handle the challenges of introducing microservice architecture in your organization  


"This book will help you answer some important questions: What problems do microservices solve for, and how should organizations and cultures be set up to succeed?"  


- Adrian Cockcroft Technology Fellow, Battery Ventures  


Irakl Nadareishvili is CTO and cofounder of New York healthtech startup ReferWell.  


Ronnie Mitra is Director of Design at the API Academy at CA Technologies.  


Matt McLarty (@mattmclartybc) is Vice President of the API Academy at CA Technologies.  


Mike Amundsen is Director of Architecture for the API Academy at CA Technologies.  


Twitter: @oreillymedia facebook.com/oreilly


--- Page 3 ---

# Praise for Microservice Architecture  


The authors' approach of starting with a value proposition, "Speed and Safety at Scale and in Harmony," and reasoning from there, is an important contribution to thinking about application design.  


—Mel Conway, Educator and Inventor  


A well- thought- out and well- written description of the organizing principles underlying the microservices architectural style with a pragmatic example of applying them in practice.  


—James Lewis, Principal Consultant, ThoughtWorks  


This book demystifies one of the most important new tools for building robust, scalable software systems at speed.  


—Otto Berkes, Chief Technology Officer, CA Technologies  


If you've heard of companies doing microservices and want to learn more, Microservice Architecture is a great place to start. It addresses common questions and concerns about breaking down a monolith and the challenges you'll face with culture, practices, and tooling. The microservices topic is a big one and this book gives you smart pointers on where to go next.  


—Chris Munns, Business Development Manager—DevOps, Amazon Web Services  


Anyone who is building a platform for use inside or outside an organization should read this book. It provides enough "a- ha" insights to keep everyone on your team engaged, from the business sponsor to the most technical team member. Highly recommended!  


—Dave Goldberg, Director, API Products, Capital One


--- Page 4 ---

A practical roadmap to microservices design and the underlying cultural and organizational change that is needed to make it happen successfully.  


—Mark Boyd, Writer/Analyst, Platformable  


An essential guidebook for your microservices journey, presenting the concepts, discussions, and structures supportive of this architectural pattern as well as the pragmatic ground work to become successful. —Ian Kelly, Experimenter and Contributor, CA Technologies


--- Page 5 ---

# Microservice ArchitectureAligning Principles, Practices, and Culture  


Irakl Nadareishvili, Ronnie Mitra, Matt McLarty, and Mike Amundsen


--- Page 6 ---

## Microservice Architecture  


by Irakli Nadareishvili, Ronnie Mitra, Matt McLarty, and Mike Amundsen  


Copyright © 2016 Mike Amundsen, Matt McLarty, Ronnie Mitra, Irakli Nadareishvili. All rights reserved.  


Printed in the United States of America.  


Published by O'Reilly Media, Inc., 1005 Gravenstein Highway North, Sebastopol, CA 95472.  


O'Reilly books may be purchased for educational, business, or sales promotional use. Online editions are also available for most titles (http://safaribooksonline.com). For more information, contact our corporate/ institutional sales department: 800- 998- 9938 or corporate@oreilly.com.  


Editors: Brian MacDonald and Holly Bauer  Production Editor: Kristen Brown  Copyeditor: Christina Edwards  Proofreader: Kim Cofer  


Indexer: WordCo Indexing Services, Inc.  Interior Designer: David Futato  Cover Designer: Karen Montgomery  Illustrator: Melanie Yarbrough  


June 2016: First Edition  


## Revision History for the First Edition  


2016- 06- 02: First Release  2016- 07- 18: Second Release  


See http://oreilly.com/catalog/errata.csp?isbn=9781491956250 for release details.  


The O'Reilly logo is a registered trademark of O'Reilly Media, Inc. Microservice Architecture, the cover image, and related trade dress are trademarks of O'Reilly Media, Inc.  


While the publisher and the authors have used good faith efforts to ensure that the information and instructions contained in this work are accurate, the publisher and the authors disclaim all responsibility for errors or omissions, including without limitation responsibility for damages resulting from the use of or reliance on this work. Use of the information and instructions contained in this work is at your own risk. If any code samples or other technology this work contains or describes is subject to open source licenses or the intellectual property rights of others, it is your responsibility to ensure that your use thereof complies with such licenses and/or rights.


--- Page 7 ---

# Table of Contents  


Preface. ix  


## Part I. Understanding Microservices  


1. The Microservices Way. 3  


Understanding Microservices 4  Adopting Microservices 5  "What are microservices? Don't I already have them?" 6  "How could this work here?" 7  "How would we deal with all the parts? Who is in charge?" 8  The Microservices Way 9  The Speed of Change 9  The Safety of Change 9  At Scale 10  In Harmony 10  Summary 11  


## 2. The Microservices Value Proposition. 13  


Microservice Architecture Benefits 13  Deriving Business Value 15  Defining a Goal-Oriented, Layered Approach 17  Modularized Microservice Architecture 17  Cohesive Microservice Architecture 18  Systematized Microservice Architecture 18  Maturity Model for Microservice Architecture Goals and Benefits 19  Applying the Goal-Oriented, Layered Approach 20  Summary 21


--- Page 8 ---

## Part II. Microservice Design Principles  


3. Designing Microservice Systems. 25  


The Systems Approach to Microservices 25Service 27Solution 28Process and Tools 28Organization 28Culture 29Embracing Change 29Putting it Together: The Holistic System 30Standardization and Coordination 30A Microservices Design Process 33Set Optimization Goals 34Development Principles 35Sketch the System Design 35Implement, Observe, and Adjust 36The Microservices System Designer 38Summary 38  


4. Establishing a Foundation. 41  


Goals and Principles 42Goals for the Microservices Way 42Operating Principles 45Platforms 49Shared Capabilities 50Local Capabilities 52Culture 54Focus on Communication 55Aligning Your Teams 55Fostering Innovation 56Summary 58  


## Part III. Microservices in Practice  


5. Service Design. 61  


Microservice Boundaries 62Microservice Boundaries and Domain-Driven Design 62Bounded Context 64Smaller Is Better 65Ubiquitous Language 66


--- Page 9 ---

API Design for Microservices 67  Message- Oriented 67  Hypermedia- Driven 68  Data and Microservices 70  Shipping, Inc. 70  Event Sourcing 72  System Model for Shipping, Inc. 75  CQRS 76  Distributed Transactions and Sagas 78  Asynchronous Message- Passing and Microservices 80  Dealing with Dependencies 81  Pragmatic Mobility 84  Summary 86  


6. System Design and Operations. 89  Independent Deployability 89  More Servers, More Servers! My Kingdom for a Server! 91  Docker and Microservices 93  The Role of Service Discovery 94  The Need for an API Gateway 97  Security 97  Transformation and Orchestration 98  Routing 100  Monitoring and Alerting 101  Summary 101  


7. Adopting Microservices in Practice. 103  Solution Architecture Guidance 104  How many bug fixes/features should be included in a single release? 104  When do I know our microservice transformation is done? 104  Organizational Guidance 105  How do I know if my organization is ready for microservices? 105  Culture Guidance 106  How do I introduce change? 106  Can I do microservices in a project-centric culture? 108  Can I do microservices with outsourced workers? 108  Tools and Process Guidance 109  What kinds of tools and technology are required for microservices? 109  What kinds of practices and processes will I need to support microservices? 110  How do I govern a microservice system? 111  Services Guidance 112


--- Page 10 ---

Should all microservices be coded in the same programming language? 112  What do I do about orphaned components? 113  Summary 113  


A. Microservice Architecture Reading List 117  Index 121


--- Page 11 ---

Microservice architecture has emerged as a common pattern of software development from the practices of a number of leading organizations. These practices includes principles, technologies, methodologies, organizational tendencies, and cultural characteristics. Companies taking steps to implement microservices and reap their benefits need to consider this broad scope.  


## Who Should Read This Book  


Who Should Read This BookYou should read this book if you are interested in the architectural, organizational, and cultural changes that are needed to succeed with a microservice architecture. We primarily wrote this book for technology leaders and software architects who want to shift their organizations toward the microservices style of application development. You don't have to be a CTO or enterprise architect to enjoy this book, but we've written our guidance under the assumption that you are able to influence the organizational design, technology platform, and software architecture at your company.  


## What's In This Book  


This book promotes a goal- oriented, design- based approach to microservice architecture. We offer this design- centric approach because, as we talked to several companies about their programs, we discovered one of the keys to their success was the willingness to not stick to a single tool or process as they attempted to increase their company's time- to- market while maintaining—even increasing—their systems' safety and resilience.  


The companies we talked to offered a wide range of services including live video and audio streaming service, foundation- level virtual services in the cloud, and support for classic brick- and- mortar operations. While these companies' products vary, we learned that the principles of speed and safety "at scale" were a common thread. They


--- Page 12 ---

each worked to provide the same system properties in their own unique ways—ways that fit the key business values and goals of the company.  


It's the properties and values that we focus on in this book, and the patterns and practices we see companies employ in order to reach their unique goals. If you're looking for a way to identify business goals for your microservices adoption, practical guidance on how to design individual microservices and the system they form, and tips on how to overcome common architectural challenges, this is your book!  


## The Outline  


The book is organized into three parts. The first part (Chapters 1- 2) identifies the principles and practices of microservice architecture and the benefits they can provide. This section will be valuable to anyone who needs to justify the use of microservices within their organization and provide some background on how other organizations have started on this journey.  


The second part (Chapters 3- 4) introduces a design- based approach to microservice architecture, identifies a series of common processes and practices we see repeated through successful microservice systems, and provides some implementation guidance on executing the various elements for your company's microservice implementation.  


The third and final part (Chapters 5- 7) provides a set of practical recipes and practices to help companies identify ways to introduce and support microservices, meet immediate challenges, and plan for and respond to the inevitably changing business environment ahead.  


Here's a quick rundown of the chapters:  


Chapter 1, The Microservices Way  


This chapter outlines the principles, practices, and culture that define microservice architecture.  


Chapter 2, The Microservices Value Proposition  


This chapter examines the benefits of microservice architecture and some techniques to achieve them.  


Chapter 3, Designing Microservice Systems  


This chapter explores the system aspects of microservices and illustrates a design process for microservice architecture.  


Chapter 4, Establishing a Foundation  


This chapter discusses the core principles for microservice architecture, as well as the platform components and cultural elements needed to thrive.


--- Page 13 ---

## Chapter 5, Service Design  


This chapter takes the "micro" design view, examining the fundamental design concepts for individual microservices.  


## Chapter 6, System Design and Operations  


This chapter takes the "macro" design view, analyzing the critical design areas for the software system made up of the collection of microservices.  


## Chapter 7, Adopting Microservices in Practice  


This chapter provides practical guidance on how to deal with common challenges organizations encounter as they introduce microservice architecture.  


## Chapter 8, Epilogue  


Finally, this chapter examines microservices and microservice architecture in a timeless context, and emphasizes the central theme of the book: adaptability to change.  


## What's Not In This Book  


The aim of this book is to arm readers with practical information and a way of thinking about microservices that is timeless and effective. This is not a coding book. There is a growing body of code samples and open source projects related to microservices available on the Web, notably on GitHub and on sites like InfoQ. In addition, the scope of this domain is big and we can only go so deep on the topics we cover. For more background on the concepts we discuss, check out our reading list in Appendix A.  


While we provide lots of guidance and advice—advice based on our discussions with a number of companies designing and implementing systems using microservice architecture patterns—we do not tell readers which product to buy, which open source project to adopt, or how to design and test component APIs. Instead, we offer insight into the thinking processes and practices of experienced and successful companies actually doing the work of microservices. If you're looking for simple answers, you're likely to be disappointed in some of the material here. If, on the other hand, you're looking for examples of successful microservice companies and the kinds of principles, practices, and processes they employ, this book is for you.  


## Conventions Used in This Book  


The following typographical conventions are used in this book:  


Italic  


Indicates new terms, URLs, email addresses, filenames, and file extensions.


--- Page 14 ---

## Constant width  


Used for program listings, as well as within paragraphs to refer to program elements such as variable or function names, databases, data types, environment variables, statements, and keywords.  


## Constant width bold  


Shows commands or other text that should be typed literally by the user.  


## Constant width italic  


Shows text that should be replaced with user- supplied values or by values determined by context.  

  


This element signifies a tip or suggestion.  

  


This element signifies a general note.  

  


This element indicates a warning or caution.  


## Safari® Books Online  

  


Safari Books Online is an on- demand digital library that delivers expert content in both book and video form from the world's leading authors in technology and business.  


Technology professionals, software developers, web designers, and business and creative professionals use Safari Books Online as their primary resource for research, problem solving, learning, and certification training.  


Safari Books Online offers a range of plans and pricing for enterprise, government, education, and individuals.  


Members have access to thousands of books, training videos, and prepublication manuscripts in one fully searchable database from publishers like O'Reilly Media,


--- Page 15 ---

Prentice Hall Professional, Addison- Wesley Professional, Microsoft Press, Sams, Que, Peachpit Press, Focal Press, Cisco Press, John Wiley & Sons, Syngress, Morgan Kaufmann, IBM Redbooks, Packt, Adobe Press, FT Press, Apress, Manning, New Riders, McGraw- Hill, Jones & Bartlett, Course Technology, and hundreds more. For more information about Safari Books Online, please visit us online.  


## How to Contact Us  


Please address comments and questions concerning this book to the publisher:  


O'Reilly Media, Inc.  1005 Gravenstein Highway North  Sebastopol, CA 95472  800- 998- 9938 (in the United States or Canada)  707- 829- 0515 (international or local)  707- 829- 0104 (fax)  


To comment or ask technical questions about this book, send email to bookquestions@oreilly.com.  


For more information about our books, courses, conferences, and news, see our website at http://www.oreilly.com.  


Find us on Facebook: http://facebook.com/oreilly  


Follow us on Twitter: http://twitter.com/oreillymedia  


Watch us on YouTube: http://www.youtube.com/oreillymedia  


## Acknowledgments  


The authors would like to thank Brian MacDonald, Holger Reinhardt, Ian Kelly, and Brian Mitchell for helping to clarify, focus, and structure the content of the book. We would also like to thank John Allspaw, Stu Charlton, Adrian Cockcroft, Mel Conway, James Lewis, Ruth Malan, and Jon Moore for helping to guide our thinking along the way.  


A number of early microservice adopters provided insight for the book. We would like to thank Greg Bell, Ken Britton, Beier Cai, Steve Cullingworth, Bill Monkman, Mike Sample, and Jeremy Skelton of Hootsuite; Chris Munns of Amazon; Clay Garrard and Patrick Devlin of Disney; and Christian Deger of AutoScout24.  


The book would not have been completed without the support of CA Technologies. We would like to thank Alex Jones, Jeff Miller, Ryan Blain, Jaime Ryan, Sam Macklin, and many others for their help. We would also like to thank Leia Poritz, Heather


--- Page 16 ---

Scherer, Rachel Roumeliotis, Sharon Cordesse, Kristen Brown, Christina Edwards, and the team at O'Reilly Media.  


Finally and most importantly, the authors would like to thank their families. Mike thanks Lee, Shannon, Jesse, and Dana for putting up with his usual travel and writing shenanigans. Matt thanks Chris, Daniel, and Josiah for their love and support. Ronnie thanks his father for putting him in front of a computer. Irakli thanks Ana, Dachi, Maia, Diana, and Malkhaz for their unconditional support and encouragement.


--- Page 17 ---

# Understanding Microservices  


## Balancing Speed and Safety  


If you drive around Sweden you'll see variations of the same road markings, road signs, and traffic signals that are used everywhere else in the developed world. But Sweden is a remarkably safer place for road users than the rest of the world. In fact, in 2013 it was among the safest countries in road traffic deaths per 100,000 people.  


So, how did the Swedes do it? Are they better drivers? Are the traffic laws in Sweden stricter than other countries? Are their roads just better designed? It turns out that the recipe for traffic safety is a combination of all of these things, delivered by an innovative program called Vision Zero.  


Vision Zero has a laudable goal—reducing all road accident- related deaths to zero. It aims to achieve this by designing road systems that prioritize safety above all other factors, while still recognizing the importance of keeping traffic moving. In other words, a road system that is designed first and foremost with safety in mind.  


At its core, Vision Zero is about culture change. Policymakers, traffic system designers, and citizens have a shared belief that the safety of pedestrians and drivers is more valuable than the need to move from place to place as quickly as possible. This culture of safety drives individual behavior, which can result in a more desirable outcome for the traffic system.  


In addition, the road system itself is designed to be safer. Traffic designers apply speed limits, road signs, and traffic movement patterns in a way that benefits the overall safety of the system. For example, while it is necessary to ensure the move


--- Page 18 ---

ment of cars on the road, speed is limited to a level that the human body could withstand in a collision given the technical standards of the vehicles and roads that exist. While speed limits may impact drivers' ability to get to their destination as quickly as possible, the design decision is always driven by the requirement to protect human life. Where most road systems are designed to facilitate movement (or speed) in a safe way, Vision Zero systems incorporate movement into a system primarily designed for safety.  


The road designers are continuously making trade- offs that favor the safety of its users. Instead of solely relying on skilled drivers who know how to avoid common mistakes, Vision Zero designers create roads that account for the errors and miscalculations that many human drivers inevitably make. While it is the driver's responsibility to adhere to the rules of the road, the system designers must do their best to protect humans even in situations where drivers do not conform.  


All in all, the Vision Zero approach seems to work. While they haven't reduced fatalities to zero yet, the program has been so successful in improving safety within Sweden that other cities like New York and Seattle are adopting it and hoping to see similar results in their own traffic systems. In the end, this success was made possible by combining improvements to policy, technology, and infrastructure in a holistic manner. Vision Zero adopts a systematic approach to design in a safety- first manner.  


Just like traffic systems, software systems become more complex as their scale—in the form of scope, volume, and user interactions—increases. And like road designers, software architects and engineers must maintain a balance of speed and safety in their software systems. Software development organizations have used microservice architecture to achieve faster delivery and greater safety as the scale of their systems increase. The holistic, consciously designed approach of Vision Zero suggests an approach to microservice architecture that organizations can take to achieve the balance of speed and safety that meets their goals.


--- Page 19 ---

# The Microservices Way  


Microservices are a thing these days.  


- Phil Calçado, former Director of Engineering, SoundCloud  


Building solutions with speed and safety at scale.  


If you're like most software developers, team leaders, and architects responsible for getting working code out the door of your company, this phrase describes your job in a nutshell. Most of you have probably struggled at this, too. Getting to market quickly seems to imply giving up a bit of safety. Or, conversely, making sure the system is safe, reliable, and resilient means slowing down the pace of feature and bug- fix releases. And "at scale" is just a dream.  


However, a few years ago people started talking about companies that were doing just that. Shortening their time- to- market on new releases, actually improving their system reliability, and doing it all in runtime environments that were able to respond smoothly to unexpected spikes in traffic. These companies were "doing microservices."  


In this chapter we'll explore what microservices are and what it means to build an application the microservices way. To begin with, we'll explore the meaning of the term microservices by learning about its origin. Next, we'll take a look at some of the biggest perceived barriers to adopting microservices. Finally, we share a simple perspective on application development that will help you better understand how all the pieces of microservices systems fit together, a balancing act of speed and safety that we call the microservices way.


--- Page 20 ---

## Understanding Microservices  


To better understand what microservices are, we need to look at where they came from. We aren't going to recount the entire history of microservices and software architecture, but it's worth briefly examining how microservices came to be. While the term microservices has probably been used in various forms for many years, the association it now has with a particular way of building software came from a meeting attended by a handful of software architects. This group saw some commonality in the way a particular set of companies was building software and gave it a name.  


As James Lewis, who was in attendance, remembers it:  


At the end of our three- day meeting, one of us called out a theme—that year it had been clear that many of the problems people were facing in the wild were related to building systems that were too big. "How can I rebuild a part of this," "best ways to implement Strangler," etc.  


Turning that on its head, the problem became "how can we build systems that are replaceable over being maintainable?" We used the term micro apps, I seem to remember.  


—James Lewis  


James' recollection of the microservices origin story is important not only for historical record, but also because it identifies three concepts that are principal to the style:  


## Microservices are ideal for big systems  


The common theme among the problems that people were facing was related to size. This is significant because it highlights a particular characteristic of the microservices style—it is designed to solve problems for systems that are big. But size is a relative measure, and it is difficult to quantify the difference between small, normal, and big. You could of course come up with some way of deciding what constitutes big versus small, perhaps using averages or heuristic measurements, but that would miss the point. What the architects at this gathering were concerned with was not a question of the size of the system. Instead, they were grappling with a situation in which the system was too big. What they identified is that systems that grow in size beyond the boundaries we initially define pose particular problems when it comes to changing them. In other words, new problems arise due to their scale.  


## Microservice architecture is goal-oriented  


Something else we can derive from James' recollection of the day is the focus on a goal rather than just a solution. Microservice architecture isn't about identifying a specific collection of practices, rather it's an acknowledgment that software professionals are trying to solve a similar goal using a particular approach. There may be a set of common characteristics that arise from this style of software


--- Page 21 ---

development, but the focus is meant to be on solving the initial problem of systems that are too big.  


## Microservices are focused on replaceability  


The revelation that microservices are really about replaceability is the most enlightening aspect of the story. This idea that driving toward replacement of components rather than maintaining existing components get to the very heart of what makes the microservices approach special.  

  


If you are interested in learning more on the history of microservices, visit http://api.co/msabook.  


Overwhelmingly, the companies that we talked to have adopted the microservices architectural style as a way of working with systems in which scale is a factor. They are more interested in the goal of improving changeability than finding a universal pattern or process. Finally, the methods that have helped them improve changeability the most are primarily rooted in improving the replaceability of components. These are all characteristics that align well with the core of the microservices ideal.  


## Adopting Microservices  


If you are responsible for implementing technology at your company, the microservices proposition should sound enticing. Chances are you face increasing pressure to improve the changeability of the software you write in order to align better with a business team that wants to be more innovative. It isn't easy to make a system more amenable to change, but the microservice focus on building replaceable components offers some hope.  


However, when we've talked to people interested in adopting microservice- style architectures they often have some reservations. Behind the enthusiasm for a new way of approaching their problem is a set of looming uncertainties about the potential damage that this approach might cause to their systems. In particular, after learning more about microservices methods, potential adopters frequently identify the following issues:  


1. They have already built a microservice architecture, but they didn't know it had a name.  
2. The management, coordination, and control of a microservices system would be too difficult.


--- Page 22 ---

3. The microservices style doesn't account for their unique context, environment, and requirements.  


While we don't believe that microservices is the answer to every question about a potential architecture choice, we do feel that these particular fears should be better understood before dismissing an opportunity to improve a system. Let's take a look at each of these barriers to adoption in more detail.  


## "What are microservices? Don't I already have them?"  


Earlier in this chapter we shared the story of how microservices got their name, but we never actually came up with a concrete definition. While there is not one single definition for the term "microservice," there are two that we think are very helpful:  


Microservices are small, autonomous services that work together.  


- Sam Newman, Thoughtworks  


Loosely coupled service- oriented architecture with bounded contexts.  


- Adrian Cockcroft, Battery Ventures  


They both emphasize some level of independence, limited scope, and interoperability. We also think that it is important to view "a microservice" in the scope of an existing system. For that reason our definition of microservices also includes the architectural element:  


A microservice is an independently deployable component of bounded scope that supports interoperability through message- based communication. Microservice architecture is a style of engineering highly automated, evolvable software systems made up of capability- aligned microservices.  


You may find much of what is described in the preceding definition familiar. In fact, your organization is probably doing something like this already. If you've implemented a service- oriented architecture (SOA), you've already embraced the concept of modularity and message- based communication. If you've implemented DevOps practices you've already invested in automated deployment. If you are an Agile shop, you've already started shaping your culture in a way that fits the microservices advice.  


But given that there is no single, authoritative definition, when do you get to proclaim that your architecture is a microservice architecture? What is the measure and who gets to decide? Is there such a thing as a "minimum viable microservice architecture"?  


The short answer is we don't know. More importantly, we don't care! We've found that the companies that do well with microservices don't dwell on the meaning of this single word. That doesn't mean that definitions are trivial—instead, it's an admission that finding a universal meaning for the microservices style is not important when it comes to meeting business goals. Your time is better spent improving your architec


--- Page 23 ---

ture in a way that helps you unlock more business value. For most organizations this means building applications with more resilience and changeability than ever before. What you call that style of application is entirely up to you.  


If you are considering adopting a microservice architecture for your organization, consider how effective the existing architecture is in terms of changeability and more specifically replaceability. Are their opportunities to improve? Could you go beyond modularity, Agile practices, or DevOps to gain value? We think you'll stand a better chance at providing value to your business team if you are open to making changes that will get you closer to those goals. Later in this chapter we'll introduce two goals that we believe give you the best chance at success.  


## "How could this work here?"  


Earlier in this chapter we shared perspectives on microservices from Newman, Cockcroft, Lewis, and Fowler. From these comments, it is clear that microservice applications share some important characteristics:  


Small in size Messaging enabled Bounded by contexts Autonomously developed Independently deployable Decentralized Built and released with automated processes  


That's a big scope! So big that some people believe that microservices describe a software development utopia—a set of principles so idealistic that they simply can't be realized in the real world. But this type of claim is countered with the growing list of companies who are sharing their microservice success stories with the world. You've probably heard some of those stories already—Netflix, SoundCloud, and Spotify have all gone public about their microservices experiences.  


But if you are responsible for the technology division of a bank, hospital, or hotel chain, you might claim that none of these companies look like yours. The microservices stories we hear the most about are from companies that provide streamed content. While this is a domain with incredible pressure to remain resilient and perform at great scale, the business impact of an individual stream failing is simply incomparable to a hotel losing a reservation, a single dollar being misplaced, or a mistake in a medical report.  


Does all of this mean that microservices is not a good fit for hotels, banks, and hospitals? We don't think so and neither do the architects we've spoken to from each of


--- Page 24 ---

those industries. But we have found that the particular way your organization needs to implement a microservice system is likely to differ from the way that Netflix implements theirs. The trick is in having a clear goal and understanding where the dials are to move your organization toward it. Later in this book we'll shed some light on the principles and practices that help microservices companies succeed.  


## "How would we deal with all the parts? Who is in charge?"  


Two microservices characteristics that you might find especially concerning are decentralization and autonomy. Decentralization means that the bulk of the work done within your system will no longer be managed and controlled by a central body. Embracing team autonomy means trusting your development teams to make their own decisions about the software they produce. The key benefit to both of these approaches is that software changes become both easier and faster—less centralization results in fewer bottlenecks and less resistance to change, while more autonomy means decisions can be made much quicker.  


But if your organization hasn't worked this way in the past, how confident are you that it could do so in the future? For example, your company probably does its best to prevent the damage that any single person's decisions can have on the organization as a whole. In large companies, the desire to limit negative impact is almost always implemented with centralized controls—security teams, enterprise architecture teams, and the enterprise service bus are all manifestations of this concept. So, how do you reconcile the ideals of a microservice architecture within a risk- averse culture? How do we govern the work done by microservices teams?  


Similarly, how do you manage the output of all these teams? Who decides which services should be created? How will services communicate efficiently? How will you understand what is happening?  


We've found that decentralization and control are not opposing forces. In other words, the idea that there is a trade- off between a decentralized system and a governed system is a myth. But this doesn't mean that you gain the benefits of decentralization and autonomy for free. When you build software in this way, the cost of controlling and managing output increases significantly. In a microservice architecture, the services tend to get simpler, but the architecture tends to get more complex. That complexity is often managed with tooling, automation, and process.  


Ultimately, you must come to terms with the fact that asserting control and management of a microservice system is more expensive than in other architectural styles. For many organizations, this cost is justified by a desire for increased system changeability. However, if you believe that the return doesn't adequately outweigh the benefit, chances are this is not the best way to build software in your organization.


--- Page 25 ---

## The Microservices Way  


When you first begin learning about microservice architecture it's easy to get caught up in the tangible parts of the solution. You don't have to look hard to find people who are excited about Docker, continuous delivery, or service discovery. All of these things can help you to build a system that sounds like the microservice systems we've been discussing. But microservices can't be achieved by focusing on a particular set of patterns, process, or tools. Instead, you'll need to stay focused on the goal itself—a system that can make change easier.  


More specifically, the real value of microservices is realized when we focus on two key aspects—speed and safety. Every single decision you make about your software development ends up as a trade- off that impacts these two ideals. Finding an effective balance between them at scale is what we call the microservices way.  


Speed and Safety at Scale and in Harmony.  


The Microservices Way  


## The Speed of Change  


The speed of changeThe desire for speed is a desire for immediate change and ultimately a desire for adaptability. On one hand, we could build software that is capable of changing itself—this might require a massive technological leap and incredibly complex system. But the solution that is more realistic for our present state of technological advancement is to shorten the time it takes for changes to move from individual workers to a production environment.  


Years ago, most of us released software in the same way that NASA launches rockets. After deliberate effort and careful quality control, our software was burned into a permanent state and delivered to users on tapes, CDs, DVDs, and diskettes. Of course, the popularity of the Web changed the nature of software delivery and the mechanics of releases have become much cheaper and easier. Ease of access combined with improved automation has drastically reduced the cost of a software change. Most organizations have the platforms, tools, and infrastructure in place to implement thousands of application releases within a single day. But they don't. In fact, most teams are happy if they can manage a release in a week. Why is that? The answer of course is that the real deterrent to release speed is the fragility of the software they've produced.  


## The Safety of Change  


The Safety of ChangeSpeed of change gets a lot of attention in stories about microservice architecture, but the unspoken, yet equally important counterpart is change safety. After all, "speed kills" and in most software shops nobody wants to be responsible for breaking production. Every change is potentially a breaking change and a system optimized purely
