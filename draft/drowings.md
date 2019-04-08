## Bee Graphic

To be useful we have to extend Bee language with graphics.


## Constants

 symbol | value
--------|-------
 π      | 3.14
 ⊥      | π/2

## Data types

Each graphic element is a composite data type.

 Type  | Name     | Description
-------|----------|---------------------------------
  ∠    | Angle    | <: N[0..2 · π] 
  ⊡    | Point    | {x, y ∈ R}
  ↗    | Vector   | {o, p ∈ ⊡}
  ↺    | Polar    | {o ∈ ⊡, r ∈ Δ, α ∈ ∠ }  
  ◯    | Circle   | {o ∈ ⊡, r ∈ Δ}  
  ◴    | Arc      | {o ∈ ⊡, r ∈ Δ, α,β ∈ ∠ }
  □    | Square   | {o ∈ ⊡, b ∈ Δ}
  ◁    | Triangle | {o ∈ ⊡, b ∈ Δ, α,β,ɣ ∈ ∠}
  ◇    | Diamond  | {o ∈ ⊡, α,β ∈ ∠} 
  ⎊    | Regular  | {o ∈ ⊡, r ∈ +Δ, n ∈ Δ}
  ⌂    | Shape    | {o ∈ ⊡, s @ [⊡]}
  ◪    | Fill     | { ■, ▤, ▥, ▦, ▧, ▨, ▩ } 

**unused**

```  
∘ ∙  ↺ ↻ ∟ ⊞ ⊠ ⊗ ⊕ ♀ ♂ ☺ ↱ ⎋ ⎋ ↺↗
```

Type   | Signature                 |
-------|---------------------------|-------------------------------------------------
Δ      | <: R[0..+]                | Distance or length
V      | {o ∈ ⊡, d ∈ Δ}            | 2D vectorial space
H      | {o ∈ ⊡, s ∈ ⌂, α ∈ ∠ }    | Any shape, with origin and rotation
Y      | {c ∈ N, v ∈ [L], m @ [H]} | 2D Layer with c = color, m = set of shapes
G      | {o ∈ ⊡, w,h ∈ Z, m @ [Y]} | Graphic canvas (with points and shapes)

**legend**
```
w = with
h = height
s = shape
m = members
d = distance
v = visible 
```

## Space objects

Type     | Description
---------|-------------------------------------------------------------------------
Galactic | Galactic space
Solar    | Solar space
Star     | A celestial body similar to the Sun with position relative to our Sun
Planet   | Planed similar to Earth with: mass, radius, year duration, day duration
Moon     | Natural celestial body bound to a planet by gravity
Satellite| Artificial celestial body bound to a planet or moon by gravity
Craft    | Space-craft capable to travel in space, not bounded to a planet

## Drawing keywords

Keyword  | Description
---------|-----------------------------------
draw     | draw anything that is not a dot
plot     | place a dot
show     | show canvas
hide     | hide canvas
wait     | wait a number of seconds
erase    | remove a drawing shape
clear    | remove all drawings from a layer