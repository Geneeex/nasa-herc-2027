# Rover views and dimensioned figures

[Back to the project](../../README.md) · [CAD guide](../README.md) · [Design baseline](../../docs/design-baseline.md)

Eight supplied figures show the rover exterior, wheel module and annotated design dimensions. The original files are preserved at full resolution. Select any figure to open its image file; the [figure index](figure-index.json) records the source names, pixel dimensions and SHA-256 hashes.

## Rover overview

[![Three-quarter view of the rover showing the body, camera mast, antenna, wheels and suspension](rover-oblique.jpg)](rover-oblique.jpg)

**Figure 3 — Three-quarter view.** The overall view brings the four-wheel layout, raised sensor housing and visible suspension into one illustration.

## Front and side views

| Front view | Side view |
|:---:|:---:|
| [![Front view of the rover and its wheel stance](rover-front.jpg)](rover-front.jpg) | [![Side profile of the rover with camera mast and antenna](rover-side.jpg)](rover-side.jpg) |
| **Figure 1.** Body, front wheel stance and visible suspension arrangement. | **Figure 4.** Body profile, wheel placement and raised equipment. |

## Wheel and suspension detail

[![Close view of a wheel, suspension arm, pivot and paired springs](wheel-suspension.jpg)](wheel-suspension.jpg)

**Figure 2 — Wheel module.** This view makes the visible arm, pivot and spring arrangement easier to inspect. It does not specify travel, spring rate, damping, load capacity or assembly tolerances.

## Annotated design dimensions

These values reproduce the annotations supplied with the figures. The millimetre values are the design references; the inch values are rounded as shown. Refer to the [controlled design baseline](../../docs/design-baseline.md) for the current assumptions.

| Dimension | Millimetres | Inches shown | Figure |
|---|---:|---:|---|
| Rover width | 630 | 24.80 | 5 |
| Rover length | 655 | 25.79 | 7 |
| Height to camera top, excluding antenna | 421 | 16.57 | 7 |
| Wheel width | 90 | 3.54 | 6 |
| Wheel outside diameter, including tread | 215 | 8.46 | 8 |
| Rim outside diameter | 188 | 7.40 | 8 |
| Rim-to-tread radial span | 13.5 | 0.53 | 8 |

### Overall width

[![Front view annotated with rover width of 630 mm or 24.80 inches](rover-width.png)](rover-width.png)

**Figure 5 — 630 mm width.** The arrow spans the outside edges of the wheels in the front view.

### Length and camera-top height

[![Side view annotated with length of 655 mm and height of 421 mm to the top of the camera housing, excluding the antenna](rover-length-height.png)](rover-length-height.png)

**Figure 7 — 655 mm length and 421 mm camera-top height.** The vertical reference ends at the camera housing, while the antenna extends above it. The 421 mm label therefore does not describe the complete antenna-inclusive envelope. The separate historical task-scene record gives a model height near 432 mm; these supplied drawings have not been checked against that native model.

### Wheel width

[![Wheel and suspension view annotated with a wheel width of 90 mm or 3.54 inches](wheel-width.png)](wheel-width.png)

**Figure 6 — 90 mm wheel width.** The annotation describes the wheel width, not the full arm or suspension assembly.

### Wheel, rim and radial span

[![Wheel drawing with 215 mm overall diameter, 188 mm rim outer diameter and a 13.5 mm radial span including tread](wheel-dimensions.png)](wheel-dimensions.png)

**Figure 8 — Wheel geometry.** The supplied label calls 13.5 mm the tyre radial thickness including tread. Here that value is interpreted as the nominal rim-to-tread radial span: `(215 - 188) / 2 = 13.5 mm`. It is **not a minimum printed tyre wall thickness** and does not establish internal tyre geometry or print settings.

## Using these figures

Use these images for design discussion and documentation alongside the [architecture diagrams](../../diagrams/README.md) and [illustrative task scenes](../README.md#task-scene-previews). They are rendered design views, not photographs or evidence of completed hardware tests. Source CAD files, manufacturing tolerances and a new model verification are not provided by this figure update.
