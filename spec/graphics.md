
# Bee Graphic

Bee has native minimal graphic support. This is a speciality domain that require Unicode and makes Bee a versatile tool for dynamic drowing, 2D and 3D objects in Carthesian spaces. Bee will support radians and decimal degree symbols. 

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

Rational Approximations

* Archimedes' Fraction: $\frac{22}{7} \approx 3.142857$ (accurate to 2 decimal places).
* Milward's Fraction / Adrian Anthoniszoon: $\frac{355}{113} \approx 3.1415929$ (accurate to 6 decimal places, exceptionally efficient for its denominator size).
* Algorithmic Computation via Rational SeriesComputers calculate $\pi$ using infinite series where each term is a rational number. Summing these rational fractions converges on $\pi$.

* Leibniz Formula (Slow):

$$\pi = 4 \sum_{k=0}^{\infty} \frac{(-1)^k}{2k+1} = 4 \left(1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \dots\right)$$

**compiler recalculation**

** Bee will implement one of these algorithms to calculate and cash a constant value at runtime, with a specified precision, and cash this value for duration of execution. This is a small price to pay at the beginning just in case we need extreme precision.

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

**Note:** Mandatory in the core language, we need support for these symbols.

## Graphic types

We define specific subtypes for graphics as subsets of existing basic types. The signature is a proposal to define these subtypes.


| Type | Name | Signature | Description |
|:--- |:--- |:--- |
| Canvas  | {o ∈ P, w,h ∈ Z, m ∈ [Layer]} | Canvas (with points and shapes) |
| Layer   | {c ∈ B, v ∈ B, m ∈ [Shape]}   | Layer with c = color, m = set of shapes |
| Shape   | {o ∈ P, s ∈ ⌂,   θ ∈ Angle }  | Shape, with origin and rotation |
| Label   | {o ∈ P, t ∈ S, α, β ∈ Angle}   | Graphic label with rotation |


**legend**


```
w = width
h = height
s = shape
m = members
d = distance
v = visible
```

**Note:** Can be implemented as language extensions using Bee itself, no need for core implementation

## Drawing Elements

Each graphic element is a composite data type.


| Name | Signature   | Meaning
| :--- | :---        | :---         |
| RAD  | (0 .. 2π)   | Radian Range |
| DEG  | (0°..360°)  | Degree Range |
| CRT  | {x, y ∈ Q}  | Cartesian Point   |
| POL  | {r ∈ P, θ ∈ RAD }   | Polar Point |
| VEC  | {o, p ∈ CRT }       | Vector |
| CRC  | {o ∈ CRT,  r ∈ P }  |  Circle  |
| ARC  | {o ∈ CRT,  r ∈ P, θ₁, θ₂ ∈ DEG } | Arc | 
| SQR  | {o ∈ CRT,  r ∈ P, θ ∈ DEG} | Square with rotation |
| TRG  | {a, b, c ∈ CRT, θ₁, θ₂, θ₃ ∈ DEG} | Triangle |
| REG  | {o ∈ CRT, n, r ∈ P, θ ∈ DEG} | Regular Shape |
| PLG  | {v ∈ [VEC] } | Polygon Shape |
| ISO  | {d ∈ P, θ₁, θ₂ DEG} | ISO Fill Pattern  {▤, ▥, ▦, ▧, ▨, ▩} |


- We use default rational numbers Q for precisi

**Note:** Can be implemented as language extensions using Bee itself, no need for core implementation

## Drawing keywords

In the future we can define comands to draw as keywords:

| Table |
| --- |
| Keyword | Description |
| draw | create a shape on a layer |
| wipe | remove a drown shapes from a layer |
| show | show canvas |
| hide | hide canvas |

**TODO:** - Need to define if these are rules or hard coded keywords.

## Latitude Longitude

Any location on Earth is described by two numbers: its latitude and its longitude. If a pilot or a ship captain wants to specify position on a map, these are the "coordinates" they would use.


Latitude and longitude are two angles, measured in degrees, "minutes of arc" and "seconds of arc." These are denoted by the symbols ( "°", "′", "″" ) For example: 35° 43′ 9″ means an angle of 35 degrees, 43 minutes and 9 seconds. A degree contains 60 minutes of arc and a minute contains 60 seconds of arc and you may omit the words "of arc" where the context makes it absolutely clear that these are not units of time.


Bee language has limited support for measurement units. Calculations often represent angles by small letters of the Greek alphabet, and that way latitude will be represented by λ (lambda, Greek L), and longitude by φ (phi, Greek F). Here is how they are defined.


## Data Types

- Δ = Distance  :meters
- λ = Longitude :g° m′ s″
- φ = Latitude  :g° m′ s″

```
type DST: (0..+100000000) <: Q; -- Δ twice equatorial precision
type LON: (-180°..+180° ) <: Q; -- λ longitude angle range (degree)
type LAT: (-90°..+90°   ) <: Q; -- φ latitude angle range (degree)
```

**Note:** May be implemented for cartography extension

## Map Data

Map data is a special use-case. We can define Unicode symbols to be used as data types:

- • = Node: { Shape Point }
- ↯ = Link: { Street, Trail }
- ⇄ = Lane
- ⌘ = Complex Intersection
- ◉ = Intersection
- ◈ = Place of Interest ( Food, Market, Gas ...)
- ▣ = Area of Interest ( Park, Stadium, Golf )
- § = SpLine ( Border, Railway, River)
- ■ = Area ( Water, Forest )

This could lead to very compact definitions, easy for trained eye to see.

```
-- map simple point: λ = Latitude, φ = Longitude, i = index
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

**legend**

- φ = longitude
- λ = latitude
- ε = elevation

**Note:** May be implemented in extension libraries.

## Space objects

For games and space maps, maybe is a good idea to create a special library that define additional types.

| Type | Description |
| :--- | :--- |
| Galactic | Galactic space |
| Solar | Solar space |
| Star | A celestial body similar to the Sun with position relative to our Sun |
| Planet | Planed similar to Earth with: mass, radius, year duration, day duration |
| Moon | Natural celestial body bound to a planet by gravity |
| Satellite | Artificial celestial body bound to a planet or moon by gravity |
| Craft | Space-craft capable to travel in space, not bounded to a planet |

**Note:** May be implemented in extension libraries.

## Planets symbols

We aknowledge these symbols but we have no intention to implement in the language:

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

**Note:** May be implemented in extension libraries.

---

[Go back](concurrency.md) | [Read next](library.md)
