# Compiling Techniques – Macrogenerator

## General overview and assumptions

An assignment is to design macrogenerator which does not allow to specify any parameters in macrodefinition. However, what is special about this macrogenerator is that it processes macrodefinition without parameters but it can be overcome using nested macrodefinitions which are supported by this macrogenerator.

The available discriminants:

| **Discriminant** | **Description** |
| --- | --- |
| &amp; | Macrodefinition |
| $ | Macrocall |

To indicate the end of macrodefinition we reused the sign &#39;&amp;&#39;. Hence, macrodefinition structure presents as follow:

**&amp;**name body**&amp;**

**Assumption:** We must somehow distinguish whether &#39;&amp;&#39; indicates beginning of a new macrodefinition or the end of currently examined one. To somehow overcome this problem I assumed that &#39;&amp;&#39;, which is directly followed by name (without any white signs between), is a starting discriminant and &#39;&amp;&#39; , which is directly followed by white sign or macrocall discriminant, is closing discriminant.

## Functional requirements

The purpose of macrogenerator is to perform text transformation according to macrodefinitions and macrocalls specified by the user. Because, macrodefinition can be specified by the user inside source text we are dealing with _dynamic_ transformation and it is necessary to enhance macrogenerator with a proper macrodefinitions&#39; library data structure to allow hierarchical substitution. More information can be found in _Data structures_ section. Examples of usage can be found in _Input/Output_ section.

## Implementation

### General architecture

| **Class UML** |
| --- |
| ![alt text](https://db3pap002files.storage.live.com/y4mgXpqFL7S-1N44zs1XTC6qAU8A7hxYnj-Yc-J-eSU74t90bjEzC3BJxQEx7vX3nic4z_7rb_1-v7xZjsBgLIJ5baxUAFxFjyJfgqyHfvCUR5E3DeHXX0lwlRqHtjtH1jqQkFo-dI_R8N74jZWE_j9nYHGBkR6l-2l2RZYGd1ErzrlSpYEn-MOlqFP-MeBTW7mhIVxYNcYLt7Hn56NQExPBQ/uml.png?psid=1&width=340&height=365) |
| **Description** |
| **Macrogenerator class** |
| _MACRODEF\_DISCRIMINANT_ – discriminant indicating macrodefinition. |
| _MACROCALL\_DISCRIMINANT_ – discriminant indicating macrocall. |
| _macrolibrary_ – Macrolibrary class object used to organize macrodefinitions&#39; library. |
| _transform(source\_text: str): str_ – function transforming _source\_text_ in a specified way. |
| _macrodefinition(): void_ – support function to define macrodefinition in macrogenerator. |
| _macrocall(mname: str): str_ – support function to perform macrocall. |
| _free\_text(): str_ – support function to perform free text reading and writing to output. |
| **Macrolibary class** |
| _library_ – list containing macrodefinitions. |
| _mbody(mname: str): str_ – function that returns mbody based on mname passed. |
| _increase\_level(): void_ – increases text level (appends new slot for macrodefinitions in library). |
| _decrease\_level(): void_ – decreases text level (remove lastly append slot from library). |
| _insert(macrodef: pair): void_ – inserts mname and corresponding mbody at current text level. |

### Data structures

| **Parameter** | **Description** |
| --- | --- |
| Macrolibrary | List of macrodefinitions. Due to, the fact that we are going to use hierarchical substitution, indices of a list will indicate current level of text level diagram. |
| Macrodefinition | Pair of MNAME (macrodefinition name) and MBODY (macrodefinition body). |

**Remark:** At each level of text level diagram more than one macrodefinition may appear. Hence, Macrolibrary must be define as list which allows to store more than one macrodefinition under one index. It may be implemented as a list of hash maps, where each hash map describe macrodefinitions defined at a particular level (list index).

### Module descriptions

Main function of a module is a _transform_ function. The flowchart below presents data flow through _transform_ function.

![](https://db3pap002files.storage.live.com/y4mu3p8gXtAkkF-e3zD_HGMI0Apn4AOkf7VHTb6-ERHRjwkEJYsLoHIKnKkbdvEPd333QCjoKlxBNEDCSeMc3ijnmlBUUxrKIttUxE-IeEp8-ChHMAkPEpOk3ne9t2ZzrblbCwy9ZwSUyps2Mjsl2VF2UhD24yiN46tAKIJ3Awgd_SkRB7A3YtdVveicMZfJ89XXmTzrldQxQNTkj0zQYcqsA/transform%20flowchart.png?psid=1&width=661&height=879) <br />
_Flowchart illustrating algorithm of transform function_

**Remark:** It is worth to notice that when macrocall is spotted the function perform recursive substitution. Flowchart does not depict error handling for which I propose exceptions&#39; mechanism.

### Input/output description

Macrogenerator takes as an input source text, which may contain macrodefinition and according to them and macrocalls transforms source text and produces output text. Below some examples of transformation performes by macrogenerator.

Example 1: Basic macrodefinition and macrocall._

| **Input** | **Output** |
| --- | --- |
| &amp;COMPILE g++ &amp; $COMPILE | _g++_ |

Where, &quot;_COMPILE_&quot; is a macrodefinition name, &quot;_g++_&quot; - is a macrodefinition body.

Example 2: Nesting macrodefinition.

| **Input** | **Output** |
| --- | --- |
| &amp;COMPILE gcc­ -c &amp;NAME main.cpp**&amp;** $NAME &amp; $COMPILE | _gcc -c main.cpp_ |

&quot;_COMPILE&quot;_ is outer macrodefinition and &quot;_NAME&quot;_ is a nested macrodefinition.

Example 3: Invalid nesting of macrodefinition.

| **Input** | **Output** |
| --- | --- |
| &amp;COMPILE gcc­ -c  &amp;main.cpp $COMPILE | _ERROR_ |

Because of macrogenerator previous assumption, about specifying starting macrodefinition &#39;&amp;&#39; and ending one, _main.cpp_ will not be treated as a _free text_ but as a new macrodefinition name . Further source text processing will cause an error because there are no macrodefinition closing discriminants (&#39;&amp;&#39;). <br /> <br />

Full documentation: https://github.com/wiktorlazarski/Macrogenerator/blob/master/docs/ECOTE%20Final%20project.pdf
