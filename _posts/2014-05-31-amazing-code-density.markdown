---
layout: post
title: Amazing code density
---

Take a look at this very brief
[demo](http://www.youtube.com/watch?v=8jilQsFjD48&t=0m8s). You might
be thinking it's a bit charitable to call it a "demo" because it's kind
of lame... but it turns out that version is only 8 bytes. That's a
pretty amazing 8 bytes!

I was curious how it worked, so I took a look at an updated version
that's been further optimized to be only 7 bytes long, and even fixes
the screen not getting cleared.

It is of course a DOS .com file because there's no way to approach that
size otherwise. Ostensibly, this is the whole code, though as we'll see
later this isn't the whole story:

    loop:
      c4 1c     LES bx,[si]
      9f        LAHF
      ab        STOSW
      91        XCHG cx,ax
      eb fa     JMP loop+1

DOS programs load at offset 0x100, with the segment registers all set to
the same segment, and both the instruction pointer and SI pointing to
0x100.

The first instruction (LES) loads a 16:16 segment:offset from the memory
pointed to by SI into ES:BX. In this case SI is pointing at the
instruction itself, so it loads BX with 0x1cc4, and ES with the next two
bytes, so ES = 0xab9f.

The next instruction is a LAHF, which loads the 8 bit flags register
into AH (the top half of AX). The flags register starts as
`C0 Z0 S0 O0 A0 P0 D0 I1 T0` and isn't affected by LES. So, AH is loaded
with 0x02, and AX becomes 0x0200.

Next, the STOSW stores AX into ES:DI. Hmm. Well, AX is 0x0200. And ES:DI
is 0xab9f:fffe. So, this time, we store 0x0200 into some random place in
memory (possibly in the bitmap graphics area?). Not important, but
harmless. Colour text video memory is mapped at 0xb8000, and eventually
by repeating the STOSW which advances DI, we'll get to DI=0xcc70 and so
ES:DI will be ab9f:cc70 == 0xb8000, and we'll start putting stuff on the
screen. Conveniently 0x02 is the console attribute meaning bright green
giving the nice "Matrix-y" colour.

Next, we XCHG CX,AX. CX = 0x00ff, so after the swap, CX=0x0200,
AX=0x00ff. The top byte here is 0x00 which is black-on-black so the next
STOSW will write some character, but it will effectively be clearing
that character.

Now comes some magic: the JMP jumps to loop+1. That is, into the middle
of the LES instruction. This is then decoded as "1c 9f", which is "SBB
AL, 0x9f". This is subtracts 0x9f from AL, which effectively randomizes
AL, so we get the cycling letter pattern as we cycle through the loop,
while maintaining the 0x02 in the top half of AX for the colour.

After the SBB, we STOSW, XCHG and JMP again. This time we write a black
byte, next time we write green, and repeat. We're still writing into
random memory at this point, but eventually we get to 0xb8000, fill the
screen, and then DI loops back to 0 and we start again.

So, a summary of the bytes:

"C4 1C" is used in two different ways for code (LES, SBB), and as data
as well (though this loaded data value is unimportant).

"9F" is the most amazingly reused byte: At first it's the very important
LAHF which loads the colour into AH. Later, it's the operand to the SBB
instruction, and is prime, so cycles effectively through the character
set to randomize the output. Finally, it's loaded into the ES register
as data along with 0xab to point more or less at video memory.

"AB" is used in two ways, as the STOSW that does the main work of
filling video memory, but also as data for the top part of the ES
register. This is quite serendipitous as there's a relatively small
range for the segment to be able to hit text video memory.

"91 EB FA" are regular code. The toggling between CX/AX is pretty clever
to create vertical lines and of course the JMP causes the
reinterpretation of LES to SBB.

Some pretty amazing code density. Props to one Mr
[HellMood](http://www.pouet.net/prod.php?which=63126).

