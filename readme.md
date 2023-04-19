# Psec: A Turkish Programming Language
Psec is a new programming language written in Turkish. It aims to be as similar to pseudo code as possible in order to make it easier for Turkish-speaking individuals to learn programming.

### Why Psec?
Programming can be a challenging skill to learn, especially for those who are new to the field. Psec aims to simplify the process of learning programming for Turkish speakers by providing a language that is easy to understand and use. By using Psec, individuals who are just starting their journey in programming can focus on learning the core concepts and structures of programming, without struggling to understand complex syntax or technical terms.

Psec has been designed to be as similar to pseudo code as possible, making it easy to read and understand for anyone who can read Turkish. By using familiar language constructs, Psec eliminates the need to memorize complex syntax, which can be a barrier to entry for many beginners.

### Features of Psec
Psec has been designed with simplicity in mind, so it is straightforward to learn and use. Some of its features include:

- Easy-to-read syntax: Psec syntax is designed to be as close as possible to the natural Turkish language, making it easy for beginners to understand the logic of programming.

- Readable and understandable code: Psec code is easy to read and understand, even for individuals who are not familiar with programming.

- Low entry barrier: Psec has a low entry barrier, so individuals who are new to programming can quickly start writing code without needing to invest a lot of time learning a complex syntax.


### Getting started with Psec
To get started with Psec, check out the documentation and sample code available on our Github page.

### Installation Steps

**Prerequisites**:
Before we start, make sure that you have the following software installed on your machine:
- Git
- Python 3.x

**Installation:**
1. Open a terminal window or command prompt on your machine.

2. Navigate to the directory where you want to install Psec.

3. Clone the Psec repository by running the following command:
`git clone https://github.com/kerbal_galactic/psec.git`
4. Once the repository has been cloned, navigate to the psec directory by running the following command:
`cd psec`
5. Install the required dependencies by running the following command:
`pip install -r requirements.txt`

### Usage
**Interpreter**:
    Will be added soon.

**Compiling Psec Code**:
To compile a Psec program, you need to use the pseudo.py command-line tool that comes with the Psec package. Here is an example of how to compile a Psec program:

`python pseudo.py program.pc --compile`

As a result, an executable will be created with its dependencies placed in the 'dist' folder. Use the `--onefile` option if you want to compile it to an executable that can be distributed.

`python pseudo.py program.pc --compile --onefile`

Any errors that might occur while the code is being executed or compiled are typically suppressed. The `--debug` option is used to enable runtime warnings and exceptions. This is helpful if you want to identify any execution-related problems.

Using the `--bytecode` option, Psec code can also be converted to Python byte code. This option will generate a byte code output file with the extension ".pyc" in "\_\_pycache\_\_" directory.

### Contribution
We welcome contributions to Psec from anyone who is interested in helping us grow and improve the language. If you would like to contribute, you can fork the repository and create a pull request with your changes.