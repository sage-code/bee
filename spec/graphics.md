
# Bee Graphic

Bee has natige graphic support. This is a speciality domain that require Unicode and makes Bee a versatile tool for drowing diagrams, 2D and 3D objects in Carthesian space. 

Bee support radians using (π) prefix. Instead of (2 * π) you can write ( 2π ). Also Bee support ° symbol to represent decimal degree. These two domain specific notations will make Bee veru distruptive and uncomon but maybe useful.

**degree literal**

With Comb Dot: angle = 30°

| symbol | decima degree |
| :--- | :--- |
| 0   | 0°0′0″ |
| π/4 | 45° |
| π/2 | 90° |
| π   | 180° |
| 2π  | 360° |

**π constant:**

Key Rational Approximations

* Archimedes' Fraction: $\frac{22}{7} \approx 3.142857$ (accurate to 2 decimal places).
* Milward's Fraction / Adrian Anthoniszoon: $\frac{355}{113} \approx 3.1415929$ (accurate to 6 decimal places, exceptionally efficient for its denominator size).

* Algorithmic Computation via Rational SeriesComputers calculate $\pi$ using infinite series where each term is a rational number. Summing these rational fractions converges on $\pi$.

* Leibniz Formula (Slow):

$$\pi = 4 \sum_{k=0}^{\infty} \frac{(-1)^k}{2k+1} = 4 \left(1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \dots\right)$$

**decimal conversion**

$$\text{degrees} = \text{radians} \times \frac{180}{\pi}$$

**Minutes and Seconds:**

Bee is using Unicode symbols prime (′) for minutes and (″) for seconds of arc. These symbols are different from classing single quote or double quotes: `," you usually find on a keyboard.

**Examples:**

```
new α:= 180°   ∈ G;
new β:= 0°0′0″ ∈ G;
```

- Relation operators can convert the measurement units;
- Operator ± should work with degree, minutes and seconds;

## Graphic types


| Type | Name | Signature | Description |
| :--- |:--- |:--- |:--- |
| V | Canvas | {o ∈ P, w,h ∈ Z, m ∈ [Y]} | Canvas (with points and shapes) |
| Y | Layer  | {c ∈ B, v ∈ L, m ∈ [H]}   | Layer with c = color, m = set of shapes |
| H | Shape  | {o ∈ P, s ∈ ⌂, θ ∈ G }    | Shape, with origin and rotation |
| G | Tag    | {o ∈ P, t ∈ S, α, β ∈ G}  | Graphic label with rotation |



legend


```
w = width
h = height
s = shape
m = members
d = distance
v = visible
```


## Drawing Elements


Each graphic element is a composite data type.


| Table |
| --- |
| Type | Name | Description |
| :--- | :--- | :--- |
| G    | Angle | (0 .. 2π) or (0°..360°) |
| C    | Cartesian | {x, y ∈ Q} |
| ⊙    | Polar | {r ∈ P, θ ∈ G } |
| ↗     | Vector | {o, p ∈ ⊡} |
| ↺    | Relative | {o ∈ ⊡, r ∈ P, θ ∈ G } |
| ○    | Circle | {o ∈ ⊡, r ∈ P} |
| ◷    | Arc | {o ∈ ⊡, r ∈ P, θ₁, θ₂ ∈ G } |
| □    | Square | {o ∈ ⊡, b ∈ P} |
| ◁    | Triangle | {o ∈ ⊡, b ∈ P, θ₁, θ₂, θ₃ ∈ G} |
| ◇    | Diamond | {o ∈ ⊡, θ₁, θ₂ ∈ G} |
| ⎊    | Regular | {o ∈ ⊡, r, n ∈ P} |
| ⌂    | Polygon | {o ∈ ⊡, c ∈ [⊡]} |
| ◪    | Fill | { ▤, ▥, ▦, ▧, ▨, ▩ } |


- We use default rational numbers Q
- We use P = positive numbers for distance

## Drawing keywords


| Table |
| --- |
| Keyword | Description |
| draw | put shape on layer |
| wipe | remove drown shapes |
| show | show canvas |
| hide | hide canvas |


## Latitude Longitude


Any location on Earth is described by two numbers: its latitude and its longitude. If a pilot or a ship captain wants to specify position on a map, these are the "coordinates" they would use.


Latitude and longitude are two angles, measured in degrees, "minutes of arc" and "seconds of arc." These are denoted by the symbols ( "°", "′", "″" ) For example: 35° 43′ 9″ means an angle of 35 degrees, 43 minutes and 9 seconds. A degree contains 60 minutes of arc and a minute contains 60 seconds of arc and you may omit the words "of arc" where the context makes it absolutely clear that these are not units of time.


Bee language has limited support for measurement units. Calculations often represent angles by small letters of the Greek alphabet, and that way latitude will be represented by λ (lambda, Greek L), and longitude by φ (phi, Greek F). Here is how they are defined.


## Precision


Earth coordinates can be represented using default Q numbers on 32 bit.


| Table |
| --- |
| .digits | angle (g°) | equivalent | 2 | 0.01° | 1.1132 km | 3 | 0.001° | 111.32 m | 4 | 0.0001° | 11.132 m | 5 | 0.00001° | 1.1132 m (default precision) | Type | Description | Galactic | Galactic space | Solar | Solar space | Star | A celestial body similar to the Sun with position relative to our Sun | Planet | Planed similar to Earth with: mass, radius, year duration, day duration | Moon | Natural celestial body bound to a planet by gravity | Satellite | Artificial celestial body bound to a planet or moon by gravity | Craft | Space-craft capable to travel in space, not bounded to a planet | Type | Name | ☀ | Sun | ☿ | Mercury | ♀ | Venus | ♁ | Earth | ♂ | Marth | ♃ | Jupiter | ♄ | Saturn | ♅ | Uraus | ♆ | Neptun | ♇ | Pluto |
| 2 | 0.01° | 1.1132 km |
| 3 | 0.001° | 111.32 m |
| 4 | 0.0001° | 11.132 m |
| 5 | 0.00001° | 1.1132 m (default precision) |
| Type | Description |
| Galactic | Galactic space |
| Solar | Solar space |
| Star | A celestial body similar to the Sun with position relative to our Sun |
| Planet | Planed similar to Earth with: mass, radius, year duration, day duration |
| Moon | Natural celestial body bound to a planet by gravity |
| Satellite | Artificial celestial body bound to a planet or moon by gravity |
| Craft | Space-craft capable to travel in space, not bounded to a planet |
| Type | Name |
| ☀ | Sun |
| ☿ | Mercury |
| ♀ | Venus |
| ♁ | Earth |
| ♂ | Marth |
| ♃ | Jupiter |
| ♄ | Saturn |
| ♅ | Uraus |
| ♆ | Neptun |
| ♇ | Pluto |



| Table |
| --- |
| Type | Description |
| Galactic | Galactic space |
| Solar | Solar space |
| Star | A celestial body similar to the Sun with position relative to our Sun |
| Planet | Planed similar to Earth with: mass, radius, year duration, day duration |
| Moon | Natural celestial body bound to a planet by gravity |
| Satellite | Artificial celestial body bound to a planet or moon by gravity |
| Craft | Space-craft capable to travel in space, not bounded to a planet |
| Type | Name |
| ☀ | Sun |
| ☿ | Mercury |
| ♀ | Venus |
| ♁ | Earth |
| ♂ | Marth |
| ♃ | Jupiter |
| ♄ | Saturn |
| ♅ | Uraus |
| ♆ | Neptun |
| ♇ | Pluto |



## Data Types

- Δ = Distance :meters
- Λ = Longitude :g° m′ s″
- Φ = Latitude :g° m′ s″

```
type Δ: (0..+100000000) <: Q; -- twice equatorial
type Λ: (-180°..+180° ) <: Q; -- longitude angle (degree)
type Φ: (-90°..+90°   ) <: Q; -- latitude angle (degree)
```


Map data types are represented by Unicode symbols:

- • = Node: { Shape Point }
- ↯ = Link: { Street, Trail }
- ⇄ = Lane
- ⌘ = Complex Intersection
- ◉ = Intersection
- ◈ = Place of Interest ( Food, Market, Gas ...)
- ▣ = Area of Interest ( Park, Stadium, Golf )
- § = Line ( Border, Railway, River)
- ■ = Area ( Water, Forest )
- ♁ = Map
- ⁉ = Condition

```-- map simple point: λ = Latitude, φ = Longitude, i = index
  type • : {i ∈ N, λ ∈ Λ, φ ∈ Φ} <: Object;
-- network node:  λ = Latitude, φ = Longitude, ε = Elevation
  type ◉ : {id ∈ N, λ ∈ Λ, φ ∈ Φ, ε ∈ P} <: Object;
-- network link
  type ↯ : {id ∈ N, start_node ∈ ◉, end_node ∈ ◉, shape ∈ [•]} <: Object;
-- place of interest
  type ◈ : {id ∈ N, point ∈ •, label ∈ S} <: Object;
-- map area
  type ■ : {id ∈ N, origin ∈ •, shape ∈ [•], category ∈ S} <: Object;
-- area of interest
  type ▣ : {id ∈ N, point ∈ •, shape ∈ [•], label ∈ S} <: Object;
-- map data model
  type ♁ : {origin ∈ •, extent ∈ •, scale ∈ Q
             nodes ∈ [◉], links ∈ [↯],
             area ∈ [■], pint ∈ [◈], aint ∈  [▣] } <: Object;
```


legend

- φ = longitude
- λ = latitude
- ε = elevation

## Space objects


| Table |
| Type | Description |
| :--- | :--- |
| Galactic | Galactic space |
| Solar | Solar space |
| Star | A celestial body similar to the Sun with position relative to our Sun |
| Planet | Planed similar to Earth with: mass, radius, year duration, day duration |
| Moon | Natural celestial body bound to a planet by gravity |
| Satellite | Artificial celestial body bound to a planet or moon by gravity |
| Craft | Space-craft capable to travel in space, not bounded to a planet |



## Planets

This is a curiosity. Planets have symbols. Is a feature I have no intention to implement in the language but just in case here is a table:

| Table |
| --- |
| Type | Name |
| ☀ | Sun |
| ☿ | Mercury |
| ♀ | Venus |
| ♁ | Earth |
| ♂ | Marth |
| ♃ | Jupiter |
| ♄ | Saturn |
| ♅ | Uraus |
| ♆ | Neptun |
| ♇ | Pluto |


---

[Go back](concurrency.md) | [Read next](library.md)
