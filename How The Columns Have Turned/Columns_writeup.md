# How the Colums Have Turned

> The key is: 729513912306026 [name=last line of dialog.txt]

The key never changes because they messed up the encryption algorithm so it maths out to the same value every time.
The code in the py file says `twistedColumnarEncrypt`.

...in all honesty I did not notice that it was "twisted" columnar encrypt and not just "normal" columnar encrypt so idk if that has any significance. (so I just looked into it and yes, a program does already exist to rearrange this. I wasted about two hours on it yesterday.)

Anyways, I did find that I had to rearrange chunks of the decoded text to make it somewhat make sense.

The ciper decrypts to this... rearranged every 15 character chunk:
 
THE LOCATION OF THE
CONVOY DANTE IS D
ETERMINED TO BE ON
THE THIRD PLANET A
FTER VINYR YOU CAN
USE LIGHT SPEED AF
TER THE DELIVERYS

THE CARGO IS SAFE W
E NEED TO MOVE FAST
CAUSE THE RADARS A
ROUND THE TRAJECT
ORY OF THE PLANET A
REPICKING UP SUSP
ICIOUSACTIVITY A

BE CAREFUL SKOLI W
HEN YOU ARRIVE AT T
HE PALACEOFSCION
SAY THE CODE PHRAS
E TO GET IN HTB THE L
CG IS VULNERABLE W
E NEED TO CHANGE IT 

DONT FORGET TO CHA
NGE THE DARK FUEL O
F THE SPACESHIP WE
DONT WANT ANY UNPL
EASANT SURPRISES
TO HAPPEN THIS SER
IOUS MISSION POPO

IF YOU MESS UP AGAIN
ILL SEND YOU TO TH
E ANDROID GRAVE YA
RD TO SUFFER FROM T
HE CONSTANT TERMI
NATION OF YOUR KIN
D A FINAL WARNING M

>"The flag consists entirely of uppercase characters and has the form HTB{SOMETHINGHERE}. You still have to add the {} yourself." [name=HTB][color=#1de051]

It is not HTB{BECAREFULSKOLIWHENYOUARRIVEATTHEPALACEOFSCION}, nor HTB{THECODEPHRASE}, nor HTB{THELCG}, nor HTB{THELCGISVULNERABLE}

...
It was HTB{THELCGISVULNERABLEWENEEDTOCHANGEIT}.
